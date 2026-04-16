"""
Integração com API Omnilink WSTT v1.159 (SOAP/WSDL)
Documentação oficial: Manual de Integração WSTT 1.159

Arquitetura assíncrona do WSTT:
  - Telecomandos: comandos enviados ao veículo (ex: PedePosicaoAvulsa)
  - Teleeventos:  eventos recebidos do veículo (ex: Posição Automática)

Fluxo para "Posição Atual":
  BuscarUltimoIdPost  → obtém IDs sequenciais atuais
  ObtemEventosNormais → filtra CodMsg=0x92 (Posição Automática) por IdTerminal

Fluxo para "Rota":
  ObtemEventosNormais(UltimoSequencial=0) → todos eventos do buffer (7 dias)
  filtrar por IdTerminal + intervalo de datas + CodMsg=0x92

Fluxo para "Posição Avulsa" (sob demanda):
  PedePosicaoAvulsa → enfileira comando para veículo (retorna id sequencial)
  ObtemEventosCtrl  → poleia CodMsg=0x91 (resposta da posição avulsa)

Coordenadas no formato: "023_32_13_0_S" (graus_minutos_segundos_décimos_orientação)
"""
import logging
import re
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

from django.core.cache import cache

logger = logging.getLogger(__name__)

# ─── Credenciais e endpoint ──────────────────────────────────────────────────
URL_WSDL  = "https://wstt.omnilink.com.br/iasws/iasws.asmx?WSDL"
USUARIO   = "administrativo@grupojrservicos.com.br"
SENHA_MD5 = "89db6cb87ca3be0c05de956144235fac"

# ─── Códigos CodMsg dos teleeventos (hexadecimal conforme documentação) ───────
CODMSG_POSICAO_AVULSA    = 0x91   # 145 dec — resposta a PedePosicaoAvulsa
CODMSG_POSICAO_AUTOMATICA = 0x92  # 146 dec — posição automática periódica
CODMSG_SINAL_VIDA         = 0x9F  # 159 dec — heartbeat do rastreador

# ─── TTLs de cache ────────────────────────────────────────────────────────────
CACHE_POSICAO_TTL   = 30    # 30 s — posição atual
CACHE_HISTORICO_TTL = 300   # 5 min — rota histórica
CACHE_IDS_TTL       = 10    # 10 s — sequenciais (mínimo permitido pela API)
CACHE_CLIENT_TTL    = 120   # 2 min — instância zeep
CACHE_EVENTOS_TTL   = 300   # 5 min — buffer de eventos (compartilhado posicao+historico)


# ─── Cliente SOAP ─────────────────────────────────────────────────────────────

def _get_client():
    """Retorna cliente SOAP zeep com timeout configurado."""
    try:
        from zeep import Client
        from zeep.transports import Transport
        import requests

        session = requests.Session()
        session.verify = True
        transport = Transport(session=session, operation_timeout=15)
        return Client(URL_WSDL, transport=transport)
    except ImportError:
        raise RuntimeError("zeep não instalado. Execute: pip install zeep")
    except Exception as e:
        raise RuntimeError(f"Falha ao conectar na API Omnilink: {e}")


# ─── Conversões ───────────────────────────────────────────────────────────────

def _mct_id_to_terminal(mct_id: str) -> str:
    """
    Converte MCT ID para IdTerminal hexadecimal (formato usado nos teleeventos).

    A API Omnilink armazena IdTerminal como hex uppercase de 6 chars.
    Exemplo: "OM6034040" → decimal 6034040 → hex "5C1278"

    Retorna string hex uppercase (ex: "5C1278").
    """
    m = re.search(r'\d+', str(mct_id))
    if m:
        n = int(m.group())
        return format(n, 'X').upper()   # ex: 6034040 → "5C1278"
    raise ValueError(f"MCT ID sem parte numérica: '{mct_id}'")


def _parse_coord(texto: str) -> float:
    """
    Converte coordenada Omnilink para graus decimais.

    Suporta dois formatos conforme tipo_wstt da conta:
      - "023_32_13_0_S"  → graus_minutos_segundos_décimos_orientação (padrão)
      - "-23.537"        → decimal direto (se tipo_wstt bit1=1)

    Retorna 0.0 em caso de erro.
    """
    if not texto:
        return 0.0

    texto = texto.strip()

    # Tenta decimal direto (ex: "-23.537" ou "-23,537")
    try:
        return float(texto.replace(',', '.'))
    except (ValueError, TypeError):
        pass

    # Formato graus_minutos_segundos_décimos_orientação
    try:
        partes = texto.split('_')
        if len(partes) >= 4:
            graus    = int(partes[0])
            minutos  = int(partes[1])
            segundos = int(partes[2])
            decimos  = int(partes[3])
            orientacao = partes[4].upper() if len(partes) > 4 else 'N'

            decimal = graus + minutos / 60.0 + (segundos + decimos / 10.0) / 3600.0
            if orientacao in ('S', 'W'):
                decimal = -decimal
            return round(decimal, 6)
    except Exception as e:
        logger.debug(f"Omnilink _parse_coord '{texto}': {e}")

    return 0.0


def _parse_datetime(texto: str) -> datetime | None:
    """Converte string de data/hora para datetime. Aceita múltiplos formatos."""
    for fmt in ('%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M'):
        try:
            return datetime.strptime(texto.strip(), fmt)
        except (ValueError, AttributeError):
            continue
    return None


def _codmsg_to_int(valor: str) -> int:
    """
    Converte CodMsg (sempre hexadecimal no XML, ex: "92") para inteiro.
    Valores com 2-3 hex chars são tratados como hex; resto como decimal.
    """
    valor = valor.strip()
    try:
        # Documentação diz que CodMsg é sempre hex
        return int(valor, 16)
    except ValueError:
        try:
            return int(valor)
        except ValueError:
            return -1


# ─── Parser de XML de teleeventos ─────────────────────────────────────────────

def _parse_teleeventos_xml(xml_str: str, apenas_posicoes: bool = True) -> list[dict]:
    """
    Parseia XML de teleeventos retornado pela API Omnilink.

    Retorna lista de dicts com campos padronizados:
      lat, lng, velocidade, odometro, ignicao, data_hora, id_terminal, cod_msg
    """
    eventos = []
    if not xml_str:
        return eventos

    # A API retorna tags em PascalCase (ex: <TeleEvento>, <IdTerminal>).
    # Normalizamos para lowercase antes de parsear para simplificar o código.
    xml_limpo = re.sub(
        r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
        lambda m: f'<{m.group(1)}{m.group(2).lower()}',
        xml_str.strip()
    )

    if not xml_limpo.startswith('<'):
        return eventos

    # Encapsula fragmento sem elemento raiz
    if not (xml_limpo.startswith('<root') or xml_limpo.startswith('<?xml')
            or xml_limpo.startswith('<listateleeventos')):
        xml_limpo = f'<root>{xml_limpo}</root>'

    try:
        root = ET.fromstring(xml_limpo)
    except ET.ParseError:
        try:
            root = ET.fromstring(f'<root>{xml_limpo}</root>')
        except ET.ParseError as e:
            logger.error(f"Omnilink XML inválido: {e} | início: {xml_str[:200]}")
            return eventos

    for ev in root.iter('teleevento'):
        def _t(tag: str, default: str = '') -> str:
            el = ev.find(tag)
            return (el.text or '').strip() if el is not None else default

        # Tags já estão em lowercase após normalização
        cod_raw = _t('codmsg')
        if not cod_raw:
            continue

        cod_msg = _codmsg_to_int(cod_raw)

        if apenas_posicoes and cod_msg not in (CODMSG_POSICAO_AUTOMATICA, CODMSG_POSICAO_AVULSA):
            continue

        lat = _parse_coord(_t('latitude'))
        lng = _parse_coord(_t('longitude'))

        # Coordenadas (0,0) = posição inválida/GPS sem lock
        if lat == 0.0 and lng == 0.0:
            continue

        ign_val = _t('ignicao')
        if ign_val == '1':
            ignicao = True
        elif ign_val == '0':
            ignicao = False
        else:
            ignicao = None   # valor 2 = indefinido

        # Hodômetro vem em metros, convertemos para km
        try:
            hodometro_km = round(float(_t('hodometro') or 0) / 1000.0, 1)
        except ValueError:
            hodometro_km = 0.0

        try:
            velocidade = float(_t('velocidade') or 0)
        except ValueError:
            velocidade = 0.0

        eventos.append({
            'lat':         lat,
            'lng':         lng,
            'velocidade':  velocidade,
            'odometro':    hodometro_km,
            'ignicao':     ignicao,
            'data_hora':   _t('datahoraevento') or _t('datahora'),
            'id_terminal': _t('idterminal'),
            'cod_msg':     cod_msg,
        })

    return eventos


# ─── BuscarUltimoIdPost ───────────────────────────────────────────────────────

def _buscar_ultimo_id_post() -> dict:
    """
    Obtém os IDs sequenciais atuais via BuscarUltimoIdPost.

    Retorna dict: {'id': int, 'idctrl': int}
    Deve ser chamado uma única vez antes de iniciar o polling.
    """
    cache_key = "omnilink_ultimo_id_post"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        client = _get_client()
        xml_str = client.service.BuscarUltimoIdPost(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
        )

        resultado = {'id': 0, 'idctrl': 0}
        if xml_str:
            try:
                # A API devolve fragmento sem elemento raiz e tags podem ser
                # PascalCase. Normalizamos e encapsulamos antes de parsear.
                xml_raw = str(xml_str).strip()
                xml_low = re.sub(
                    r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
                    lambda m: f'<{m.group(1)}{m.group(2).lower()}',
                    xml_raw
                )
                wrapped = f'<root>{xml_low}</root>'
                root = ET.fromstring(wrapped)
                id_val     = root.findtext('id')     or '0'
                idctrl_val = root.findtext('idctrl') or '0'
                resultado = {
                    'id':     int(id_val.strip()),
                    'idctrl': int(idctrl_val.strip()),
                }
            except Exception as e:
                logger.warning(f"Omnilink BuscarUltimoIdPost parse: {e} | xml: {str(xml_str)[:300]}")

        cache.set(cache_key, resultado, CACHE_IDS_TTL)
        logger.info(f"Omnilink BuscarUltimoIdPost: id={resultado['id']} idctrl={resultado['idctrl']}")
        return resultado

    except Exception as e:
        logger.error(f"Omnilink BuscarUltimoIdPost erro: {e}")
        return {'id': 0, 'idctrl': 0}


# ─── Buffer compartilhado de eventos ─────────────────────────────────────────

def _get_eventos_normais() -> list[dict]:
    """
    Obtém e cacheia o buffer de eventos normais da plataforma Omnilink.

    Compartilhado entre get_ultima_posicao e get_historico_posicoes para evitar
    duas chamadas distintas à API (que causaria erro -413 "aguardar 180s").

    Lookback de 100M IDs ≈ ~4 dias de eventos globais.
    Cache de 5 min (mesmo TTL do cooldown da API).
    """
    cache_key = "omnilink_eventos_normais_v1"
    cached = cache.get(cache_key)
    if cached is not None:
        logger.debug(f"Omnilink cache hit: {len(cached)} eventos")
        return cached

    try:
        ids = _buscar_ultimo_id_post()
        if ids['id'] == 0:
            logger.warning("Omnilink: BuscarUltimoIdPost retornou id=0")
            return []

        ultimo_seq = max(1, ids['id'] - 100_000_000)
        logger.info(f"Omnilink ObtemEventosNormais: UltimoSequencial={ultimo_seq}")

        client = _get_client()
        xml_str = client.service.ObtemEventosNormais(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            UltimoSequencial=ultimo_seq,
        )

        raw = str(xml_str) if xml_str else ''
        logger.debug(f"Omnilink ObtemEventosNormais resposta (inicio): {raw[:200]}")

        eventos = _parse_teleeventos_xml(raw)
        logger.info(f"Omnilink ObtemEventosNormais: {len(eventos)} eventos parseados")

        if eventos:
            cache.set(cache_key, eventos, CACHE_EVENTOS_TTL)
        return eventos

    except Exception as e:
        logger.error(f"Omnilink _get_eventos_normais: {e}")
        return []


# ─── Funções públicas ─────────────────────────────────────────────────────────

def get_ultima_posicao(mct_id: str) -> dict | None:
    """
    Retorna a última posição conhecida do veículo.

    Estratégia:
      1. ObtemEventosNormais com lookback de 5000 eventos
      2. Filtra por IdTerminal e pega o mais recente CodMsg=0x92

    Retorna dict com: lat, lng, velocidade, odometro, ignicao, data_hora, endereco
    ou None se não encontrado.
    """
    cache_key = f"omnilink_pos_{mct_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        id_terminal_str = _mct_id_to_terminal(mct_id)

        # Usa buffer compartilhado (evita segunda chamada API e erro -413)
        todos_eventos = _get_eventos_normais()

        eventos_veiculo = [
            e for e in todos_eventos
            if e.get('id_terminal') == id_terminal_str
        ]

        if not eventos_veiculo:
            logger.info(f"Omnilink: nenhuma posição para IdTerminal={id_terminal_str} (MCT={mct_id})")
            return None

        # O último na lista é o mais recente
        ultimo = eventos_veiculo[-1]
        data = {
            'lat':        ultimo['lat'],
            'lng':        ultimo['lng'],
            'velocidade': ultimo['velocidade'],
            'odometro':   ultimo['odometro'],
            'ignicao':    ultimo['ignicao'],
            'data_hora':  ultimo['data_hora'],
            'endereco':   '',
        }
        cache.set(cache_key, data, CACHE_POSICAO_TTL)
        return data

    except Exception as e:
        logger.error(f"Omnilink get_ultima_posicao({mct_id}): {e}")
        return None


def get_historico_posicoes(mct_id: str, inicio: datetime, fim: datetime) -> list[dict]:
    """
    Retorna lista de posições do veículo no intervalo inicio..fim.

    Estratégia:
      BuscarUltimoIdPost → obtém ID atual (N)
      ObtemEventosNormais(UltimoSequencial = max(1, N - LOOKBACK)) → eventos recentes
      Filtra por IdTerminal e intervalo de datas.

    LOOKBACK = 200000 eventos (cobre vários dias de frota inteira).
    UltimoSequencial=0 é inválido na API (erro -204).

    Retorna lista de dicts: lat, lng, velocidade, odometro, ignicao, data_hora
    (lista vazia se não houver dados).
    """
    fmt_cache = '%Y%m%d%H%M'
    cache_key = f"omnilink_hist_{mct_id}_{inicio.strftime(fmt_cache)}_{fim.strftime(fmt_cache)}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        id_terminal_str = _mct_id_to_terminal(mct_id)

        # Remove timezone de inicio/fim — datetimes da API são sempre naive.
        # Se o Django armazenar com tz (USE_TZ=True), a comparação lançaria TypeError.
        def _naive(dt):
            return dt.replace(tzinfo=None) if getattr(dt, 'tzinfo', None) else dt

        inicio_n = _naive(inicio)
        fim_n    = _naive(fim)

        # Usa buffer compartilhado (evita segunda chamada API e erro -413)
        todos_eventos = _get_eventos_normais()
        logger.info(f"Omnilink historico: {len(todos_eventos)} eventos totais para filtrar")

        pontos = []
        for ev in todos_eventos:
            # Filtra pelo veículo
            if ev.get('id_terminal') != id_terminal_str:
                continue

            # Filtra pelo período da OS (se tiver data/hora parseável)
            dth_str = ev.get('data_hora', '')
            if dth_str:
                dth = _parse_datetime(dth_str)
                if dth is not None and not (inicio_n <= dth <= fim_n):
                    continue

            pontos.append({
                'lat':        ev['lat'],
                'lng':        ev['lng'],
                'velocidade': ev['velocidade'],
                'odometro':   ev['odometro'],
                'ignicao':    ev['ignicao'],
                'data_hora':  ev['data_hora'],
            })

        logger.info(f"Omnilink historico: {len(pontos)} pontos para MCT={mct_id} entre {inicio} e {fim}")

        if pontos:
            cache.set(cache_key, pontos, CACHE_HISTORICO_TTL)
        return pontos

    except Exception as e:
        logger.error(f"Omnilink get_historico_posicoes({mct_id}): {e}")
        return []


def get_historico_operacao(os_obj) -> list[dict]:
    """
    Atalho: busca histórico para o período completo da OS.
    Usa inicio_viagem → termino_viagem do operacional.
    """
    op = getattr(os_obj, 'operacional', None)
    if not op:
        return []

    viatura = os_obj.equipe.viatura if os_obj.equipe else None
    mct_id  = viatura.mct_id if viatura and viatura.mct_id else None
    if not mct_id:
        return []

    inicio = op.inicio_viagem or op.chegada_operacao
    fim    = op.termino_viagem or op.termino_operacao or datetime.now()

    if not inicio:
        return []

    return get_historico_posicoes(mct_id, inicio, fim)


def pede_posicao_avulsa(mct_id: str) -> str | None:
    """
    Solicita posição sob demanda ao veículo via PedePosicaoAvulsa.

    Retorna o ID sequencial do telecomando (para correlacionar a resposta)
    ou None em caso de erro.

    NOTA: A resposta virá assincronamente via ObtemEventosCtrl (CodMsg=0x91).
    Esta função apenas envia o telecomando; use poll_posicao_avulsa() para
    aguardar a resposta.
    """
    try:
        client = _get_client()
        resultado = client.service.PedePosicaoAvulsa(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            idVeiculo=str(mct_id),
        )
        logger.info(f"Omnilink PedePosicaoAvulsa({mct_id}): {resultado}")
        return str(resultado) if resultado else None
    except Exception as e:
        logger.error(f"Omnilink PedePosicaoAvulsa({mct_id}): {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# ESPELHAMENTOS — Compartilhamento de rastreadores entre contas Omnilink
# ══════════════════════════════════════════════════════════════════════════════

def _parse_espelhamentos_xml(xml_str: str) -> list[dict]:
    """Parseia XML de ListarEspelhamentosByClienteStatus."""
    resultado = []
    if not xml_str:
        return resultado
    xml_low = re.sub(
        r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
        lambda m: f'<{m.group(1)}{m.group(2).lower()}',
        str(xml_str).strip()
    )
    try:
        root = ET.fromstring(f'<root>{xml_low}</root>')
    except ET.ParseError:
        try:
            root = ET.fromstring(xml_low)
        except ET.ParseError as e:
            logger.error(f"Omnilink espelhamentos XML: {e}")
            return resultado

    def _t(el, tag):
        node = el.find(tag)
        return (node.text or '').strip() if node is not None else ''

    for esp in root.iter('espelhamento'):
        resultado.append({
            'id':                      _t(esp, 'id'),
            'placa':                   _t(esp, 'placa'),
            'serial':                  _t(esp, 'serial'),
            'id_cliente':              _t(esp, 'id_cliente'),
            'id_cliente_destino':      _t(esp, 'id_cliente_destino'),
            'status':                  _t(esp, 'status'),
            'data_cad':                _t(esp, 'data_cad'),
            'data_exp':                _t(esp, 'data_exp'),
            'user_cad':                _t(esp, 'user_cad'),
            'user_aceite':             _t(esp, 'user_aceite'),
            'data_aceite':             _t(esp, 'data_aceite'),
            'status_aceite':           _t(esp, 'status_aceite'),
            'cnpj_central':            _t(esp, 'cnpj_central'),
            'id_central':              _t(esp, 'id_central'),
            'nome_central':            _t(esp, 'nome_central') or _t(esp, 'base_destino') or _t(esp, 'basedestino'),
            'espelhamento_obrigatorio': _t(esp, 'espelhamento_obrigatorio'),
        })
    return resultado


def listar_espelhamentos(status: str = '', data_inicio: str = '', data_fim: str = '') -> list[dict]:
    """
    Lista espelhamentos da conta via ListarEspelhamentosByClienteStatus.

    status: '' ou None = todos | '0' = aguardando | '1' = aceito | '2' = recusado
    data_inicio / data_fim: 'dd/MM/yyyy'  (máx 30 dias, obrigatório)
    """
    if not data_inicio:
        from datetime import datetime, timedelta
        hoje = datetime.now()
        data_fim    = hoje.strftime('%d/%m/%Y')
        data_inicio = (hoje - timedelta(days=30)).strftime('%d/%m/%Y')

    try:
        client = _get_client()
        xml_str = client.service.ListarEspelhamentosByClienteStatus(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            Status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        logger.info(f"Omnilink ListarEspelhamentos ({data_inicio}→{data_fim}): {str(xml_str)[:200]}")
        return _parse_espelhamentos_xml(xml_str)
    except Exception as e:
        logger.error(f"Omnilink listar_espelhamentos: {e}")
        return []


def criar_espelhamento(placa: str, data_expiracao: str,
                       cnpj_destino: str = '', id_central: str = '',
                       obrigatorio: int = 0) -> dict:
    """
    Cria espelhamento enviado (JR → cliente).

    Tenta primeiro CriarEspelhamento (método direto com destino),
    depois CriarSolicitacaoEspelhamentoReverso como fallback.

    placa:          placa do rastreador JR a compartilhar
    data_expiracao: 'dd/MM/yyyy HH:mm:ss'
    cnpj_destino:   CNPJ/CPF da base destino (opcional)
    id_central:     ID numérico da central destino (opcional)
    obrigatorio:    0=ambos podem excluir  1=somente destino

    Retorna dict: {'ok': bool, 'id_sequencia': str, 'mensagem': str}
    """
    try:
        client = _get_client()

        # ── Tenta método direto (com destino explícito) ───────────────────
        for nome_metodo in ('CriarEspelhamento', 'CriarCompartilhamento',
                            'EnviarEspelhamento', 'NovoEspelhamento'):
            op = getattr(client.service, nome_metodo, None)
            if op is None:
                continue
            try:
                if cnpj_destino:
                    resultado = op(Usuario=USUARIO, Senha=SENHA_MD5,
                                   Placa=placa, CNPJ=cnpj_destino,
                                   data_expiracao=data_expiracao,
                                   Espelhamento_Obrigatorio=obrigatorio)
                else:
                    resultado = op(Usuario=USUARIO, Senha=SENHA_MD5,
                                   Placa=placa, IdCentral=id_central,
                                   data_expiracao=data_expiracao,
                                   Espelhamento_Obrigatorio=obrigatorio)
                logger.info(f"Omnilink {nome_metodo}({placa}): {resultado}")
                return {'ok': True, 'id_sequencia': str(resultado), 'mensagem': str(resultado), 'metodo': nome_metodo}
            except Exception as e_inner:
                logger.debug(f"Omnilink {nome_metodo} falhou: {e_inner}")
                continue

        # ── Fallback: CriarSolicitacaoEspelhamentoReverso ────────────────
        # ATENÇÃO: este método NÃO aceita IdCentral nem CNPJ.
        # Assinatura real: Usuario, Senha, Placa, data_expiracao, Espelhamento_Obrigatorio
        # O destino (central) é acordado fora do sistema; o parceiro aceita pelo id_sequencia.
        resultado = client.service.CriarSolicitacaoEspelhamentoReverso(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            Placa=placa,
            data_expiracao=data_expiracao,
            Espelhamento_Obrigatorio=obrigatorio,
        )
        logger.info(f"Omnilink CriarSolicitacaoEspelhamentoReverso({placa}): {resultado}")
        xml_r = re.sub(r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
                       lambda m: f'<{m.group(1)}{m.group(2).lower()}', str(resultado))
        try:
            root = ET.fromstring(f'<root>{xml_r}</root>')
            id_seq = root.findtext('idsequencia') or root.findtext('id') or ''
            conf   = root.findtext('confirmacao') or str(resultado)
        except Exception:
            id_seq, conf = '', str(resultado)
        return {'ok': True, 'id_sequencia': id_seq, 'mensagem': conf, 'metodo': 'CriarSolicitacaoEspelhamentoReverso'}

    except Exception as e:
        logger.error(f"Omnilink criar_espelhamento({placa}): {e}")
        return {'ok': False, 'id_sequencia': '', 'mensagem': str(e)}


def aceitar_espelhamento(id_solicitacao: int, aceitar: bool = True) -> dict:
    """
    Aceita (aceitar=True) ou rejeita (aceitar=False) uma solicitação recebida.
    StatusAceite: 1=aceito  2=rejeitado
    """
    try:
        client = _get_client()
        resultado = client.service.AceiteDeEspelhamentoReverso(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            IdSolicitacao=int(id_solicitacao),
            StatusAceite=1 if aceitar else 2,
        )
        logger.info(f"Omnilink AceiteEspelhamento({id_solicitacao}, aceitar={aceitar}): {resultado}")
        return {'ok': True, 'mensagem': str(resultado)}
    except Exception as e:
        logger.error(f"Omnilink aceitar_espelhamento({id_solicitacao}): {e}")
        return {'ok': False, 'mensagem': str(e)}


def excluir_espelhamento(id_solicitacao: int) -> dict:
    """Exclui/cancela um espelhamento pelo IdSolicitacao."""
    try:
        client = _get_client()
        resultado = client.service.ExcluirSolicitacaoEspelhamentoReverso(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            IdSolicitacao=int(id_solicitacao),
        )
        logger.info(f"Omnilink ExcluirEspelhamento({id_solicitacao}): {resultado}")
        return {'ok': True, 'mensagem': str(resultado)}
    except Exception as e:
        logger.error(f"Omnilink excluir_espelhamento({id_solicitacao}): {e}")
        return {'ok': False, 'mensagem': str(e)}


def listar_centrais_disponiveis() -> list[dict]:
    """
    Lista as centrais/bases disponíveis para espelhamento.
    Tenta múltiplos nomes de método WSDL; fallback: fixture local JSON.
    """
    cache_key = 'omnilink_centrais_v1'
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        client = _get_client()
        for nome in ('ListarCentraisDisponiveis', 'ListarBases', 'ListarCentrais',
                     'GetCentrais', 'BuscarCentrais', 'ListarBasesParceiras',
                     'ListarCentraisOmnilink', 'ListarClientes', 'GetBases',
                     'BuscarBases', 'ListarEmpresas', 'GetEmpresas'):
            op = getattr(client.service, nome, None)
            if op is None:
                continue
            try:
                xml_str = op(Usuario=USUARIO, Senha=SENHA_MD5)
                xml_low = re.sub(r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
                                 lambda m: f'<{m.group(1)}{m.group(2).lower()}', str(xml_str))
                root = ET.fromstring(f'<root>{xml_low}</root>')
                centrais = []
                for el in root.iter():
                    id_c  = el.findtext('id') or el.findtext('idcentral') or ''
                    nome_c = el.findtext('nome') or el.findtext('descricao') or ''
                    if id_c and nome_c:
                        centrais.append({'id': id_c, 'nome': nome_c})
                if centrais:
                    cache.set(cache_key, centrais, 3600)
                    logger.info(f"Omnilink {nome}: {len(centrais)} centrais")
                    return centrais
            except Exception as e_inner:
                logger.debug(f"Omnilink {nome}: {e_inner}")
                continue

        logger.warning("Omnilink listar_centrais: nenhum método WSDL encontrou resultados — usando fixture local")
        return _carregar_centrais_fixture()
    except Exception as e:
        logger.error(f"Omnilink listar_centrais: {e}")
        return _carregar_centrais_fixture()


def _carregar_centrais_fixture() -> list[dict]:
    """
    Carrega lista de centrais do arquivo JSON local (fixture extraída do AMNLink).
    A Omnilink não expõe esse dado no WSDL — o portal embeds como variável JS.
    """
    import json as _json
    import pathlib
    fixture = pathlib.Path(__file__).parent / 'fixtures' / 'centrais_omnilink.json'
    try:
        with open(fixture, encoding='utf-8') as f:
            data = _json.load(f)
        logger.info(f"Omnilink centrais fixture: {len(data)} entradas carregadas")
        return data
    except Exception as e:
        logger.error(f"Omnilink _carregar_centrais_fixture: {e}")
        return _extrair_centrais_dos_espelhamentos()


def _extrair_centrais_dos_espelhamentos() -> list[dict]:
    """Fallback final: extrai centrais únicas dos espelhamentos existentes."""
    cache_key = 'omnilink_centrais_fallback_v1'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        espelhamentos = listar_espelhamentos()
        vistas = {}
        for e in espelhamentos:
            id_c   = e.get('id_central') or e.get('id_cliente_destino') or ''
            nome_c = e.get('nome_central') or e.get('cnpj_central') or ''
            if nome_c and id_c and id_c not in vistas:
                vistas[id_c] = nome_c
        centrais = [{'id': k, 'nome': v} for k, v in sorted(vistas.items(), key=lambda x: x[1])]
        if centrais:
            cache.set(cache_key, centrais, 1800)
        return centrais
    except Exception as e:
        logger.error(f"Omnilink _extrair_centrais_dos_espelhamentos: {e}")
        return []


def descobrir_metodos_wsdl() -> list[str]:
    """Retorna lista completa de métodos disponíveis no WSDL (diagnóstico)."""
    try:
        client = _get_client()
        return sorted(client.service._operations)
    except Exception as e:
        return [f"ERRO: {e}"]

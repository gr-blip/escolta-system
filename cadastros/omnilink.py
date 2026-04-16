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
        id_terminal = _mct_id_to_terminal(mct_id)
        id_terminal_str = str(id_terminal)

        ids = _buscar_ultimo_id_post()
        # Lookback de 20M IDs ≈ ~4-5 dias na plataforma global Omnilink.
        # UltimoSequencial=0 é inválido (-204); mínimo aceitável é 1.
        ultimo_seq = max(1, ids['id'] - 20_000_000)

        client = _get_client()
        xml_str = client.service.ObtemEventosNormais(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            UltimoSequencial=ultimo_seq,
        )

        eventos = _parse_teleeventos_xml(str(xml_str) if xml_str else '')

        # Filtra pelo veículo correto
        eventos_veiculo = [
            e for e in eventos
            if e.get('id_terminal') == id_terminal_str
        ]

        if not eventos_veiculo:
            logger.info(f"Omnilink: nenhuma posição recente para IdTerminal={id_terminal} (MCT={mct_id})")
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
        id_terminal = _mct_id_to_terminal(mct_id)
        id_terminal_str = str(id_terminal)

        # Remove timezone de inicio/fim — datetimes da API são sempre naive.
        # Se o Django armazenar com tz (USE_TZ=True), a comparação lançaria TypeError.
        def _naive(dt):
            return dt.replace(tzinfo=None) if getattr(dt, 'tzinfo', None) else dt

        inicio_n = _naive(inicio)
        fim_n    = _naive(fim)

        # Obtém o ID atual para calcular lookback histórico.
        # A plataforma Omnilink é global (~3-5M eventos/dia totais).
        # Para cobrir 7 dias = ~35M IDs. Usamos 100M para ter margem.
        ids = _buscar_ultimo_id_post()
        lookback = max(1, ids['id'] - 100_000_000)

        client = _get_client()
        xml_str = client.service.ObtemEventosNormais(
            Usuario=USUARIO,
            Senha=SENHA_MD5,
            UltimoSequencial=lookback,
        )

        todos_eventos = _parse_teleeventos_xml(str(xml_str) if xml_str else '')
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

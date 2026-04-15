"""
Integração com API Omnilink (SOAP/WSDL)
Documentação: https://wstt.omnilink.com.br/iasws/iasws.asmx?WSDL
"""
import logging
from datetime import datetime, timedelta
from functools import lru_cache
from django.core.cache import cache

logger = logging.getLogger(__name__)

URL_WSDL  = "https://wstt.omnilink.com.br/iasws/iasws.asmx?WSDL"
USUARIO   = "administrativo@grupojrservicos.com.br"
SENHA_MD5 = "89db6cb87ca3be0c05de956144235fac"

# Cache de 30 segundos para posição atual (evita spam na API)
CACHE_POSICAO_TTL  = 30
# Cache de 5 minutos para histórico
CACHE_HISTORICO_TTL = 300


def _get_client():
    """Retorna cliente SOAP zeep (lazy init)."""
    try:
        from zeep import Client
        from zeep.transports import Transport
        import requests

        session = requests.Session()
        session.verify = True
        transport = Transport(session=session, operation_timeout=10)
        return Client(URL_WSDL, transport=transport)
    except ImportError:
        raise RuntimeError("zeep não instalado. Rode: pip install zeep")
    except Exception as e:
        raise RuntimeError(f"Erro ao conectar à API Omnilink: {e}")


def get_ultima_posicao(mct_id: str) -> dict:
    """
    Busca a última posição conhecida do veículo pelo MCT ID.

    Retorna dict com:
        lat, lng, velocidade, odometro, ignicao, data_hora, endereco
    ou None em caso de erro.
    """
    cache_key = f"omnilink_pos_{mct_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        client = _get_client()

        # Tenta variantes comuns do método Omnilink
        result = None
        metodos = [
            "ObterUltimaPosicaoVeiculo",
            "BuscarUltimaPosicao",
            "ObterUltimaPosicao",
            "GetLastPosition",
        ]
        for metodo in metodos:
            try:
                fn = getattr(client.service, metodo)
                result = fn(
                    usuario=USUARIO,
                    senha=SENHA_MD5,
                    identificacao=mct_id,
                )
                break
            except Exception:
                continue

        if result is None:
            logger.warning(f"Omnilink: nenhum método funcionou para mct_id={mct_id}")
            return None

        data = _parse_posicao(result)
        cache.set(cache_key, data, CACHE_POSICAO_TTL)
        return data

    except Exception as e:
        logger.error(f"Omnilink get_ultima_posicao erro: {e}")
        return None


def get_historico_posicoes(mct_id: str, inicio: datetime, fim: datetime) -> list:
    """
    Busca histórico de posições do veículo no intervalo de datas.

    Retorna lista de dicts com: lat, lng, velocidade, data_hora
    """
    cache_key = f"omnilink_hist_{mct_id}_{inicio.strftime('%Y%m%d%H%M')}_{fim.strftime('%Y%m%d%H%M')}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        client = _get_client()

        result = None
        metodos = [
            "ObterHistoricoPosicoes",
            "BuscarHistoricoPosicoes",
            "ObterPosicoes",
            "GetPositions",
        ]
        for metodo in metodos:
            try:
                fn = getattr(client.service, metodo)
                result = fn(
                    usuario=USUARIO,
                    senha=SENHA_MD5,
                    identificacao=mct_id,
                    dataInicio=inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                    dataFim=fim.strftime("%Y-%m-%dT%H:%M:%S"),
                )
                break
            except Exception:
                continue

        if result is None:
            return []

        pontos = _parse_historico(result)
        cache.set(cache_key, pontos, CACHE_HISTORICO_TTL)
        return pontos

    except Exception as e:
        logger.error(f"Omnilink get_historico_posicoes erro: {e}")
        return []


def get_historico_operacao(os_obj) -> list:
    """
    Atalho: busca histórico para o período da OS (inicio_viagem → termino_viagem).
    """
    op = getattr(os_obj, 'operacional', None)
    if not op:
        return []

    viatura = (os_obj.equipe.viatura if os_obj.equipe else None)
    mct_id  = viatura.mct_id if viatura and viatura.mct_id else None
    if not mct_id:
        return []

    inicio = op.inicio_viagem or op.chegada_operacao
    fim    = op.termino_viagem or op.termino_operacao or datetime.now()

    if not inicio:
        return []

    return get_historico_posicoes(mct_id, inicio, fim)


# ── Parsers (adaptam ao formato real retornado pela API) ─────────────────────

def _parse_posicao(result) -> dict:
    """
    Normaliza o objeto retornado pela API para um dict padronizado.
    Adapta automaticamente a nomes de campo comuns na API Omnilink.
    """
    def _get(obj, *keys):
        for k in keys:
            v = getattr(obj, k, None)
            if v is None and isinstance(obj, dict):
                v = obj.get(k)
            if v is not None:
                return v
        return None

    try:
        lat = float(_get(result, 'latitude', 'Latitude', 'lat') or 0)
        lng = float(_get(result, 'longitude', 'Longitude', 'lng', 'lon') or 0)
        vel = float(_get(result, 'velocidade', 'Velocidade', 'speed', 'Speed') or 0)
        odo = float(_get(result, 'odometro', 'Odometro', 'hodometro', 'odometer') or 0)
        ign = bool(_get(result, 'ignicao', 'Ignicao', 'ignition'))
        dth = _get(result, 'dataHora', 'DataHora', 'data_hora', 'dateTime', 'DateTime')
        end = _get(result, 'endereco', 'Endereco', 'address', 'logradouro') or ''

        return {
            'lat': lat,
            'lng': lng,
            'velocidade': vel,
            'odometro': round(odo, 1),
            'ignicao': ign,
            'data_hora': str(dth) if dth else '',
            'endereco': str(end),
        }
    except Exception as e:
        logger.error(f"Omnilink _parse_posicao erro: {e}")
        return {}


def _parse_historico(result) -> list:
    """
    Normaliza lista de posições retornada pelo histórico.
    """
    pontos = []
    try:
        # A API pode retornar uma lista ou um objeto wrapper
        items = result
        if hasattr(result, 'Posicao'):
            items = result.Posicao
        elif hasattr(result, 'posicao'):
            items = result.posicao
        elif hasattr(result, 'item'):
            items = result.item
        elif not hasattr(result, '__iter__'):
            items = [result]

        for item in (items or []):
            p = _parse_posicao(item)
            if p.get('lat') and p.get('lng'):
                pontos.append(p)
    except Exception as e:
        logger.error(f"Omnilink _parse_historico erro: {e}")

    return pontos

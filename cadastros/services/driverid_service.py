"""
cadastros/services/driverid_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Integração com API DriverID — consulta de processos judiciais por CPF.

Fluxo:
  0. POST /sessions (login) → obtém JWT
  1. POST /documentCriminals  →  retorna transactionId
  2. Polling GET /documentCriminals/findByTransactionId/{id}  →  resultado resumido
  3. GET /documentCriminals/process/findByTransactionId/{id}  →  processos detalhados

Autenticação: Session-based (email + password → JWT com expiração)
"""
import base64
import json
import logging
import time
from datetime import datetime, timezone as tz

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BASE_URL = settings.DRIVERID_API_URL

# ─── Cache do token JWT ──────────────────────────────────────────────────────
_token_cache = {
    'token': None,
    'expires_at': 0,  # epoch timestamp
}


class DriverIDError(Exception):
    """Erro genérico da API DriverID."""


class DriverIDTimeout(DriverIDError):
    """Consulta não retornou resultado no tempo esperado."""


def _decode_jwt_exp(token: str) -> float:
    """Decodifica o payload do JWT (sem verificar assinatura) para obter exp."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return 0
        payload = parts[1] + '=='  # padding para base64
        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        return float(data.get('exp', 0))
    except Exception:
        return 0


def _login() -> str:
    """
    POST /sessions com email/password.
    Retorna o JWT token e atualiza o cache.
    """
    email = settings.DRIVERID_EMAIL
    password = settings.DRIVERID_PASSWORD

    if not email or not password:
        raise DriverIDError(
            'Credenciais DriverID não configuradas. '
            'Defina DRIVERID_EMAIL e DRIVERID_PASSWORD nas variáveis de ambiente.'
        )

    resp = requests.post(
        f'{BASE_URL}/sessions',
        json={'email': email, 'password': password},
        headers={'Content-Type': 'application/json'},
        timeout=30,
    )

    if resp.status_code == 401:
        raise DriverIDError('Credenciais DriverID inválidas (email ou password incorretos).')

    resp.raise_for_status()
    data = resp.json()

    token = data.get('data', {}).get('token', '')
    if not token:
        raise DriverIDError(f'Login DriverID não retornou token. Resposta: {data}')

    # Cacheia o token com margem de segurança de 5 minutos antes da expiração
    exp = _decode_jwt_exp(token)
    _token_cache['token'] = token
    _token_cache['expires_at'] = exp - 300 if exp > 0 else time.time() + 3600  # fallback: 1h

    logger.info('DriverID: login realizado com sucesso')
    return token


def _get_token() -> str:
    """
    Retorna o token JWT válido (do cache ou faz login).
    """
    now = time.time()
    if _token_cache['token'] and _token_cache['expires_at'] > now:
        return _token_cache['token']
    return _login()


def _headers() -> dict:
    """Headers com Bearer token atualizado."""
    token = _get_token()
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type':  'application/json',
    }


def _request_with_reauth(method: str, url: str, **kwargs) -> requests.Response:
    """
    Faz uma requisição HTTP. Se receber 401, faz login novamente e repete.
    """
    kwargs.setdefault('headers', _headers())
    kwargs.setdefault('timeout', 30)

    resp = requests.request(method, url, **kwargs)

    if resp.status_code == 401:
        logger.warning('DriverID: token expirado, fazendo login novamente...')
        _token_cache['token'] = None  # força novo login
        kwargs['headers'] = _headers()
        resp = requests.request(method, url, **kwargs)

    resp.raise_for_status()
    return resp


# ─── Passo 1: submeter CPF ───────────────────────────────────────────────────

def _post_consulta(cpf_limpo: str) -> str:
    """
    POST /documentCriminals
    Retorna o transactionId.
    """
    resp = _request_with_reauth(
        'POST',
        f'{BASE_URL}/documentCriminals',
        json={'document': cpf_limpo},
    )
    data = resp.json()
    if data.get('statusCode') != 200:
        raise DriverIDError(data.get('message', 'Erro desconhecido'))
    tx_id = data.get('data', {}).get('transactionId', '')
    if not tx_id:
        raise DriverIDError('Nenhum transactionId retornado')
    return tx_id


# ─── Passo 2: polling do resultado ────────────────────────────────────────────

def _poll_resultado(tx_id: str, tentativas: int = 5, espera: int = 10) -> dict:
    """
    GET /documentCriminals/findByTransactionId/{txId}
    Faz polling até o resultado estar pronto.
    Status: 3=processando, 144=aprovado, 145=alerta, 146=erro
    """
    url = f'{BASE_URL}/documentCriminals/findByTransactionId/{tx_id}'
    for tentativa in range(tentativas):
        resp = _request_with_reauth('GET', url)
        data = resp.json()

        status_code = data.get('data', {}).get('status', {}).get('code')
        if status_code and status_code != 3:  # 3 = processando
            return data['data']

        logger.info(f'Polling {tx_id}: tentativa {tentativa + 1}/{tentativas} — aguardando...')
        time.sleep(espera)

    raise DriverIDTimeout(f'Consulta {tx_id} não retornou após {tentativas * espera}s')


# ─── Passo 3: processos detalhados ────────────────────────────────────────────

def _get_processos_detalhados(tx_id: str) -> list:
    """
    GET /documentCriminals/process/findByTransactionId/{txId}
    Retorna lista de processos com partes, assuntos, valores, etc.
    """
    url = f'{BASE_URL}/documentCriminals/process/findByTransactionId/{tx_id}'
    resp = _request_with_reauth('GET', url)
    data = resp.json()
    if data.get('statusCode') != 200:
        raise DriverIDError(data.get('message', 'Erro ao buscar processos'))
    return data.get('data', {}).get('data', [])


# ─── Função pública ───────────────────────────────────────────────────────────

def consultar_cpf(cpf: str) -> dict:
    """
    Consulta CPF na API DriverID e retorna dict normalizado:

    {
        'cpf': str,
        'nome': str,
        'status_cpf': str,
        'total_processos': int,
        'processos': list,
        'resultado_completo': dict,
        'transaction_id': str,
    }

    Raises DriverIDError, DriverIDTimeout, requests.HTTPError.
    """
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    if len(cpf_limpo) != 11:
        raise DriverIDError(f'CPF inválido: {cpf}')

    logger.info(f'DriverID: submetendo CPF {cpf_limpo[:3]}***{cpf_limpo[-2:]}')
    tx_id = _post_consulta(cpf_limpo)

    logger.info(f'DriverID: transactionId={tx_id}, aguardando resultado...')
    resultado = _poll_resultado(tx_id)

    status_info = resultado.get('status', {})
    result_data = resultado.get('result', {})

    processos_basicos = result_data.get('processos', [])
    total = len(processos_basicos)

    # Buscar processos detalhados
    processos_detalhados = []
    try:
        processos_detalhados = _get_processos_detalhados(tx_id)
        logger.info(f'DriverID: {len(processos_detalhados)} processos detalhados obtidos')
    except Exception as e:
        logger.warning(f'DriverID: falha ao obter processos detalhados: {e}')
        processos_detalhados = processos_basicos

    return {
        'cpf':               cpf_limpo,
        'nome':              result_data.get('name', ''),
        'status_cpf':        result_data.get('documentStatusMessage', result_data.get('documentStatus', '')),
        'total_processos':   len(processos_detalhados),
        'processos':         processos_detalhados,
        'resultado_completo': resultado,
        'transaction_id':    tx_id,
    }

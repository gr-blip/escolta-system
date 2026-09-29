"""Context processors do app cadastros."""


def solicitacoes_pendentes(request):
    """Contador na sidebar. Falha de banco nao pode derrubar TODA tela do
    sistema por causa de um badge."""
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}
    try:
        from .solicitacoes import pendentes
        return {'solicitacoes_pendentes': pendentes()}
    except Exception:
        return {}

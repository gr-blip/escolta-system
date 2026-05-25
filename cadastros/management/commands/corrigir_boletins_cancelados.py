from django.core.management.base import BaseCommand
from cadastros.models import BoletimMedicao


class Command(BaseCommand):
    help = 'Corrige status de boletins de OS canceladas'

    def handle(self, *args, **options):
        boletins_errados = BoletimMedicao.objects.filter(
            os__status='cancelada'
        ).exclude(status='cancelado')

        count = boletins_errados.count()
        self.stdout.write(f'Encontrados {count} boletins para corrigir')

        if count > 0:
            for b in boletins_errados:
                b.status = 'cancelado'
                b.save()
                self.stdout.write(f'  Corrigido: OS-{b.os.numero}')

            self.stdout.write(self.style.SUCCESS(f'Corrigidos {count} boletins'))
        else:
            self.stdout.write('Nenhum boletim para corrigir')

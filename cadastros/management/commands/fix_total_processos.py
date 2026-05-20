"""
Management command: fix_total_processos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Atualiza total_processos de ConsultaProcessos existentes
baseado no resultado_json (processos detalhados).
"""
from django.core.management.base import BaseCommand
from cadastros.models import ConsultaProcesso


class Command(BaseCommand):
    help = 'Corrige total_processos de consultas existentes baseado no resultado_json'

    def handle(self, *args, **options):
        consultas = ConsultaProcesso.objects.all()
        updated = 0

        for c in consultas:
            data = c.resultado_json or {}
            processos = data.get('data', {}).get('data', [])
            real_total = len(processos)

            if c.total_processos != real_total:
                self.stdout.write(
                    f'  CPF {c.cpf}: {c.total_processos} → {real_total}'
                )
                c.total_processos = real_total
                c.save(update_fields=['total_processos'])
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Concluído: {updated} registro(s) atualizado(s)'
        ))

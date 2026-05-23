"""
cadastros/management/commands/consultar_processos.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Management command para consulta periódica de processos judiciais via DriverID.

Executa via cron a cada 2 meses:
  python manage.py consultar_processos

Busca agentes patrimoniais ativos com última consulta > 60 dias (ou sem consulta),
chama a API DriverID, salva o resultado e gera PDF.
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone

from cadastros.models import FuncionarioPatrimonial, ConsultaProcesso
from cadastros.services.driverid_service import consultar_cpf, DriverIDError
from cadastros.pdf_processo import gerar_pdf_consulta

logger = logging.getLogger(__name__)

DIAS_RECONSULTA = 60


class Command(BaseCommand):
    help = 'Consulta processos judiciais de agentes patrimoniais via DriverID (cron a cada 2 meses)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força consulta de TODOS os agentes, ignorando o intervalo de 60 dias.',
        )
        parser.add_argument(
            '--cpf',
            type=str,
            help='Consulta apenas um CPF específico.',
        )

    def handle(self, *args, **options):
        agora = timezone.now()
        limite = agora - timedelta(days=DIAS_RECONSULTA)

        if options['cpf']:
            funcionarios = FuncionarioPatrimonial.objects.filter(
                cpf__contains=options['cpf'].replace('.', '').replace('-', '')
            )
            self.stdout.write(f'Modo CPF único: {funcionarios.count()} agente(s) encontrado(s)')
        elif options['force']:
            funcionarios = FuncionarioPatrimonial.objects.filter(status='ativo')
            self.stdout.write(f'Modo FORCE: consultando TODOS os {funcionarios.count()} agentes ativos')
        else:
            # Agentes ativos sem consulta ou com última consulta > 60 dias
            funcionarios = FuncionarioPatrimonial.objects.filter(status='ativo').exclude(
                consultas_processo__criado_em__gte=limite
            )
            self.stdout.write(f'Agentes ativos sem consulta recente (>{DIAS_RECONSULTA} dias): {funcionarios.count()}')

        if not funcionarios.exists():
            self.stdout.write(self.style.WARNING('Nenhum agente para consultar.'))
            return

        total = funcionarios.count()
        sucesso = 0
        erro = 0

        for i, func in enumerate(funcionarios, 1):
            self.stdout.write(f'[{i}/{total}] Consultando {func.nome} (CPF {func.cpf[:3]}***{func.cpf[-2:]})...')

            try:
                resultado = consultar_cpf(func.cpf)

                consulta = ConsultaProcesso.objects.create(
                    funcionario=func,
                    cpf=resultado['cpf'],
                    nome_retornado=resultado['nome'],
                    status_cpf=resultado['status_cpf'],
                    total_processos=resultado['total_processos'],
                    resultado_json={'data': {
                        'data': resultado['processos'],
                        'result': {
                            'name': resultado['nome'],
                            'documentStatusMessage': resultado['status_cpf'],
                        },
                    }},
                    transaction_id=resultado['transaction_id'],
                    origem='auto_agendado',
                )

                # Gerar PDF
                try:
                    pdf_buf = gerar_pdf_consulta(consulta)
                    consulta.pdf_file.save(
                        f'consulta_{func.cpf}_{consulta.criado_em:%Y%m%d_%H%M}.pdf',
                        ContentFile(pdf_buf.read()),
                        save=True,
                    )
                except Exception as e:
                    logger.warning(f'Falha ao gerar PDF para {func.cpf}: {e}')

                status_msg = resultado['status_cpf']
                proc_count = resultado['total_processos']
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ {status_msg} — {proc_count} processo(s)'
                ))
                sucesso += 1

            except DriverIDError as e:
                self.stderr.write(self.style.ERROR(f'  ✗ Erro DriverID: {e}'))
                erro += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ✗ Erro inesperado: {e}'))
                erro += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Concluído: {sucesso} sucesso(s), {erro} erro(s), {total} total'
        ))

# -*- coding: utf-8 -*-
"""
Management command para importar funcionários JRS Facilities a partir de Excel.

Uso:
    python manage.py importar_jrs_facilities
    python manage.py importar_jrs_facilities --arquivo caminho/para/arquivo.xlsx
"""

from datetime import datetime
from django.core.management.base import BaseCommand
from cadastros.models import FuncionarioPatrimonial

try:
    import openpyxl
except ImportError:
    openpyxl = None


class Command(BaseCommand):
    help = 'Importa funcionários JRS Facilities Ltda a partir do Excel EFETIVO - JRS.xlsx'

    def add_arguments(self, parser):
        parser.add_argument(
            '--arquivo',
            type=str,
            default=r'C:\Users\wilke\Downloads\EFETIVO - JRS.xlsx',
            help='Caminho do arquivo Excel (padrão: C:\\Users\\wilke\\Downloads\\EFETIVO - JRS.xlsx)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Apenas mostra o que seria importado, sem salvar.',
        )

    def handle(self, *args, **options):
        if openpyxl is None:
            self.stderr.write(self.style.ERROR('openpyxl não instalado. Rode: pip install openpyxl'))
            return

        arquivo = options['arquivo']
        dry_run = options['dry_run']

        self.stdout.write(self.style.NOTICE(f'Lendo: {arquivo}'))

        wb = openpyxl.load_workbook(arquivo, data_only=True)
        ws = wb.active

        importados = 0
        pulados = 0
        erros = 0

        # Dados começam na linha 6 (linhas 1-5 são cabeçalho)
        for row_num in range(6, ws.max_row + 1):
            empresa_val = ws.cell(row=row_num, column=1).value  # Empresa
            cpf_raw     = ws.cell(row=row_num, column=2).value  # CPF
            nome_raw    = ws.cell(row=row_num, column=3).value  # Nome
            nasc_raw    = ws.cell(row=row_num, column=4).value  # Data de Nascimento
            cargo_raw   = ws.cell(row=row_num, column=5).value  # Cargo
            mae_raw     = ws.cell(row=row_num, column=6).value  # Nome da Mãe

            # Pular linhas vazias
            if not cpf_raw:
                continue

            # Limpar CPF (remover pontuação)
            cpf_limpo = str(cpf_raw).strip()
            cpf_formatado = cpf_limpo.replace('.', '').replace('-', '').replace('/', '')
            # Formatar como XXX.XXX.XXX-XX
            if len(cpf_formatado) == 11:
                cpf_formatado = f'{cpf_formatado[:3]}.{cpf_formatado[3:6]}.{cpf_formatado[6:9]}-{cpf_formatado[9:]}'

            nome = str(nome_raw).strip() if nome_raw else ''
            cargo = str(cargo_raw).strip() if cargo_raw else ''
            nome_mae = str(mae_raw).strip() if mae_raw else ''

            # Parsear data de nascimento
            data_nascimento = None
            if nasc_raw:
                if isinstance(nasc_raw, datetime):
                    data_nascimento = nasc_raw.date()
                else:
                    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
                        try:
                            data_nascimento = datetime.strptime(str(nasc_raw).strip(), fmt).date()
                            break
                        except ValueError:
                            continue

            if not nome:
                self.stdout.write(self.style.WARNING(f'  Linha {row_num}: sem nome, pulando'))
                pulados += 1
                continue

            # Verificar se CPF já existe
            if FuncionarioPatrimonial.objects.filter(cpf=cpf_formatado).exists():
                self.stdout.write(self.style.WARNING(f'  CPF {cpf_formatado} já existe ({nome}), pulando'))
                pulados += 1
                continue

            if dry_run:
                self.stdout.write(f'  [DRY-RUN] {nome} | CPF: {cpf_formatado} | Cargo: {cargo} | Mãe: {nome_mae}')
                importados += 1
                continue

            FuncionarioPatrimonial.objects.create(
                empresa='jrs_facilities',
                nome=nome,
                cpf=cpf_formatado,
                cargo=cargo,
                nome_mae=nome_mae,
                data_nascimento=data_nascimento,
                status='ativo',
            )
            importados += 1

        if dry_run:
            self.stdout.write(self.style.NOTICE(
                f'\n[DRY-RUN] {importados} seriam importados, {pulados} pulados.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\nImportação concluída: {importados} importados, {pulados} pulados, {erros} erros.'
            ))

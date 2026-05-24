# -*- coding: utf-8 -*-
"""
Management command para importar funcionários Freelance.

Uso:
    python manage.py importar_freelance
    python manage.py importar_freelance --dry-run
"""

from django.core.management.base import BaseCommand
from cadastros.models import FuncionarioPatrimonial


FREELANCE_DATA = [
    {'cpf': '044.182.431-51', 'nome': 'AIRTON MARROES SILVA COSTA',            'cargo': 'BRIGADISTA',                  'mae': 'MARIA DALVA LIMA E SILVA COSTA'},
    {'cpf': '072.881.951-12', 'nome': 'ALESSANDRO DE SOUZA MOREIRA',           'cargo': 'AGENTE PATRIMONIAL',          'mae': 'DJANE MARIA DE SOUZA MOREIRA'},
    {'cpf': '018.568.221-92', 'nome': 'HEGLISSON LIMA DE OLIVEIRA',            'cargo': 'BRIGADISTA',                  'mae': 'PAULA FRASSINETE LIMA DE OLIVEIRA'},
    {'cpf': '659.494.121-68', 'nome': 'HOSANA PEREIRA DOS SANTOS',             'cargo': 'BRIGADISTA',                  'mae': 'HOSANA ROSA PEREIRA'},
    {'cpf': '079.534.941-67', 'nome': 'JAQUELINE ALCENA DOS SANTOS',           'cargo': 'BRIGADISTA',                  'mae': 'TEREZA ALCENA DOS SANTOS'},
    {'cpf': '053.353.553-01', 'nome': 'LEANDRO DA SILVA FERNANDES',            'cargo': 'BRIGADISTA',                  'mae': 'IRACEMA DA SILVA FERNANDES'},
    {'cpf': '973.459.111-87', 'nome': 'LUCAS VIEIRA RODRIGUES',                'cargo': 'VIGILANTE',                   'mae': 'GUILHERMINA VIEIRA RODRIGUES'},
    {'cpf': '077.467.051-70', 'nome': 'LUIZ FELIPE DOS SANTOS SILVA',          'cargo': 'AUXILIAR DE SERVICOS GERAIS', 'mae': 'TAMARA RAFAELA ALVES DOS SANTOS'},
    {'cpf': '058.551.631-64', 'nome': 'PALOMA DE PADUA DOS SANTOS OLIVEIRA',   'cargo': 'AUXILIAR DE SERVICOS GERAIS', 'mae': 'MADALENA OLIVEIRA PEREIRA'},
    {'cpf': '692.221.931-72', 'nome': 'THAIS SANTOS MEDEIROS',                 'cargo': 'BRIGADISTA',                  'mae': 'SOLANGE DA SILVA SANTOS'},
    {'cpf': '797.861.891-91', 'nome': 'VALDELINO GONCALVES DO CARMO',          'cargo': 'AGENTE PATRIMONIAL',          'mae': 'VALDOMIRA ROMEIRA DO CARMO'},
    {'cpf': '012.289.471-55', 'nome': 'VANESSA DA SILVA GUIMARAES',            'cargo': 'AUXILIAR DE SERVICOS GERAIS', 'mae': 'VERA LUCIA FRANCISCA DA SILVA'},
    {'cpf': '599.122.431-53', 'nome': 'WANDERLON PIMENTA VITOR',               'cargo': 'BRIGADISTA',                  'mae': 'ILZARA PEREIRA DA SILVA PIMENTA'},
]


class Command(BaseCommand):
    help = 'Importa funcionarios Freelance (tabela hardcoded)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Apenas mostra o que seria importado, sem salvar.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        importados = 0
        pulados = 0

        for row in FREELANCE_DATA:
            cpf = row['cpf']
            nome = row['nome']

            if FuncionarioPatrimonial.objects.filter(cpf=cpf).exists():
                self.stdout.write(self.style.WARNING(f'  CPF {cpf} ja existe ({nome}), pulando'))
                pulados += 1
                continue

            if dry_run:
                self.stdout.write(f'  [DRY-RUN] {nome} | CPF: {cpf} | Cargo: {row["cargo"]}')
                importados += 1
                continue

            FuncionarioPatrimonial.objects.create(
                empresa='freelance',
                nome=nome,
                cpf=cpf,
                cargo=row['cargo'],
                nome_mae=row['mae'],
                status='ativo',
            )
            importados += 1
            self.stdout.write(f'  + {nome}')

        if dry_run:
            self.stdout.write(self.style.NOTICE(f'\n[DRY-RUN] {importados} seriam importados, {pulados} pulados.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\nImportacao concluida: {importados} importados, {pulados} pulados.'))

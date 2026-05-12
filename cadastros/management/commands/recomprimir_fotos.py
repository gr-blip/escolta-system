"""
Management command para recomprimir fotos existentes no sistema.

Uso:
    python manage.py recomprimir_fotos           # processa tudo
    python manage.py recomprimir_fotos --dry-run  # apenas mostra o que seria feito
    python manage.py recomprimir_fotos --limite 100  # processa no máximo 100 fotos

O comando percorre todos os models de foto (FotoMarco, FotoParada, FotoIncidente,
FotoVeiculoEscoltado, FotoTrocaMotorista), recomprime cada imagem para
JPEG 1280px largura máxima / qualidade 72, e substitui o arquivo no disco.
Fotos já pequenas (< 200KB) são ignoradas automaticamente.
"""

import io
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ExifTags

from cadastros.models import (
    FotoMarco,
    FotoParada,
    FotoIncidente,
    FotoVeiculoEscoltado,
    FotoTrocaMotorista,
)


MAX_LARGURA = 1280
QUALIDADE = 72
LIMITE_SKIP_KB = 200  # arquivos menores que isso já estão ok, pula


MODELOS = [
    ('FotoMarco',           FotoMarco),
    ('FotoParada',          FotoParada),
    ('FotoIncidente',       FotoIncidente),
    ('FotoVeiculoEscoltado', FotoVeiculoEscoltado),
    ('FotoTrocaMotorista',  FotoTrocaMotorista),
]


def _corrigir_orientacao(img):
    try:
        exif = img._getexif()
        if exif:
            for tag, val in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    if val == 3:
                        img = img.rotate(180, expand=True)
                    elif val == 6:
                        img = img.rotate(270, expand=True)
                    elif val == 8:
                        img = img.rotate(90, expand=True)
                    break
    except Exception:
        pass
    return img


def _recomprimir_arquivo(caminho_absoluto, dry_run=False):
    """
    Recomprime um arquivo de imagem no disco.
    Retorna (antes_kb, depois_kb, novo_caminho) ou None se ignorado/erro.
    """
    if not os.path.exists(caminho_absoluto):
        return None

    tamanho_antes = os.path.getsize(caminho_absoluto) // 1024  # KB

    if tamanho_antes < LIMITE_SKIP_KB:
        return None  # já pequeno

    if dry_run:
        return (tamanho_antes, None, caminho_absoluto)

    try:
        with Image.open(caminho_absoluto) as img:
            img = _corrigir_orientacao(img)
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            if img.width > MAX_LARGURA:
                ratio = MAX_LARGURA / img.width
                img = img.resize((MAX_LARGURA, int(img.height * ratio)), Image.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=QUALIDADE, optimize=True)
            buffer.seek(0)

        novo_caminho = os.path.splitext(caminho_absoluto)[0] + '.jpg'
        with open(novo_caminho, 'wb') as f:
            f.write(buffer.read())

        if novo_caminho != caminho_absoluto:
            os.remove(caminho_absoluto)

        tamanho_depois = os.path.getsize(novo_caminho) // 1024
        return (tamanho_antes, tamanho_depois, novo_caminho)

    except Exception as e:
        return None


class Command(BaseCommand):
    help = 'Recomprime todas as fotos existentes para JPEG 1280px / qualidade 72'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra quantas fotos seriam processadas sem alterar nada',
        )
        parser.add_argument(
            '--limite',
            type=int,
            default=0,
            help='Número máximo de fotos a processar (0 = sem limite)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limite = options['limite']

        if dry_run:
            self.stdout.write(self.style.WARNING('Modo DRY-RUN — nenhum arquivo será alterado\n'))

        total_processadas = 0
        total_ignoradas = 0
        economia_kb = 0

        for nome_model, ModelClass in MODELOS:
            total_model = ModelClass.objects.exclude(foto='').count()
            self.stdout.write(f'Processando {nome_model}... ({total_model} registros com foto)')
            queryset = ModelClass.objects.exclude(foto='').order_by('id')

            for obj in queryset.iterator():
                if limite and total_processadas >= limite:
                    break

                try:
                    caminho = obj.foto.path
                except Exception as e:
                    self.stdout.write(f'  [ERRO path] {nome_model} #{obj.pk} foto={obj.foto.name!r}: {e}')
                    continue

                resultado = _recomprimir_arquivo(caminho, dry_run=dry_run)

                if resultado is None:
                    total_ignoradas += 1
                    self.stdout.write(f'  [SKIP] {nome_model} #{obj.pk}: arquivo ausente ou < {LIMITE_SKIP_KB}KB')
                    continue

                antes, depois, novo_caminho = resultado
                total_processadas += 1

                if depois is not None:
                    economia_kb += antes - depois
                    # Atualiza o campo no banco se a extensão mudou
                    novo_nome_campo = os.path.splitext(obj.foto.name)[0] + '.jpg'
                    if novo_nome_campo != obj.foto.name:
                        with transaction.atomic():
                            ModelClass.objects.filter(pk=obj.pk).update(foto=novo_nome_campo)
                    self.stdout.write(f'  {nome_model} #{obj.pk}: {antes}KB → {depois}KB')
                else:
                    self.stdout.write(f'  {nome_model} #{obj.pk}: {antes}KB (seria processada)')

        # ── Resumo ─────────────────────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS(f'Processadas : {total_processadas}'))
        self.stdout.write(self.style.SUCCESS(f'Ignoradas   : {total_ignoradas} (já comprimidas < {LIMITE_SKIP_KB}KB)'))
        if not dry_run and economia_kb > 0:
            self.stdout.write(self.style.SUCCESS(f'Espaço liberado: {economia_kb / 1024:.1f} MB'))
        self.stdout.write(self.style.SUCCESS('═' * 50))

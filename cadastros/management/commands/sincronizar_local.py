"""
cadastros/management/commands/sincronizar_local.py
────────────────────────────────────────────────────
Baixa o backup mais recente do Google Drive e carrega no banco local (SQLite).

Uso:
    python manage.py sincronizar_local
    python manage.py sincronizar_local --confirmar   (pula confirmação)

Variáveis necessárias no .env local:
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_REFRESH_TOKEN
    GOOGLE_DRIVE_FOLDER_ID
"""
import gzip
import io
import json
import os
import tempfile

from decouple import config
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Sincroniza banco local com o backup mais recente do Google Drive'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar', action='store_true',
            help='Pula a confirmação interativa'
        )

    def handle(self, *args, **options):
        # ── Verificação de segurança ───────────────────────────
        db = connection.settings_dict
        if 'postgresql' in db.get('ENGINE', '') or 'postgres' in str(db.get('NAME', '')):
            self.stderr.write(self.style.ERROR(
                '❌ Este comando só pode rodar no banco LOCAL (SQLite). '
                'Não execute em produção!'
            ))
            return

        if not options['confirmar']:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  ATENÇÃO: Este comando vai APAGAR todos os dados locais\n'
                '   e substituir pelo backup mais recente do Google Drive.\n'
            ))
            resp = input('   Digite "sim" para continuar: ').strip().lower()
            if resp != 'sim':
                self.stdout.write('Operação cancelada.')
                return

        # ── Credenciais Drive ──────────────────────────────────
        folder        = config('GOOGLE_DRIVE_FOLDER_ID', default='')
        client_id     = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        refresh_token = config('GOOGLE_REFRESH_TOKEN', default='')

        if not all([folder, client_id, client_secret, refresh_token]):
            self.stderr.write(self.style.ERROR(
                'Faltam variáveis no .env: GOOGLE_DRIVE_FOLDER_ID, '
                'GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN'
            ))
            return

        # ── Conecta ao Drive ───────────────────────────────────
        self.stdout.write('🔗 Conectando ao Google Drive …')
        service = self._drive_service(client_id, client_secret, refresh_token)

        # ── Busca backup mais recente ──────────────────────────
        self.stdout.write('🔍 Buscando backup mais recente …')
        resp = service.files().list(
            q=f"'{folder}' in parents and name contains 'jr_db_' and trashed=false",
            fields='files(id,name,createdTime)',
            orderBy='createdTime desc',
            pageSize=1,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()

        arquivos = resp.get('files', [])
        if not arquivos:
            self.stderr.write(self.style.ERROR('Nenhum backup encontrado no Drive.'))
            return

        arq = arquivos[0]
        self.stdout.write(f'📥 Baixando: {arq["name"]} …')

        # ── Baixa arquivo ──────────────────────────────────────
        from googleapiclient.http import MediaIoBaseDownload
        request = service.files().get_media(
            fileId=arq['id'], supportsAllDrives=True
        )
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        buf.seek(0)

        # ── Descomprime JSON ───────────────────────────────────
        self.stdout.write('📦 Descomprimindo …')
        with gzip.GzipFile(fileobj=buf) as gz:
            json_bytes = gz.read()

        # ── Salva em arquivo temporário ────────────────────────
        with tempfile.NamedTemporaryFile(
            mode='wb', suffix='.json', delete=False
        ) as tmp:
            tmp.write(json_bytes)
            tmp_path = tmp.name

        try:
            import subprocess
            import sys

            # ── Apaga banco SQLite ─────────────────────────────
            self.stdout.write('🗑️  Apagando banco local …')
            db_path = str(connection.settings_dict.get('NAME', ''))
            connection.close()
            if db_path and os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(f'    Removido: {db_path}')

            # ── Recria via subprocess (nova conexão limpa) ─────
            self.stdout.write('🔧 Aplicando migrações …')
            ret = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--verbosity=0'],
                capture_output=True, text=True
            )
            if ret.returncode != 0:
                raise Exception(ret.stderr)

            # ── Limpa dados criados pelas migrações ───────────
            self.stdout.write('🧹 Limpando dados de migração …')
            ret = subprocess.run(
                [sys.executable, '-c',
                 'import django, os; os.environ.setdefault("DJANGO_SETTINGS_MODULE","escolta_system.settings"); django.setup();'
                 'from django.contrib.auth.models import User;'
                 'from cadastros.models_perfil import PerfilUsuario;'
                 'PerfilUsuario.objects.all().delete();'
                 'User.objects.all().delete();'
                 'print("Limpeza OK")'],
                capture_output=True, text=True
            )
            if ret.stdout:
                self.stdout.write(f'    {ret.stdout.strip()}')

            # ── Carrega dados via subprocess ───────────────────
            self.stdout.write('📂 Carregando dados …')
            ret = subprocess.run(
                [sys.executable, 'manage.py', 'loaddata', tmp_path],
                capture_output=True, text=True
            )
            if ret.returncode != 0:
                raise Exception(ret.stderr or ret.stdout)
            self.stdout.write(ret.stdout.strip())

            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Sincronização concluída! Backup: {arq["name"]}'
            ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro: {e}'))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _drive_service(self, client_id, client_secret, refresh_token):
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri='https://oauth2.googleapis.com/token',
        )
        return build('drive', 'v3', credentials=creds)

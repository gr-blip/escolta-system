"""
cadastros/management/commands/backup_to_google.py
──────────────────────────────────────────────────
Backup diário do banco (Django dumpdata JSON) + pasta de mídia para o Google Drive.

Variáveis de ambiente obrigatórias (Railway):
    GOOGLE_DRIVE_FOLDER_ID       — ID da pasta de destino no Drive
    GOOGLE_CLIENT_ID             — Client ID OAuth2
    GOOGLE_CLIENT_SECRET         — Client Secret OAuth2
    GOOGLE_REFRESH_TOKEN         — Refresh Token OAuth2 do usuário real

Uso:
    python manage.py backup_to_google
    python manage.py backup_to_google --apenas-db
    python manage.py backup_to_google --apenas-midia
    python manage.py backup_to_google --manter 14    (padrão: 7 dias)
"""
import gzip
import io
import json
import logging
import os
import tarfile

from decouple import config
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

PREFIXO_DB    = 'jr_db_'
PREFIXO_MEDIA = 'jr_media_'


class Command(BaseCommand):
    help = 'Backup diário (banco JSON + mídia) para o Google Drive'

    def add_arguments(self, parser):
        parser.add_argument('--apenas-db',    action='store_true')
        parser.add_argument('--apenas-midia', action='store_true')
        parser.add_argument('--manter',       type=int, default=7)

    def handle(self, *args, **options):
        folder        = config('GOOGLE_DRIVE_FOLDER_ID', default='')
        client_id     = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        refresh_token = config('GOOGLE_REFRESH_TOKEN', default='')

        if not all([folder, client_id, client_secret, refresh_token]):
            self.stderr.write(self.style.ERROR(
                'Faltam variáveis: GOOGLE_DRIVE_FOLDER_ID, GOOGLE_CLIENT_ID, '
                'GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN'
            ))
            return

        service = self._drive_service(client_id, client_secret, refresh_token)

        from datetime import datetime, timezone
        ts     = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        erros  = []

        apenas_db    = options['apenas_db']
        apenas_midia = options['apenas_midia']
        manter       = options['manter']

        # ── 1. Banco de dados (Django dumpdata → JSON comprimido) ──
        if not apenas_midia:
            nome_db = f'{PREFIXO_DB}{ts}.json.gz'
            self.stdout.write(f'[1/2] Exportando banco → {nome_db} …')
            try:
                buf = self._dump_db()
                self._upload(service, folder, nome_db, buf, 'application/gzip')
                self.stdout.write(self.style.SUCCESS(f'    ✓ Banco enviado: {nome_db}'))
                self._purgar_antigos(service, folder, PREFIXO_DB, manter)
            except Exception as e:
                msg = f'Falha no backup do banco: {e}'
                self.stderr.write(self.style.ERROR(f'    ✗ {msg}'))
                logger.error(msg)
                erros.append(msg)

        # ── 2. Mídia ──
        if not apenas_db:
            nome_media = f'{PREFIXO_MEDIA}{ts}.tar.gz'
            self.stdout.write(f'[2/2] Compactando mídia → {nome_media} …')
            try:
                buf = self._dump_media()
                self._upload(service, folder, nome_media, buf, 'application/gzip')
                self.stdout.write(self.style.SUCCESS(f'    ✓ Mídia enviada: {nome_media}'))
                self._purgar_antigos(service, folder, PREFIXO_MEDIA, manter)
            except Exception as e:
                msg = f'Falha no backup da mídia: {e}'
                self.stderr.write(self.style.ERROR(f'    ✗ {msg}'))
                logger.error(msg)
                erros.append(msg)

        if erros:
            self.stderr.write(self.style.ERROR(f'Backup concluído COM ERROS: {len(erros)} falha(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('Backup concluído com sucesso!'))

    # ──────────────────────────────────────────────
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

    def _dump_db(self):
        """Django dumpdata → JSON comprimido em memória."""
        buf_str = io.StringIO()
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--exclude=contenttypes',
            '--exclude=auth.permission',
            stdout=buf_str,
            verbosity=0,
        )
        buf_gz = io.BytesIO()
        with gzip.GzipFile(fileobj=buf_gz, mode='wb') as gz:
            gz.write(buf_str.getvalue().encode('utf-8'))
        buf_gz.seek(0)
        return buf_gz

    def _dump_media(self):
        """Compacta /app/media em tarball gzip em memória."""
        media_root = getattr(settings, 'MEDIA_ROOT', '/app/media')
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w:gz') as tar:
            if os.path.exists(media_root):
                tar.add(media_root, arcname='media')
        buf.seek(0)
        return buf

    def _upload(self, service, folder_id, nome, buf, mime):
        from googleapiclient.http import MediaIoBaseUpload
        meta  = {'name': nome, 'parents': [folder_id]}
        media = MediaIoBaseUpload(buf, mimetype=mime, resumable=True)
        service.files().create(
            body=meta, media_body=media, fields='id',
            supportsAllDrives=True,
        ).execute()

    def _purgar_antigos(self, service, folder_id, prefixo, manter):
        query = (
            f"'{folder_id}' in parents "
            f"and name contains '{prefixo}' "
            f"and trashed = false"
        )
        resp = service.files().list(
            q=query, fields='files(id,name,createdTime)',
            orderBy='createdTime desc',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        for arq in resp.get('files', [])[manter:]:
            service.files().delete(
                fileId=arq['id'], supportsAllDrives=True
            ).execute()
            self.stdout.write(f'    🗑  Removido: {arq["name"]}')

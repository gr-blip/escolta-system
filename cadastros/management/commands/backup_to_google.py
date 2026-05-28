"""
cadastros/management/commands/backup_to_google.py
──────────────────────────────────────────────────
Backup diário do banco PostgreSQL + pasta de mídia para o Google Drive.

Uso:
    python manage.py backup_to_google
    python manage.py backup_to_google --apenas-db
    python manage.py backup_to_google --apenas-midia
    python manage.py backup_to_google --manter 14    (padrão: 7 dias)

Variáveis de ambiente obrigatórias (Railway):
    DATABASE_URL               — string de conexão PostgreSQL
    GOOGLE_SERVICE_ACCOUNT_JSON — conteúdo JSON da conta de serviço
    GOOGLE_DRIVE_FOLDER_ID      — ID da pasta de destino no Drive
"""
import io
import json
import logging
import os
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone

from decouple import config
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

PREFIXO_DB    = 'jr_db_'
PREFIXO_MEDIA = 'jr_media_'


class Command(BaseCommand):
    help = 'Backup diário (PostgreSQL + mídia) para o Google Drive'

    def add_arguments(self, parser):
        parser.add_argument('--apenas-db',    action='store_true', help='Faz só o backup do banco')
        parser.add_argument('--apenas-midia', action='store_true', help='Faz só o backup da mídia')
        parser.add_argument('--manter',       type=int, default=7,
                            help='Quantos backups manter por tipo (padrão: 7)')

    # ──────────────────────────────────────────────
    def handle(self, *args, **options):
        db_url  = config('DATABASE_URL', default='')
        sa_json = config('GOOGLE_SERVICE_ACCOUNT_JSON', default='')
        folder  = config('GOOGLE_DRIVE_FOLDER_ID', default='')

        if not db_url or not sa_json or not folder:
            self.stderr.write(self.style.ERROR(
                'Faltam variáveis de ambiente: DATABASE_URL, '
                'GOOGLE_SERVICE_ACCOUNT_JSON, GOOGLE_DRIVE_FOLDER_ID'
            ))
            return

        try:
            sa_info = json.loads(sa_json)
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR('GOOGLE_SERVICE_ACCOUNT_JSON não é um JSON válido.'))
            return

        service = self._drive_service(sa_info)
        ts      = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        erros   = []

        apenas_db    = options['apenas_db']
        apenas_midia = options['apenas_midia']
        manter       = options['manter']

        # ── 1. Banco de dados ─────────────────────
        if not apenas_midia:
            nome_db = f'{PREFIXO_DB}{ts}.sql.gz'
            self.stdout.write(f'[1/2] Gerando dump do banco → {nome_db} …')
            try:
                buf = self._dump_db(db_url)
                self._upload(service, folder, nome_db, buf, 'application/gzip')
                self.stdout.write(self.style.SUCCESS(f'    ✓ Banco enviado: {nome_db}'))
                self._purgar_antigos(service, folder, PREFIXO_DB, manter)
            except Exception as e:
                msg = f'Falha no backup do banco: {e}'
                self.stderr.write(self.style.ERROR(f'    ✗ {msg}'))
                logger.error(msg)
                erros.append(msg)

        # ── 2. Mídia ──────────────────────────────
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

        # ── Resultado final ───────────────────────
        if erros:
            self.stderr.write(self.style.ERROR(f'Backup concluído COM ERROS: {len(erros)} falha(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('Backup concluído com sucesso!'))

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def _drive_service(self, sa_info):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        creds = service_account.Credentials.from_service_account_info(
            sa_info, scopes=['https://www.googleapis.com/auth/drive.file']
        )
        return build('drive', 'v3', credentials=creds)

    def _dump_db(self, db_url):
        """Executa pg_dump e retorna buffer gzip em memória."""
        with tempfile.NamedTemporaryFile(suffix='.sql', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = self._pg_password(db_url)
            subprocess.run(
                ['pg_dump', '--no-password', db_url, '-f', tmp_path],
                check=True, env=env,
                capture_output=True
            )
            buf = io.BytesIO()
            import gzip
            with open(tmp_path, 'rb') as f_in, gzip.GzipFile(fileobj=buf, mode='wb') as f_gz:
                f_gz.write(f_in.read())
            buf.seek(0)
            return buf
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _pg_password(self, db_url):
        """Extrai senha do DATABASE_URL (postgresql://user:senha@host/db)."""
        try:
            from urllib.parse import urlparse
            return urlparse(db_url).password or ''
        except Exception:
            return ''

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
        service.files().create(body=meta, media_body=media, fields='id').execute()

    def _purgar_antigos(self, service, folder_id, prefixo, manter):
        """Remove backups mais antigos que `manter` dias, mantendo ao menos `manter` arquivos."""
        query = (
            f"'{folder_id}' in parents "
            f"and name contains '{prefixo}' "
            f"and trashed = false"
        )
        resp = service.files().list(
            q=query, fields='files(id,name,createdTime)',
            orderBy='createdTime desc'
        ).execute()
        arquivos = resp.get('files', [])
        excluir  = arquivos[manter:]          # mantém os N mais recentes
        for arq in excluir:
            service.files().delete(fileId=arq['id']).execute()
            self.stdout.write(f'    🗑  Removido backup antigo: {arq["name"]}')

import os
import subprocess
import datetime
import json
import tarfile
from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

class Command(BaseCommand):
    help = 'Backs up database and media files to Google Drive'

    def handle(self, *args, **options):
        self.stdout.write("Starting backup process...")

        # Configuration
        db_url = config('DATABASE_URL', default='')
        google_service_account_json = config('GOOGLE_SERVICE_ACCOUNT_JSON', default='')
        google_drive_folder_id = config('GOOGLE_DRIVE_FOLDER_ID', default='')
        
        if not db_url or not google_service_account_json or not google_drive_folder_id:
            self.stderr.write("Error: Missing required environment variables (DATABASE_URL, GOOGLE_SERVICE_ACCOUNT_JSON, GOOGLE_DRIVE_FOLDER_ID)")
            return

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        db_backup_file = f'db_backup_{timestamp}.sql'
        media_backup_file = f'media_backup_{timestamp}.tar.gz'

        try:
            # 1. Database Backup
            self.stdout.write(f"Dumping database to {db_backup_file}...")
            # Note: On Railway/Linux, pg_dump is usually available.
            # We use the DATABASE_URL directly with pg_dump
            subprocess.run(['pg_dump', db_url, '-f', db_backup_file], check=True)
            self.stdout.write("Database dump successful.")

            # 2. Media Files Backup
            self.stdout.write(f"Archiving media folder to {media_backup_file}...")
            media_root = getattr(settings, 'MEDIA_ROOT', '/app/media')
            with tarfile.open(media_backup_file, "w:gz") as tar:
                tar.add(media_root, arcname=os.path.basename(media_root))
            self.stdout.write("Media archive successful.")

            # 3. Upload to Google Drive
            self.stdout.write("Uploading to Google Drive...")
            
            # Parse service account JSON
            try:
                service_account_info = json.loads(google_service_account_json)
            except json.JSONDecodeError:
                self.stderr.write("Error: GOOGLE_SERVICE_ACCOUNT_JSON is not a valid JSON string.")
                return

            scopes = ['https://www.googleapis.com/auth/drive.file']
            creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)
            service = build('drive', 'v3', credentials=creds)

            for file_to_upload in [db_backup_file, media_backup_file]:
                file_metadata = {
                    'name': file_to_upload,
                    'parents': [google_drive_folder_id]
                }
                media = MediaFileUpload(file_to_upload, resumable=True)
                uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                self.stdout.write(f"Uploaded {file_to_upload} (ID: {uploaded_file.get('id')})")

            self.stdout.write("Backup process completed successfully!")

        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error during pg_dump: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
        finally:
            # Cleanup local files
            for f in [db_backup_file, media_backup_file]:
                if os.path.exists(f):
                    os.remove(f)
                    self.stdout.write(f"Removed local file {f}")

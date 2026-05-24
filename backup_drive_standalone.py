import os
import subprocess
import datetime
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

def run_command(command, shell=False, env=None):
    result = subprocess.run(command, shell=shell, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}\nError: {result.stderr}")
    return result.stdout

def main():
    db_url        = os.getenv('DATABASE_URL')
    google_json   = os.getenv('GCP_SA_KEY_JSON')
    folder_id     = os.getenv('GDRIVE_FOLDER_ID')
    railway_token = os.getenv('RAILWAY_TOKEN')
    app_url       = os.getenv('RAILWAY_APP_URL')
    project_id    = os.getenv('RAILWAY_PROJECT_ID')

    if not all([db_url, google_json, folder_id, railway_token, app_url, project_id]):
        print("Erro: variáveis de ambiente incompletas.")
        exit(1)

    # Diagnóstico do Token (Sem expor o valor completo)
    if railway_token:
        print(f"Diagnóstico: Token carregado. Tamanho: {len(railway_token)} caracteres. Início: {railway_token[:4]}... Fim: ...{railway_token[-4:]}")
    else:
        print("Diagnóstico: Token NÃO carregado.")

    timestamp         = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    db_backup_file    = f'db_backup_{timestamp}.sql.gz'
    media_backup_file = f'media_backup_{timestamp}.tar.gz'

    try:
        # ── 1. Backup do banco ──────────────────────────────────────────
        print(f"Iniciando backup do banco → {db_backup_file}")
        env = os.environ.copy()
        cmd_db = f'pg_dump --dbname="{db_url}" | gzip > {db_backup_file}'
        run_command(cmd_db, shell=True, env=env)
        size_db = os.path.getsize(db_backup_file) / 1_048_576
        print(f"Banco OK — {size_db:.1f} MB")

        # ── 2. Backup da mídia via Railway CLI ──────────────────────────
        print(f"Iniciando backup de mídia → {media_backup_file}")
        
        env_railway = os.environ.copy()
        env_railway['RAILWAY_TOKEN'] = railway_token
        env_railway['RAILWAY_PROJECT_ID'] = project_id
        env_railway['RAILWAY_ENVIRONMENT'] = 'production'
        
        cmd_media = [
            'railway', 'run',
            '--', 'tar', 'czf', '-', '/app/media'
        ]
        
        print(f"  Executando stream de mídia via contexto de ambiente...")
        with open(media_backup_file, 'wb') as f_out:
            result = subprocess.run(cmd_media, stdout=f_out, stderr=subprocess.PIPE, env=env_railway)
        
        if result.returncode != 0:
            # Imprime o erro do Railway detalhadamente
            stderr_output = result.stderr.decode()
            raise Exception(f"railway run falhou:\n{stderr_output}")

        size_media = os.path.getsize(media_backup_file)
        if size_media < 100:
            raise Exception("Arquivo de mídia muito pequeno — o tar provavelmente falhou silenciosamente.")
        print(f"Mídia OK — {size_media / 1_048_576:.1f} MB")

        # ── 3. Upload para o Google Drive ───────────────────────────────
        print("Enviando para o Google Drive...")
        creds = service_account.Credentials.from_service_account_info(
            json.loads(google_json),
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        service = build('drive', 'v3', credentials=creds)

        for filepath in [db_backup_file, media_backup_file]:
            metadata = {'name': filepath, 'parents': [folder_id]}
            media    = MediaFileUpload(filepath, resumable=True)
            result   = service.files().create(
                body=metadata, media_body=media, fields='id'
            ).execute()
            print(f"  ✓ {filepath} (Drive ID: {result['id']})")

        print("\nBackup concluído com sucesso!")

    except Exception as e:
        print(f"\nERRO CRÍTICO: {e}")
        exit(1)

    finally:
        for f in [db_backup_file, media_backup_file]:
            if os.path.exists(f):
                os.remove(f)
                print(f"Temporário removido: {f}")

if __name__ == "__main__":
    main()

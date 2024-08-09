from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Chargement des credentials depuis la variable d'environnement
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if GOOGLE_APPLICATION_CREDENTIALS is None:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")

credentials_info = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
credentials = service_account.Credentials.from_service_account_info(
    credentials_info, scopes=['https://www.googleapis.com/auth/drive.file'])

service = build('drive', 'v3', credentials=credentials)

# Liste des fichiers dans Google Drive
results = service.files().list().execute()
files = results.get('files', [])

if not files:
    print('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"{file.get('name')} ({file.get('id')})")


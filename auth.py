from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Charger les identifiants OAuth 2.0 depuis une variable d'environnement
credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_json is None:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")

# Convertir le JSON en dictionnaire
credentials_info = json.loads(credentials_json)

# Préparer les informations pour l'authentification
creds = service_account.Credentials.from_service_account_info(
    credentials_info, scopes=['https://www.googleapis.com/auth/drive.metadata.readonly']
)

# Construire le service Google Drive
service = build('drive', 'v3', credentials=creds)

# Liste les fichiers dans Google Drive
results = service.files().list().execute()
files = results.get('files', [])

if not files:
    print('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"{file.get('name')} ({file.get('id')})")



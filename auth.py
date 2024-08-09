import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Lire le secret GitHub depuis les variables d'environnement
credentials_json = os.getenv('GOOGLE_CREDENTIALS')

if not credentials_json:
    raise ValueError("Google credentials not found in environment variables")

# Sauvegarder le secret dans un fichier temporaire
credentials_path = '/tmp/credentials.json'
with open(credentials_path, 'w') as file:
    file.write(credentials_json)

# Charger les credentials
try:
    with open(credentials_path, 'r') as file:
        credentials_info = json.load(file)
except OSError as e:
    raise ValueError(f"Error loading credentials file: {e}")

# Créer les credentials
try:
    creds = service_account.Credentials.from_service_account_info(credentials_info)
except ValueError as e:
    raise ValueError(f"Error creating credentials: {e}")

# Créer le service Google Drive
service = build('drive', 'v3', credentials=creds)

# Exemple pour lister les fichiers
results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f'{item["name"]} ({item["id"]})')




    






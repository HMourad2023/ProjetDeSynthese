from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Chemin vers le fichier JSON de clé de service
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_path is None:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")

# Nettoyer les guillemets supplémentaires si nécessaire
credentials_path = credentials_path.strip('"')

# Charger les informations d'identification depuis le fichier JSON
try:
    with open(credentials_path, 'r') as file:
        credentials_info = json.load(file)
except (IOError, json.JSONDecodeError) as e:
    raise ValueError(f"Error loading credentials file: {e}")

# Préparer les informations d'identification pour le compte de service
try:
    creds = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/drive']  # Accès complet
    )
    logging.info("Credentials created successfully.")
except Exception as e:
    raise ValueError(f"Error creating credentials: {e}")

# Construire le service Google Drive
try:
    service = build('drive', 'v3', credentials=creds)
    logging.info("Google Drive service created successfully.")
except Exception as e:
    raise ValueError(f"Error building Google Drive service: {e}")

# Lister les fichiers dans Google Drive
try:
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name)"
    ).execute()
    logging.debug(f"Results: {results}")
    files = results.get('files', [])
    logging.info("Files retrieved successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
    files = []

if not files:
    print('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"{file.get('name')} ({file.get('id')})")


    






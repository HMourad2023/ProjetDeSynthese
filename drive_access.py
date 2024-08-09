from google.oauth2 import service_account
from googleapiclient.discovery import build

# Utilisez une variable d'environnement pour le chemin du fichier des informations d'identification
import os

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    # Authentification avec le fichier de clés JSON
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    # Création du service Google Drive
    service = build('drive', 'v3', credentials=credentials)
    
    # Liste des fichiers dans Google Drive
    results = service.files().list().execute()
    items = results.get('files', [])

    if not items:
        print("No files found")
    else:
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")

if __name__ == "__main__":
    main()

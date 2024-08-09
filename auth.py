import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Chemin du fichier JSON avec les credentials
credentials_path = 'C:/Users/Asus_M/Desktop/credentials.json'

def load_credentials(path):
    try:
        # Lire le contenu du fichier
        with open(path, 'r') as file:
            # Charger les données JSON
            credentials_info = json.load(file)
        return credentials_info
    except FileNotFoundError:
        raise ValueError(f"Le fichier de credentials est introuvable à l'emplacement : {path}")
    except json.JSONDecodeError as e:
        # Gérer les erreurs de parsing JSON
        raise ValueError(f"Erreur lors du parsing des credentials JSON : {e}")

def main():
    try:
        # Charger les informations de credentials
        credentials_info = load_credentials(credentials_path)
        
        # Créer les credentials Google
        creds = service_account.Credentials.from_service_account_info(credentials_info)

        # Créer le service Google Drive
        service = build('drive', 'v3', credentials=creds)

        # Exemple pour lister les fichiers
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('Aucun fichier trouvé.')
        else:
            print('Fichiers :')
            for item in items:
                print(f'{item["name"]} ({item["id"]})')

    except ValueError as e:
        print(e)
    except Exception as e:
        # Capturer toute autre exception non prévue
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()

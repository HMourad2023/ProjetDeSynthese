from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Chemin du fichier credentials
credentials_path = 'C:/Users/Asus_M/Desktop/credentials.json'

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



    






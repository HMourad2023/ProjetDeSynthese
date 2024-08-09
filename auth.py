from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Load service account credentials from the environment variable
credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_json is None:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")

# Convert JSON string to dictionary
try:
    credentials_info = json.loads(credentials_json)
except json.JSONDecodeError as e:
    raise ValueError(f"Error decoding JSON: {e}")

# Prepare the credentials for service account
try:
    creds = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly']
    )
except Exception as e:
    raise ValueError(f"Error creating credentials: {e}")

# Build the Google Drive service
try:
    service = build('drive', 'v3', credentials=creds)
except Exception as e:
    raise ValueError(f"Error building Google Drive service: {e}")

# List files in Google Drive
try:
    results = service.files().list().execute()
    files = results.get('files', [])
except Exception as e:
    raise ValueError(f"Error listing files: {e}")

if not files:
    print('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"{file.get('name')} ({file.get('id')})")


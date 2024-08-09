# import streamlit as st
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import json

# def authenticate_google_drive():
#     credentials_json = st.secrets["GOOGLE_DRIVE_CREDENTIALS"]
#     credentials_info = json.loads(credentials_json)
#     credentials = service_account.Credentials.from_service_account_info(
#         credentials_info,
#         scopes=['https://www.googleapis.com/auth/drive']
#     )
#     service = build('drive', 'v3', credentials=credentials)
#     return service

# def list_files(service):
#     results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     return items

# def main():
#     st.title('Google Drive File List')
#     service = authenticate_google_drive()
#     items = list_files(service)
#     if not items:
#         st.write('No files found.')
#     else:
#         for item in items:
#             st.write(f'{item["name"]} ({item["id"]})')

# if __name__ == '__main__':
#     main()

from google.cloud import storage

import pandas as pd
import io

storage_client = storage.Client.from_service_account_json('google_drive/credentials.json')

def list_blobs(bucket_name, key_file_path):
    """Lists all the blobs in the bucket."""
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)


def create_file_dfs(bucket_name):
    file_names = [
        'diabetes_recommendation.csv',
        'diabetes_to_heart_clean.csv',
        'for_diabetes.csv',
        'heart-to-stroke.csv'
    ]

    # Create a dictionary to hold the DataFrames
    dataframes = {}

    # Loop through the file names and read each CSV file from GCS into a DataFrame
    for file_name in file_names:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Download the file to a BytesIO object
        file_data = io.BytesIO()
        blob.download_to_file(file_data)
        file_data.seek(0) # Move the file pointer to the beginning of the file
        
        # Read the CSV data into a DataFrame
        df = pd.read_csv(file_data)
        dataframes[file_name] = df
        return dataframes
# Replace 'your-bucket-name' with the name of your GCS bucket
# Replace 'path/to/your-service-account-file.json' with the actual path to your service account key file


# 

# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from dotenv import load_dotenv

# # If modifying these SCOPES, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# load_dotenv()

# def authenticate_google_drive():
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'google_drive/credentials.json', SCOPES,redirect_uri='http://localhost:63468/')
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     return build('drive', 'v3', credentials=creds)

# def get_files_from_drive(service):
#     folder_id = os.getenv("FOLDER_ID")
#     # Call the Drive v3 API to list files in the specified folder
#     results = service.files().list(
#         q=f"'{folder_id}' in parents", # Query to list files in the specified folder
#         pageSize=10,
#         fields="nextPageToken, files(id, name)"
#     ).execute()
#     items = results.get('files', [])

#     if not items:
#         print('No files found in the specified folder.')
#     else:
#         print('Files in the specified folder:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))


# # if __name__ == '__main__':
#     # service = authenticate_google_drive()
#     # get_files_from_drive(service)
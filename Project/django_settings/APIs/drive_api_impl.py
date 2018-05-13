from apiclient.discovery import build
from httplib2 import Http
from APIs.drive_auth import GAuth
from oauth2client import file
from watermark.models import Song

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
gg_auth = GAuth(SCOPES, store)
creds = gg_auth.getCredentials()
service = build('drive', 'v3', http=creds.authorize(Http()))
music_folder_id = '1BuTssjkPviXt0qJClmLZYR5pO33aOiob'

# Call the Drive v3 API
# results = service.files().list(
#     pageSize=20, 
#     fields="nextPageToken, files(id, name)", 
#     q=f"'{music_folder_id}' in parents").execute()
# items = results.get('files', [])
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(f"{item['name']} ({item['id']})")

def save_files_to_sqlite():
    results = service.files().list(
        pageSize=20, 
        fields="nextPageToken, files(id, name)", 
        q=f"'{music_folder_id}' in parents").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")
            if "-" in item['name']:
                name = item['name'].split(' - ')[0]
                author = item['name'].split(' - ')[1].split('.')[0]
            else:
                name = item['name'].split('.')[0]
                author = ""
            id = item['id']
            song = Song(id=id, name=name, author=author)
            song.save()
            print('Saved songs to database')
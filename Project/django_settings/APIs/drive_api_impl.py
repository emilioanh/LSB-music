from apiclient.discovery import build
from httplib2 import Http
from APIs.drive_auth import GAuth
from oauth2client import file
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from watermark.models import Song
from mimetypes import MimeTypes
import os, io

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials.json')
gg_auth = GAuth(SCOPES, store)
creds = gg_auth.getCredentials()
drive_service = build('drive', 'v3', http=creds.authorize(Http()))
music_folder_id = '1BuTssjkPviXt0qJClmLZYR5pO33aOiob'
default_download_folder = os.path.expanduser(os.sep.join(["~", "Downloads"]))

# Call the Drive v3 API
# results = drive_service.files().list(
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
    results = drive_service.files().list(
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
            fileType = item['name'].split('.')[1]
            id = item['id']
            song = Song(id=id, name=name, author=author, fileType=fileType)
            song.save()
            print('Saved songs to database')

def uploadToFolder(name, path, mimetype, folderId=music_folder_id):
    file_metadata = {
        'name': name,
        'parents': [f'{folderId}']
    }
    media = MediaFileUpload(path,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    fileId = file.get('id')
    print(f'File ID: {fileId}')
    return fileId

def downloadFile(fileId, fileName, folderPath=default_download_folder):
    request = drive_service.files().get_media(fileId=fileId)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    savedPath = folderPath + os.sep + fileName
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with open(savedPath, "wb") as fi:
        fh.seek(0)
        fi.write(fh.read())
    print("Downloaded to: " + savedPath)
    return savedPath

def createFolder(folderName):
    #create folder with provided name
    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [music_folder_id],
    }
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    
    #share folder with custom permission https://developers.google.com/drive/api/v3/manage-sharing
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    batch = drive_service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    batch.add(drive_service.permissions().create(
        fileId=file.get('id'),
        body=user_permission,
        fields='id',
    ))
    batch.execute()
    print(f"Folder ID: {file.get('id')}")
    return file.get('id')
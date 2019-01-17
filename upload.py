from __future__ import print_function

import os.path
import pickle

import io
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from var import status
import json
if status.test is True:
    from var import test as env
else:
    from var import env

SCOPES = 'https://www.googleapis.com/auth/drive'


def get_credential():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    DRIVE = build('drive', 'v3', credentials=creds)
    return DRIVE


def upload():
    DRIVE = get_credential()
    file_name = "test.zip"
    folder_str = create_folder(DRIVE)
    content = open("{0}/data-upload.zip".format(env.pathdir), "rb")
    media_body = MediaFileUpload("{0}/data-upload.zip".format(env.pathdir), mimetype='application/zip'
            ,resumable=True)
    # print(type(str(media_body)))
    metadata = {
        'name': file_name,
        "parents" : [folder_str]
    }
    request = DRIVE.files().create(body=metadata,
                         media_body=media_body,
                         fields='id').execute()

    print(request)
    # response = None
    # while response is None:
    #     status, response = request.next_chunk()
    #     if status:
    #         print ("Uploaded %d%%." % int(status.progress() * 100))
    # print ("Upload Complete!")


def create_folder(DRIVE):
    file_metadata = {
        'name': 'folderTest',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get("id")
upload()

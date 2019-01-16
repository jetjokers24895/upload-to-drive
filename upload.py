from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from var import status

if status.test is True:
	from var import test as env
else:
	from var import env

SCOPES = 'https://www.googleapis.com/auth/drive'
def get_credential():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    return DRIVE


def upload():
	DRIVE = get_credential()
	file_name = "test.zip"
	content = open("{0}/data-upload.zip".format(env.pathdir), "rb")
	metadata = {'title': file_name}
	DRIVE.files().create(body=metadata,
                                media_body= content,
                                fields='id').execute()


upload()
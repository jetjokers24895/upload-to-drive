from zipfile import ZipFile
from var import status


if status.test is True:
	from var import test as env
else:
	from var import env

with ZipFile("{0}/data-upload.zip".format(env.pathdir), "r") as f:
	print(f.read())
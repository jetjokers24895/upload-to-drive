import os

class status:
	test = True

class env:
	pathdir = os.getcwd()

class test:
	pathdir = "{0}/test".format(env.pathdir)
"""contentbox_add.py
Supports adding to the contentbox"""
import httplib2
from errors import *
class ContentboxAddCommand(object):
	h = httplib2.Http()
	def __init__(self, store_uri=None, data=None, type="application/x-unknown"):
		self.store_uri = (store_uri is not None and store_uri.endswith("/")) and store_uri[:-1] or store_uri
		self.data = data
		self.type = type
	def set_store_uri(self, store_uri):
		self.store_uri = store_uri.endswith("/") and store_uri[:-1] or store_uri
	def set_data(self, data):
		self.data = data
	def set_type(self, type):
		self.type = type
	def login(self, un, pw):
		self.h.add_credentials(un, pw)
	def execute(self):
		uri = self.store_uri + "/items"
		headers, data = self.h.request(uri, "POST", body=self.data, headers={"content-type" : self.type})
		if int(headers["status"]) in range(200, 300):
			pass
		else:
			raise CouldNotSendRequest("POST '%s': got status %s" % (uri, headers["status"]))

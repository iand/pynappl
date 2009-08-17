"""describe.py
Supports describing a URI in a store."""
__all__ = ["DescribeCommand"]
import httplib2
import urllib
import rdflib
from errors import *
class DescribeCommand(object):
	h = httplib2.Http()
	def __init__(self, store_uri=None, describe_uri=None):
		self.store_uri = (store_uri is not None and store_uri.endswith("/")) and store_uri[:-1] or store_uri
		self.describe_uri = describe_uri
	def set_store_uri(self, store_uri):
		self.store_uri = store_uri.endswith("/") and store_uri[:-1] or store_uri
	def set_describe_uri(self, describe_uri):
		self.describe_uri = describe_uri
	def execute(self):
		if self.store_uri is None:
			raise InvalidCommandParameters("Store URI is not set")
		if self.describe_uri is None:
			raise InvalidCommandParameters("Description URI is not set")
		uri = self.store_uri + "/meta?about=" + urllib.quote_plus(self.describe_uri)
		headers, data = self.h.request(uri, "GET", headers={"accept" : "application/rdf+xml"})
		if int(headers["status"]) in range(200, 300):
			g = rdflib.ConjunctiveGraph()
			g.parse(rdflib.StringInputSource(data), uri, "xml")
			self.graph = g
		else:
			raise CouldNotSendRequest("GET \"%s\": got status %s" % (uri, headers["status"]))
	def get_graph(self):
		return self.graph
if __name__ == "__main__":
	print "***** Testing *****"
	c = DescribeCommand()
	c.set_store_uri("http://api.talis.com/stores/iand-dev4")
	c.set_describe_uri("http://iandavis.com/id/steph.rdf")
	c.execute()
	print repr(list(c.get_graph().triples((None, None, None))))
	print "***** Done *****"

"""sparql.py
Supports SPARQL queries on the metabox"""
__all__ = ["SPARQLCommand", "SPARQLAskCommand", "SPARQLGraphCommand", "SPARQLSelectCommand"]
import httplib2
import urllib
import rdflib
from errors import *
from sparql_select_result import SPARQLSelectResult
from xml.etree import ElementTree as et
class SPARQLCommand(object):
	h = httplib2.Http()
	def __init__(self, store_uri=None, query=None):
		if self.__class__ == SPARQLCommand:
			raise AbstractClassError("SPARQLCommand", "SPARQLGraphCommand", "SPARQLSelectCommand", "SPARQLAskCommand")
		self.store_uri = (store_uri is not None and store_uri.endswith("/")) and store_uri[:-1] or store_uri
		self.query = query
	def set_store_uri(self, store_uri):
		self.store_uri = store_uri.endswith("/") and store_uri[:-1] or store_uri
	def set_query(self, query):
		self.query = query
	def execute(self):
		if self.store_uri is None:
			raise InvalidCommandParameters("Store URI is not set")
		if self.query is None:
			raise InvalidCommandParameters("Query is not set")
		uri = self.store_uri + "/services/sparql?query=" + urllib.quote_plus(self.query)
		headers, data = self.h.request(uri, "GET", headers={"accept" : self.accept})
		if int(headers["status"]) in range(200, 300):
			self.parse(data, uri)
		else:
			raise CouldNotSendRequest("GET \"%s\": got status %s" % (uri, headers["status"]))
	def parse(self, data, uri):
		pass
	def get_result(self):
		return self.result
class SPARQLGraphCommand(SPARQLCommand):
	accept = "application/rdf+xml"
	result = rdflib.ConjunctiveGraph()
	def parse(self, data, uri):
		self.result.parse(rdflib.StringInputSource(data), uri, "xml")
class SPARQLSelectCommand(SPARQLCommand):
	accept = "application/sparql-results+xml"
	def parse(self, data, uri):
		r = SPARQLSelectResult()
		r.parse(data)
		self.result = r
class SPARQLAskCommand(SPARQLCommand):
	accept = "application/sparql-results+xml"
	def parse(self, data, uri):
		tree = et.fromstring(data)
		t = tree.find("{http://www.w3.org/2005/sparql-results#}boolean").text
		self.result = {"true" : True, "false" : False}[t]
if __name__ == "__main__":
	print "***** Testing *****"
	c = SPARQLGraphCommand()
	c.set_store_uri("http://api.talis.com/stores/iand-dev4")
	c.set_query("CONSTRUCT {?s <http://xmlns.com/foaf/0.1/name> ?l} WHERE {?s a <http://xmlns.com/foaf/0.1/Person>. ?s <http://xmlns.com/foaf/0.1/name> ?l}")
	c.execute()
	r = c.get_result()
	print repr(list(r.triples((None, None, None))))
	c = SPARQLSelectCommand()
	c.set_store_uri("http://api.talis.com/stores/iand-dev4")
	c.set_query("SELECT ?s ?l WHERE {?s a <http://xmlns.com/foaf/0.1/Person>. ?s <http://xmlns.com/foaf/0.1/name> ?l}")
	c.execute()
	r = c.get_result()
	print r.get_variables(), r.get_results()
	c = SPARQLAskCommand()
	c.set_store_uri("http://api.talis.com/stores/iand-dev4")
	c.set_query("ASK WHERE {?s a <http://xmlns.com/foaf/0.1/Person>. ?s <http://xmlns.com/foaf/0.1/name> ?l}")
	c.execute()
	r = c.get_result()
	print r
	print "***** Done *****"

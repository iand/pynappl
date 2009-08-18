"""add.py
Support for adding triples to the metabox."""
__all__ = ["MetaboxAddCommand"]
import httplib2
import random
import sparql
from errors import *
class MetaboxAddCommand(object):
  h = httplib2.Http()
  def __init__(self, store_uri=None, rdfxml=None):
    self.store_uri = (store_uri is not None and store_uri.endswith("/")) and store_uri[:-1] or store_uri
    self.rdfxml = rdfxml
  def set_store_uri(self, store_uri):
    self.store_uri = store_uri.endswith("/") and store_uri[:-1] or store_uri
  def set_rdfxml(self, rdfxml):
    self.rdfxml = rdfxml
  def login(self, un, pw):
    self.h.add_credentials(un, pw)
  def execute(self):
    if self.store_uri is None:
      raise InvalidCommandParameters("Store URI is not set")
    if self.rdfxml is None:
      raise InvalidCommandParameters("RDF/XML content is not set")
    uri = self.store_uri + "/meta"
    headers, data = self.h.request(uri, "POST", body=self.rdfxml, headers={"content-type" : "application/rdf+xml"})
    if int(headers["status"]) in range(200, 300):
      pass
    else:
      raise CouldNotSendRequest("POST \"%s\": got status %s" % (uri, headers["status"]))
if __name__ == "__main__":
  def get_test_rdfxml():
    r = "".join([random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890") for i in range(16)])
    s = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
  <rdf:Description rdf:about="http://www.example.com">
    <rdfs:label>%s</rdfs:label>
  </rdf:Description>
</rdf:RDF>""" % r
    return s, r
  print "***** Testing *****"
  c = AddCommand()
  c.set_store_uri("http://api.talis.com/stores/iand-dev4")
  data, r = get_test_rdfxml()
  c.set_rdfxml(data)
  c.login("uid", "pwd")
  c.execute()
  c = sparql.SPARQLSelectCommand()
  c.set_store_uri("http://api.talis.com/stores/iand-dev4")
  c.set_query("SELECT ?s WHERE {?s <http://www.w3.org/2000/01/rdf-schema#label> '%s'}" % r)
  c.execute()
  result = c.get_result()
  assert len(result.variables) == 1
  assert result.variables[0] == "s"
  assert len(result.results) == 1
  assert len(result.results[0])== 1
  assert result.results[0]["s"] == "http://www.example.com"
  print "***** Done *****"

# sparql_client.py - facade for accessing SPARQL endpoints
# Copyright (C) 2009 Talis Information Ltd.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA


__all__ = ["SparqlClient", "SPARQL_RESULTS_XML", "SPARQL_RESULTS_JSON"]

import httplib2
import urllib

SPARQL_RESULTS_XML = "application/sparql-results+xml"
SPARQL_RESULTS_JSON = "application/sparql-results+json"

SYMMETRIC_BOUNDED_DESCRIPTION = """CONSTRUCT {?uri ?p ?o . ?s ?p2 ?uri .} WHERE { {?uri ?p ?o .} UNION {?s ?p2 ?uri .} }"""

LABELLED_BOUNDED_DESCRIPTION = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
CONSTRUCT {
  ?uri ?p ?o . 
  ?o rdfs:label ?label . 
  ?o rdfs:comment ?comment . 
  ?o <http://www.w3.org/2004/02/skos/core#prefLabel> ?plabel . 
  ?o rdfs:seeAlso ?seealso.
} WHERE {
  ?uri ?p ?o . 
  OPTIONAL { 
    ?o rdfs:label ?label .
  } 
  OPTIONAL {
    ?o <http://www.w3.org/2004/02/skos/core#prefLabel> ?plabel . 
  } 
  OPTIONAL {
    ?o rdfs:comment ?comment . 
  } 
  OPTIONAL { 
    ?o rdfs:seeAlso ?seealso.
  }
}"""

SYMMETRIC_LABELLED_BOUNDED_DESCRIPTION = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
CONSTRUCT {
  ?uri ?p ?o . 
  ?o rdfs:label ?label . 
  ?o rdfs:comment ?comment . 
  ?o rdfs:seeAlso ?seealso. 
  ?s ?p2 ?uri . 
  ?s rdfs:label ?label . 
  ?s rdfs:comment ?comment . 
  ?s rdfs:seeAlso ?seealso.
} WHERE { 
  { ?uri ?p ?o . 
    OPTIONAL { 
      ?o rdfs:label ?label .
    } 
    OPTIONAL {
      ?o rdfs:comment ?comment .
    } 
    OPTIONAL {
      ?o rdfs:seeAlso ?seealso.
    } 
  } 
  UNION {
    ?s ?p2 ?uri . 
    OPTIONAL {
      ?s rdfs:label ?label .
    }
    OPTIONAL {
      ?s rdfs:comment ?comment .
    }
    OPTIONAL {
      ?s rdfs:seeAlso ?seealso.
    }
  }
}"""

DESCRIPTIONS = {
  "cbd" : "DESCRIBE ?uri",
  "scbd" : SYMMETRIC_BOUNDED_DESCRIPTION,
  "lcbd" : LABELLED_BOUNDED_DESCRIPTION,
  "slcbd" : SYMMETRIC_LABELLED_BOUNDED_DESCRIPTION,
}

class SparqlClient:
  endpoint = None
  client = None
  output_parameter_name = None
  graphs = None
  named_graphs = None
  supports_rdf_json = False
  supports_sparql_json = True
  
  def __init__(self, endpoint, client=httplib2.Http()):
    self.endpoint = endpoint
    self.client = client
  
  def add_default_graph(self, graph_uri):
    if self.graphs is None:
      self.graphs = []
    self.graphs.append(graph_uri)
  
  def add_named_graph(self, graph_uri):
    if self.named_graphs is None:
      self.named_graphs = []
    self.named_graphs.append(graph_uri)
  
  def query(self, sparql, format=None, graphs=None, named_graphs=None):
    params = []
    params.append(("query", sparql))
    if graphs != None:
      for graph in graphs:
        params.append(("default-graph-uri", graph))
    elif self.graphs != None:
      for graph in self.graphs:
        params.append(("default-graph-uri", graph))
    if named_graphs != None:
      for named_graph in named_graphs:
        params.append(("named-graph-uri", named_graph))
    elif self.named_graphs != None:
      for named_graph in self.named_graphs:
        params.append(("named-graph-uri", named_graph))
    headers = {}
    if format != None:
      if self.output_parameter_name != None:
        params[self.output_parameter_name] = format
      else:
        headers["Accept"] = format
    return self.client.request(self.endpoint, "GET", urllib.urlencode(params), headers)
  
  def describe_uri(self, uri, format="application/rdf+xml", type="cbd"):
    try:
      template = DESCRIPTIONS[type]
    except KeyError:
      raise "Unknown description type"
    query = template.replace("?uri", "<%s>" % uri)
    return self.describe(query, format)
  
  def describe(self, query, format="application/rdf+xml"):
    return self.query(query, format)

  def multi_describe(self, uris, format="application/rdf+xml"):
    query = "DESCRIBE" + " ".join(["<%s>" % u for u in uris])
    return self.query(query, format)
  
  def construct(self, query, format="application/rdf+xml"):
    return self.query(query, format)
  
  def ask(self, query, format=SPARQL_RESULTS_XML):
    return self.query(query, format)
  
  def select(self, query, format=SPARQL_RESULTS_XML):
    return self.query(query, format)

def merge(sparql_client, store, query):
  headers, data = sparql_client.query(query, "application/rdf+xml")
  if headers["status"] != "200":
    raise "Unable to execute query. Response: %s" % headers["status"]
  resp = store.store_data(data)
  return resp

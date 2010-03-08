import rdflib.graph, rdflib.term, rdflib.namespace, os
DEFAULT_RDFFILE = os.path.join(os.path.dirname(__file__), "..", "..", "etc", "entitymatcher_types.rdf")
class EntityMatcher:
	def __init__(self, rdffile=DEFAULT_RDFFILE):
		self.graph = rdflib.graph.Graph()
		self.graph.parse(rdffile)
	def get_matches(self, names, type=None, default=None):
		uris = []
		for name in names:
			uris.append(self.lookup(name, type, default))
		return uris
	#~ def lookup(self, name, type=None, default=None):
		#~ name = rdflib.term.Literal(name.capitalize())
		#~ if type is None:
			#~ rows = self.graph.query("SELECT ?uri WHERE {?uri rdfs:label ?name.}", initNs=dict(
				#~ rdfs=rdflib.namespace.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
			#~ ), initBindings=dict(name=name))
		#~ else:
			#~ type = rdflib.term.URIRef("http://example.com/entitymatcher/types/" + type.capitalize())
			#~ rows = self.graph.query("SELECT ?uri WHERE {?uri rdfs:label ?name. ?uri rdf:type ?type.}", initNs=dict(
				#~ rdfs=rdflib.namespace.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
				#~ rdf=rdflib.namespace.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
			#~ ), initBindings=dict(name=name, type=type))
		#~ l = list(rows)
		#~ if len(l):
			#~ return str(l[0])
		#~ else:
			#~ return default

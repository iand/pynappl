"""sparql_select_result.py
Data structure for storing the results of SPARQL SELECT queries"""
__all__ = ["SPARQLSelectResult"]
from xml.etree import ElementTree as et
class SPARQLSelectResult(object):
	def __init__(self):
		self.variables = []
		self.results = []
	def parse(self, s):
		tree = et.fromstring(s)
		head = tree.find("{http://www.w3.org/2005/sparql-results#}head")
		self.variables = [x.get("name") for x in head.findall("{http://www.w3.org/2005/sparql-results#}variable")]
		results = tree.find("{http://www.w3.org/2005/sparql-results#}results").findall("{http://www.w3.org/2005/sparql-results#}result")
		self.results = []
		for result in results:
			d = {}
			bindings = result.findall("{http://www.w3.org/2005/sparql-results#}binding")
			for binding in bindings:
				uri = binding.find("{http://www.w3.org/2005/sparql-results#}uri")
				if uri is None:
					literal = binding.find("{http://www.w3.org/2005/sparql-results#}literal")
					if literal is None:
						raise InvalidSPARQLSelectResultSyntax("Neither URI or Literal were found")
					else:
						d[binding.get("name")] = (literal.text, None, None)
				else:
					d[binding.get("name")] = uri.text
			self.results.append(d)
	def get_variables(self):
		return self.variables
	def get_results(self):
		return self.results

# store_config.py - class representing Talis Platform store configuration
# Copyright (C) 2009 Talis Information Ltd.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	02110-1301 USA

__all__ = ["StoreConfig", "FieldPredicateMap", "QueryProfile"]
import re
import rdflib

FRAME = rdflib.Namespace("http://schemas.talis.com/2006/frame/schema#")
BF = rdflib.Namespace("http://schemas.talis.com/2006/bigfoot/configuration#")



class StoreConfig:
		def __init__(self, uri):
			self.uri = uri

		def get_first_fpmap_uri(self):
			matches = re.match(r"^http:\/\/api\.talis\.com\/stores\/([a-z][a-zA-Z0-9-]+)\/config$", self.uri)
			if matches is not None:
				store_name = matches.group(1);    
    
				# special cases for very very early stores
				if store_name in ['ajmg-dev1','beobal-dev1', 'danja-dev1', 'dataMonitoring', 'iand-dev1', 'iand-dev2', 'iand-dev3', 'jingye-dev1', 'kwijibo-dev1', 'malcyl-dev1', 'quoll-dev1', 'schema-cache', 'silkworm-dev', 'silkworm', 'source-dev1', 'source-qa1', 'tomh-dev1']:
					return 'http://api.talis.com/stores/%s/indexes/default/fpmaps/default' % store_name
				elif ( re.search(r"^engage-dev\d+$", store_name) is not None
						or re.search(r"^engagetenant\d+$", store_name) is not None  
						or re.search(r"^list-demo\d+$", store_name) is not None 
						or re.search(r"^list-dev\d+$", store_name) is not None 
						or re.search(r"^list-qa\d+$", store_name) is not None  
						or re.search(r"^nuggetengage-demo\d+$", store_name) is not None    
						or re.search(r"^nuggetengage-qa\d+$", store_name) is not None 
						or re.search(r"^zephyr-cust\d+$", store_name) is not None    
						or store_name in ['engagetenantstore', 'list-tenants-dev']   ):
					return 'http://api.talis.com/stores/%s/indexes/metaboxIndex/fpmaps/fpmap' % store_name
				elif store_name in ['bib-sandbox', 'inst-5050', 'inst-u138', 'ukbib']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/fpmaps/fpmap' % store_name
				elif store_name in ['holdings']:
					return 'http://api.talis.com/stores/%s/indexes/m21Holdings/fpmaps/fpmap' % store_name
				elif store_name in ['union']:
					return 'http://api.talis.com/stores/%s/indexes/union/fpmaps/fpmap' % store_name
				elif store_name in ['wikipedia']:
					return 'http://api.talis.com/stores/%s/indexes/abstracts/fpmaps/fpmap' % store_name
				elif store_name in ['gatech']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/fpmap' % store_name
				elif store_name in ['cenotelist']:
					return 'http://api.talis.com/stores/%s/indexes/default/fpmaps/fpmap' % store_name
				elif store_name in ['image-sandbox']:
					return 'http://api.talis.com/stores/%s/indexes/image-sandbox/fpmaps/fpmap' % store_name
				elif store_name in ['cnimages']:
					return 'http://api.talis.com/stores/%s/indexes/cnimages/fpmaps/fpmap' % store_name
			return '%s/fpmaps/1' % self.uri
			
		def get_first_query_profile_uri(self):
			matches = re.match(r"^http:\/\/api\.talis\.com\/stores\/([a-z][a-zA-Z0-9-]+)\/config$", self.uri)
			if matches is not None:
				store_name = matches.group(1);    
    
				# special cases for very very early stores
				if store_name in ['ajmg-dev1','beobal-dev1', 'danja-dev1', 'dataMonitoring', 'iand-dev1', 'iand-dev2', 'iand-dev3', 'jingye-dev1', 'kwijibo-dev1', 'malcyl-dev1', 'quoll-dev1', 'schema-cache', 'silkworm-dev', 'silkworm', 'source-dev1', 'source-qa1', 'tomh-dev1']:
					return 'http://api.talis.com/stores/%s/indexes/default/queryprofiles/default' % store_name
				elif ( re.search(r"^engage-dev\d+$", store_name) is not None
						or re.search(r"^engagetenant\d+$", store_name) is not None  
						or re.search(r"^list-demo\d+$", store_name) is not None 
						or re.search(r"^list-dev\d+$", store_name) is not None 
						or re.search(r"^list-qa\d+$", store_name) is not None  
						or re.search(r"^nuggetengage-demo\d+$", store_name) is not None    
						or re.search(r"^nuggetengage-qa\d+$", store_name) is not None 
						or re.search(r"^zephyr-cust\d+$", store_name) is not None    
						or store_name in ['engagetenantstore', 'list-tenants-dev']   ):
					return 'http://api.talis.com/stores/%s/indexes/metaboxIndex/queryprofiles/default' % store_name
				elif store_name in ['bib-sandbox', 'inst-5050', 'inst-u138', 'ukbib']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/queryprofiles/default' % store_name
				elif store_name in ['holdings']:
					return 'http://api.talis.com/stores/%s/indexes/m21Holdings/queryprofiles/default' % store_name
				elif store_name in ['union']:
					return 'http://api.talis.com/stores/%s/indexes/union/queryprofiles/default' % store_name
				elif store_name in ['wikipedia']:
					return 'http://api.talis.com/stores/%s/indexes/abstracts/queryprofiles/default' % store_name
				elif store_name in ['gatech']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/queryprofiles/default' % store_name
				elif store_name in ['cenotelist']:
					return 'http://api.talis.com/stores/%s/indexes/default/queryprofiles/default' % store_name
				elif store_name in ['image-sandbox']:
					return 'http://api.talis.com/stores/%s/indexes/image-sandbox/queryprofiles/default' % store_name
				elif store_name in ['cnimages']:
					return 'http://api.talis.com/stores/%s/indexes/cnimages/queryprofiles/default' % store_name
			return '%s/queryprofiles/1' % self.uri
			

class FieldPredicateMap():
	def __init__(self, uri):
		self.uri = uri
		self.init_graph()
		
	def init_graph(self):
		self.g = rdflib.ConjunctiveGraph()
		self.g.bind('frm', FRAME)
		self.g.bind('bf', BF)
		
	def add_mapping(self, property, name, analyzer = None):
		self.remove_mapping(property)
		mapping_uri = "%s#%s" % (self.uri, name)
		self.g.add( (rdflib.URIRef(self.uri), FRAME["mappedDatatypeProperty"], rdflib.URIRef(mapping_uri) ) )
		self.g.add( (rdflib.URIRef(mapping_uri), FRAME["property"], rdflib.URIRef(property) ) )
		self.g.add( (rdflib.URIRef(mapping_uri), FRAME["name"], rdflib.Literal(name) ) )
		if analyzer is not None:
			self.g.add( (rdflib.URIRef(mapping_uri), BF["analyzer"], rdflib.URIRef(analyzer) ) )
		
		return mapping_uri
		
		
	def remove_mapping(self, property):
		for (s, p, o) in self.g.triples( (None, FRAME["property"], rdflib.URIRef(property)) ):
			self.g.remove( (None, None, s) )
			self.g.remove( (s, None, None) )
			return
	
	def mappings(self):
		mapping_list = {}
		for (s, p, o) in self.g.triples( (rdflib.URIRef(self.uri), FRAME["mappedDatatypeProperty"], None) ):
			names = list(self.g.objects( subject = o, predicate = FRAME["name"] ) ) 
			properties = list(self.g.objects( subject = o, predicate = FRAME["property"] ) ) 
			
			if len(names) == 1 and len(properties) == 1:
				mapping_list[str(properties[0])] = { 'name' : str(names[0]) }
		return mapping_list
	

	def graph(self):
		return self.g
		
	def from_rdfxml(self, data):
		self.init_graph()
		self.g.parse(rdflib.StringInputSource(data), format="xml")


class QueryProfile():
	def __init__(self, uri):
		self.uri = uri
		self.init_graph()
		
	def init_graph(self):
		self.g = rdflib.ConjunctiveGraph()
		self.g.bind('frm', FRAME)
		self.g.bind('bf', BF)

	def graph(self):
		return self.g
		
	def from_rdfxml(self, data):
		self.init_graph()
		self.g.parse(rdflib.StringInputSource(data), format="xml")

	def add_field_weight(self, name, weight):
		self.remove_field_weight(name)
		weight_uri = "%s#%s" % (self.uri, name)
		self.g.add( (rdflib.URIRef(self.uri), BF["fieldWeight"], rdflib.URIRef(weight_uri) ) )
		self.g.add( (rdflib.URIRef(weight_uri), BF["weight"], rdflib.Literal(weight) ) )
		self.g.add( (rdflib.URIRef(weight_uri), FRAME["name"], rdflib.Literal(name) ) )
		return weight_uri

	def remove_field_weight(self, name):
		for (s, p, o) in self.g.triples( (None, FRAME["name"], rdflib.Literal(name)) ):
			self.g.remove( (None, None, s) )
			self.g.remove( (s, None, None) )
			return

	def weights(self):
		weight_list = {}
		for (s, p, o) in self.g.triples( (rdflib.URIRef(self.uri), BF["fieldWeight"], None) ):
			names = list(self.g.objects( subject = o, predicate = FRAME["name"] ) ) 
			weights = list(self.g.objects( subject = o, predicate = BF["weight"] ) ) 
			
			if len(names) == 1 and len(weights) == 1:
				weight_list[str(names[0])] = str(weights[0])
		return weight_list

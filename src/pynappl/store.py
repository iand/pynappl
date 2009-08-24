# store.py - facade for accessing Talis Platform stores
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

__all__ = ["Store"]

import httplib2
import urllib
import rdflib
import datetime as dt
import pynappl
import xml.etree.ElementTree as et

class Store:
		def __init__(self,uri, username = None, password = None, client = None):
			if client is None:
				self.client = httplib2.Http()
			else:
				self.client = client
				
			if password is not None and username is not None:
				self.client.add_credentials(username, password)

			self.uri = uri.endswith("/") and uri[:-1] or uri
			self.username = username

		def store_data(self, data, graph_name=None):
			"""Store some RDF in the Metabox associated with this store. Default is to store the
				 data in the metabox, but a private graph name can also be specified."""		

			req_uri = None
			if graph_name is None:
				req_uri = self.build_uri("/meta")
			else:
				req_uri = self.build_uri("/meta/graphs/%s" % graph_name)	
			
			return self.client.request(req_uri, "POST", body=data, headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})
		
		def store_file(self, filename, graph_name=None):
			"""Store the contents of a File (file-like object) in the Metabox associated with this store
				 The client does not support streaming submissions of data, so the stream will be fully read before data is submitted to the platform
				 file:: an IO object			
			"""
			file = open(filename, 'r')
			data = file.read()
			file.close()
			return self.store_data(data, graph_name)

		def store_graph(self, g, graph_name=None):
			"""Store the contents of an rdflib.ConjuctiveGraph in the Metabox associated with this store"""
			data = g.serialize(format='xml')
			return self.store_data(data, graph_name)

		def store_url(self, url, graph_name=None):
			"""Store the result of fetching a URL in the Metabox associated with this store"""
			(response, body) = self.client.request(url, "GET", headers={"accept" : "application/rdf+xml, application/xml;q=0.1, text/xml;q=0.1"})
			
			if response.status > 299:
				raise "Unable to read data from %s. Response was %s %s " % (url, response.status, response.reason) 
			return self.store_data(body, graph_name)


		def build_uri(self, uri):
			"""Build a request uri, by concatenating it with the base uri of the store
					uri:: relative URI to store service, e.g. "/service/sparql"
			"""
			if (uri.startswith(self.uri)):
				return uri
			if uri.startswith("/"):
				return self.uri + uri
			else:
				return self.uri + "/" + uri


		def get_jobs(self):
			req_uri = self.build_uri("/jobs")
			return self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})

		def response_body_as_graph(self, response, body, format="xml"):
			g = rdflib.ConjunctiveGraph()
			if response.status < 300:
				g.parse(rdflib.StringInputSource(body), format=format)
			return (response, g)

		def describe(self, uri, raw = False):
			req_uri = self.build_uri('meta?about=' + urllib.quote_plus(uri))
			(response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})
			if raw:
				return (response, body)
			else:
				return self.response_body_as_graph(response, body)

		def schedule_job(self, type, time, label, snapshot_uri = None):
			if time is None:
				time = dt.datetime.utcnow()
			if label is None:
				label = ''
			g = rdflib.ConjunctiveGraph();
			
			s = rdflib.URIRef('')
			g.add( (s, rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#JobRequest')) )
			g.add( (s, rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label'), rdflib.Literal(label)) )
			g.add( (s, rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType'), rdflib.URIRef(type)) )
			g.add( (s, rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime'), rdflib.Literal(time.strftime('%Y-%m-%dT%H:%M:%SZ') )) )
			if snapshot_uri is not None:
				g.add( (s, rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#snapshotUri'), rdflib.URIRef(snapshot_uri)) )
				
			body = g.serialize(format='xml')
			
			req_uri = self.build_uri("/jobs")
			return self.client.request(req_uri, "POST", body=body, headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})

		def schedule_reset(self, time=dt.datetime.utcnow(), label='Reset data job created by pynappl client'):
			"""Schedule an offline job to reset the data in a store"""
			return self.schedule_job(pynappl.JOB_TYPE_RESET, time, label)
			
		def schedule_snapshot(self, time=dt.datetime.utcnow(), label='Snapshot job created by pynappl client'):
			"""Schedule an offline job to create a snapshot of the data in a store"""
			return self.schedule_job(pynappl.JOB_TYPE_SNAPSHOT, time, label)

		def schedule_reindex(self, time=dt.datetime.utcnow(), label='Reindex job created by pynappl client'):
			"""Schedule an offline job to reindex the data in a store"""
			return self.schedule_job(pynappl.JOB_TYPE_REINDEX, time, label)

		def schedule_restore(self, snapshot_uri, time=dt.datetime.utcnow(), label='Restore job created by pynappl client'):
			"""Schedule an offline job to restore a snapshot to a store"""
			return self.schedule_job(pynappl.JOB_TYPE_RESTORE, time, label, snapshot_uri)
			
		def read_job(self, uri, raw=False):
			(response, body) = self.client.request(uri, "GET", headers={"accept" : "application/rdf+xml"})
			if raw:
				return (response, body)
			else:
				return (response, pynappl.Job.parse(uri, body))
			
		def is_writeable(self):
			req_uri = self.build_uri("/config/access-status")
			(response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"}, )
			if response.status < 300:
				g = rdflib.ConjunctiveGraph();
				g.parse(rdflib.StringInputSource(body), format="xml")
				access_status_values = list(g.objects(subject = rdflib.URIRef(req_uri), predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
				return len(access_status_values) > 0 and str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-write'

			return False

		def is_readable(self):
			req_uri = self.build_uri("/config/access-status")
			(response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"}, )
			if response.status < 300:
				g = rdflib.ConjunctiveGraph();
				g.parse(rdflib.StringInputSource(body), format="xml")
				access_status_values = list(g.objects(subject = rdflib.URIRef(req_uri), predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
				return len(access_status_values) > 0 and (str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-write' or str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-only')

			return False

		def status(self, raw = False):
			req_uri = self.build_uri("/config/access-status")
			(response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"}, )
			if raw:
				return (response, body)
			if response.status < 300:
				g = rdflib.ConjunctiveGraph();
				g.parse(rdflib.StringInputSource(body), format="xml")
				status = "store is "
				access_status_values = list(g.objects(subject = rdflib.URIRef(req_uri), predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
				if len(access_status_values) > 0:
					if str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-write':
						status += "read/write"
					elif str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-only':
						status += "read only"
					elif str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#unavailable':
						status += "unavailable"
					else:
						status = "in an unknown status"
				access_status_messages = list(g.objects(subject = rdflib.URIRef(req_uri), predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#statusMessage')))
				if len(access_status_messages) > 0 and len(str(access_status_messages[0])) > 0:
						status += " (" + str(access_status_messages[0]) + ")"
				return (response, status)
			return (response, "")

		def search(self, query, raw=False):
			req_uri = self.build_uri("/items?query=" + urllib.quote_plus(query))
			return self.client.request(req_uri, "GET", headers={"accept" : "application/rss+xml"})

		def sparql(self, query):
			req_uri = self.build_uri("/services/sparql?query=" + urllib.quote_plus(query))
			return self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml,application/sparql-results+xml"})
		
		def select(self, query, raw = False):
			response, body = self.sparql(query)
			if raw:
				return response, body
			if response.status in range(200, 300):
				results = []
				tree = et.fromstring(body)
				for result in tree.find("{http://www.w3.org/2005/sparql-results#}results").findall("{http://www.w3.org/2005/sparql-results#}result"):
					d = {}
					for binding in result.findall("{http://www.w3.org/2005/sparql-results#}binding"):
						name = binding.get("name")
						value = None
						uri = binding.find("{http://www.w3.org/2005/sparql-results#}uri")
						if uri is None:
							literal = binding.find("{http://www.w3.org/2005/sparql-results#}literal")
							if literal is None:
								bnode = binding.find("{http://www.w3.org/2005/sparql-results#}bnode")
								if bnode is None:
									raise PynapplError("SPARQL select result binding value is not a URI, Literal or BNode")
								else:
									value = rdflib.BNode(bnode.text)
							else:
								value = rdflib.Literal(literal.text)
						else:
							value = rdflib.URIRef(uri.text)
						d[name] = value
					results.append(d)
				return response, results
			return response, body

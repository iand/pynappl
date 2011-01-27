# store.py - facade for accessing Talis Platform stores
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__all__ = ["Store"]

import httplib2
import urllib
from rdflib.graph import Graph
from rdflib.namespace import Namespace
from rdflib.term import URIRef, Literal, BNode
from rdflib.parser import StringInputSource
import datetime as dt
import StringIO
import pynappl
import xml.etree.ElementTree as et
import constants

class Store:
    def __init__(self,uri, username = None, password = None, client = None):
      if client is None:
        self.client = httplib2.Http()
        self.client.follow_all_redirects = True
      else:
        self.client = client
        
      if password is not None and username is not None:
        self.client.add_credentials(username, password)
      
      self.store_name = uri  # human-readable name
      if not uri.startswith(("http://", "https://")):
        uri = "http://api.talis.com/stores/" + uri

      self.uri = uri.endswith("/") and uri[:-1] or uri
      self.username = username

    def store_data(self, data, graph_name=None, content_type='application/rdf+xml'):
      """Store some RDF in the Metabox associated with this store. Default is to store the
         data in the metabox, but a private graph name can also be specified."""    

      req_uri = None
      if graph_name is None:
        req_uri = self.build_uri("/meta")
      else:
        req_uri = self.build_uri("/meta/graphs/%s" % graph_name)  
      
      return self.client.request(req_uri, "POST", body=data, headers={"accept" : "*/*", 'content-type':content_type})
    
    def store_file(self, filename, graph_name=None, content_type=None):
      """Store the contents of a File (file-like object) in the Metabox associated with this store
         The client does not support streaming submissions of data, so the stream will be fully read before data is submitted to the platform
         file:: an IO object      
      """
      file = open(filename, 'r')
      data = file.read()
      file.close()
      
      if not content_type:
        if filename.endswith('.nt') or filename.endswith('.ttl'):
          content_type = 'text/turtle'
        else:
          content_type = 'application/rdf+xml'
      
      return self.store_data(data, graph_name, content_type)

    def store_graph(self, g, graph_name=None):
      """Store the contents of a Graph in the Metabox associated with this store"""
      data = g.serialize(format='xml')
      return self.store_data(data, graph_name,'application/rdf+xml')

    def store_url(self, url, graph_name=None):
      """Store the result of fetching a URL in the Metabox associated with this store"""
      (response, body) = self.client.request(url, "GET", headers={"accept" : "application/rdf+xml, application/xml;q=0.1, text/xml;q=0.1"})
      
      if response.status not in range (200,300):
        raise PynapplError("Unable to read data from %s. Response was %s %s " % (url, response.status, response.reason) )
      return self.store_data(body, graph_name)


    def apply_changeset(self, data, graph_name=None, content_type='application/vnd.talis.changeset+xml'):
      """Store some RDF in the Metabox associated with this store. Default is to store the
         data in the metabox, but a private graph name can also be specified."""    

      req_uri = None
      if graph_name is None:
        req_uri = self.build_uri("/meta")
      else:
        req_uri = self.build_uri("/meta/graphs/%s" % graph_name)  
      
      return self.client.request(req_uri, "POST", body=data, headers={"accept" : "*/*", 'content-type':content_type})


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
      g = Graph()
      if response.status in range (200,300):
        g.parse(StringInputSource(body), format=format)
      return (response, g)

    def describe(self, uri, raw = False):
      req_uri = self.build_uri('meta?about=' + urllib.quote_plus(uri))
      (response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})
      if raw:
        return (response, body)
      else:
        return self.response_body_as_graph(response, body)

    def schedule_job(self, type, time = None, label = None, snapshot_uri = None):
      if time is None:
        time = dt.datetime.utcnow()
      if label is None:
        label = 'Job created by pynappl client'
      g = Graph()
      
      s = BNode()
      g.add( (s, URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), URIRef('http://schemas.talis.com/2006/bigfoot/configuration#JobRequest')) )
      g.add( (s, URIRef('http://www.w3.org/2000/01/rdf-schema#label'), Literal(label)) )
      g.add( (s, URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType'), URIRef(type)) )
      g.add( (s, URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime'), Literal(time.strftime('%Y-%m-%dT%H:%M:%SZ') )) )
      if snapshot_uri is not None:
        g.add( (s, URIRef('http://schemas.talis.com/2006/bigfoot/configuration#snapshotUri'), URIRef(snapshot_uri)) )
        
      body = g.serialize(format='xml')
      
      #~ print body
      req_uri = self.build_uri("/jobs")
      return self.client.request(req_uri, "POST", body=body, headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})

    def schedule_reset(self, time=None, label='Reset data job created by pynappl client'):
      """Schedule an offline job to reset the data in a store"""
      return self.schedule_job(pynappl.JOB_TYPE_RESET, time, label)
      
    def schedule_snapshot(self, time=None, label='Snapshot job created by pynappl client'):
      """Schedule an offline job to create a snapshot of the data in a store"""
      return self.schedule_job(pynappl.JOB_TYPE_SNAPSHOT, time, label)

    def schedule_reindex(self, time=None, label='Reindex job created by pynappl client'):
      """Schedule an offline job to reindex the data in a store"""
      return self.schedule_job(pynappl.JOB_TYPE_REINDEX, time, label)

    def schedule_restore(self, snapshot_uri, time=None, label='Restore job created by pynappl client'):
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
        g = Graph();
        g.parse(StringInputSource(body), format="xml")
        access_status_values = list(g.objects(subject = URIRef(req_uri), predicate = URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
        return len(access_status_values) > 0 and str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-write'

      return False

    def is_readable(self):
      req_uri = self.build_uri("/config/access-status")
      (response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"}, )
      if response.status < 300:
        g = Graph();
        g.parse(StringInputSource(body), format="xml")
        access_status_values = list(g.objects(subject = URIRef(req_uri), predicate = URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
        return len(access_status_values) > 0 and (str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-write' or str(access_status_values[0]) == 'http://schemas.talis.com/2006/bigfoot/statuses#read-only')

      return False

    def status(self, raw = False):
      req_uri = self.build_uri("/config/access-status")
      (response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"}, )
      if raw:
        return (response, body)
      if response.status in range(200, 300):
        g = Graph();
        g.parse(StringInputSource(body), format="xml")
        status = "store is "
        access_status_values = list(g.objects(subject = URIRef(req_uri), predicate = URIRef('http://schemas.talis.com/2006/bigfoot/configuration#accessMode')))
        if len(access_status_values) > 0:
          if str(access_status_values[0]) == constants.STATUS_RW:
            status += "read/write"
          elif str(access_status_values[0]) == constants.STATUS_R:
            status += "read only"
          elif str(access_status_values[0]) == constants.STATUS_U:
            status += "unavailable"
          else:
            status += "in an unknown status"
        access_status_messages = list(g.objects(subject = URIRef(req_uri), predicate = URIRef('http://schemas.talis.com/2006/bigfoot/configuration#statusMessage')))
        if len(access_status_messages) > 0 and len(str(access_status_messages[0])) > 0:
          status += " (" + str(access_status_messages[0]) + ")"
        return (response, status)
      return (response, "")

    def search(self, query, raw=False, return_graph=False):
      req_uri = self.build_uri("/items?query=" + urllib.quote_plus(query))
      response, body = self.client.request(req_uri, "GET", headers={"accept" : "application/rss+xml"})
      if raw:
        return response, body
      if response.status in range(200, 300):
        RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        RSS = Namespace("http://purl.org/rss/1.0/")
        g = Graph()
        g.parse(StringIO.StringIO(body))
        search_uri = URIRef(req_uri)
        list = g.objects(search_uri, RSS.items).next()
        results = []
        for p, bn in g.predicate_objects(list):
          if p != RDF.type:
            o = g.objects(bn, URIRef("resource")).next()
            results.append(URIRef(o))
        if return_graph:
          results = (g, results)
        return response, results
      else:
        return response, body

    def sparql(self, query):
      req_uri = self.build_uri("/services/sparql?query=" + urllib.quote_plus(query))
      return self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml,application/sparql-results+xml"})
    
    def ask(self, query, raw = False):
      response, body = self.sparql(query)
      if raw:
        return response, body
      if response.status in range(200, 300):
        tree = et.fromstring(body)
        boolean = tree.find("{http://www.w3.org/2005/sparql-results#}boolean")
        return response, boolean.text == "true"
      return response, body
    
    def select(self, query, raw = False):
      response, body = self.sparql(query)
      if raw:
        return response, body
      if response.status in range(200, 300):
        tree = et.fromstring(body)
        head = tree.find("{http://www.w3.org/2005/sparql-results#}head")
        headers = [x.get("name") for x in head.findall("{http://www.w3.org/2005/sparql-results#}variable")]
        results = []
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
                  value = BNode(bnode.text)
              else:
                value = Literal(literal.text)
            else:
              value = URIRef(uri.text)
            d[name] = value
          results.append(d)
        return response, (headers, results)
      return response, body


    def snapshots(self, raw=False):
      """Retrieve a list of snapshots"""
      req_uri = self.build_uri("/snapshots")
      (response, body) = self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})
      if raw:
        return (response, body)
      else:
        snapshot_list = []  
        if response.status in range(200,300):
          g = Graph();
          g.parse(StringInputSource(body), format="xml")
          for snapshot_res in g.objects(subject = URIRef(self.uri), predicate = URIRef('http://schemas.talis.com/2006/bigfoot/configuration#snapshot')):
            snapshot_list.append(str(snapshot_res))
        return (response, snapshot_list)
        
    def get_config(self):
      return pynappl.StoreConfig(self.build_uri("/config"))
        
    def read_fpmap(self, raw=False):
      """Retrieve the field/predicate map (the first one if there are multiple)"""
      config = self.get_config()
      fpmap_uri = config.get_first_fpmap_uri()
      (response, body) = self.client.request(fpmap_uri, "GET", headers={"accept" : "application/rdf+xml"})
      if raw:
        return (response, body)
      else:
        fpmap = pynappl.FieldPredicateMap(fpmap_uri)
        if response.status in range(200,300):
          fpmap.from_rdfxml(body)
        return (response, fpmap)

    def write_fpmap(self, fpmap):
      config = self.get_config()
      fpmap_uri = config.get_first_fpmap_uri()
      return self.client.request(fpmap_uri, "PUT", body=fpmap.to_rdfxml(), headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})
        
    def read_query_profile(self, raw=False):
      """Retrieve the field/predicate map (the first one if there are multiple)"""
      config = self.get_config()
      qp_uri = config.get_first_query_profile_uri()
      (response, body) = self.client.request(qp_uri, "GET", headers={"accept" : "application/rdf+xml"})
      if raw:
        return (response, body)
      else:
        qp = pynappl.QueryProfile(qp_uri)
        if response.status in range(200,300):
          qp.from_rdfxml(body)
        return (response, qp)

    def write_query_profile(self, qprofile):
      config = self.get_config()
      qprofile_uri = config.get_first_query_profile_uri()
      return self.client.request(qprofile_uri, "PUT", body=qprofile.to_rdfxml(), headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})

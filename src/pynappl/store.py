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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

__all__ = ["Store"]

import httplib2
import urllib
import rdflib
import datetime as dt
import pynappl

class Store:
    def __init__(self,uri, user = None, pwd = None, client = None):
      if client is None:
        self.client = httplib2.Http()
      else:
        self.client = client
      self.storeuri = uri
      self.user = user
      self.pwd = pwd

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
      if (uri.startswith(self.storeuri)):
        return uri
      if uri.startswith("/"):
        return self.storeuri + uri
      else:
        return self.storeuri + "/" + uri


    def get_jobs(self):
      req_uri = self.build_uri("/jobs")
      return self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})

    def describe(self, uri):
      req_uri = self.build_uri('meta?about=' + urllib.quote_plus(uri))
      return self.client.request(req_uri, "GET", headers={"accept" : "application/rdf+xml"})

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
      self.schedule_job(pynappl.JOB_TYPE_RESET, time, label)
      
    def schedule_snapshot(self, time=dt.datetime.utcnow(), label='Snapshot job created by pynappl client'):
      self.schedule_job(pynappl.JOB_TYPE_SNAPSHOT, time, label)

    def schedule_reindex(self, time=dt.datetime.utcnow(), label='Snapshot job created by pynappl client'):
      self.schedule_job(pynappl.JOB_TYPE_REINDEX, time, label)

    def schedule_restore(self, snapshot_uri, time=dt.datetime.utcnow(), label='Snapshot job created by pynappl client'):
      self.schedule_job(pynappl.JOB_TYPE_RESTORE, time, label, snapshot_uri)
      
    def read_job(self, uri):
      (response, body) = self.client.request(uri, "GET", headers={"accept" : "application/rdf+xml"})
      if response.status > 299:
        raise "Unable to read job from store. Response was %s %s " % (response.status, response.reason) 

      return pynappl.Job.parse(uri, body)
      

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
         data in the metabox, but a private graph name can also be specified.
    
         data:: a String containing the data to store
         graph_name:: name of a private graph in which to store the data. E.g. "1" or "private". Resolves to /meta/graphs/graph_name
      """
    
      req_uri = None
      if graph_name is None:
        req_uri = self.build_uri("/meta")
      else:
        req_uri = self.build_uri("/meta/graphs/%s" % graph_name)  
      
      return self.client.request(req_uri, "POST", body=data, headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})
    
    def store_file(self, file, graph_name=None):
      """Store the contents of a File (or any IO stream) in the Metabox associated with this store
         The client does not support streaming submissions of data, so the stream will be fully read before data is submitted to the platform
         file:: an IO object      
      """
      data = file.read()
      file.close()
      return store_data(data)

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
      # TODO: check result is OK, then pass to Job.Parse
      

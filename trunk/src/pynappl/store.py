import httplib2
import urllib

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
    
      uri = None
      if graph_name is None:
        uri = build_uri("/meta")
      else:
        uri = build_uri("/meta/graphs/%s" % graph_name)  
      
      # TODO
      #response = @client.post(u, data, RDF_XML )
      #return response
    
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

    def schedule_reset(self):
      req_uri = self.build_uri("/jobs")
      return self.client.request(req_uri, "POST", headers={"accept" : "*/*", 'content-type':'application/rdf+xml'})

    def read_job(self, uri):
      (response, body) = self.client.request(uri, "GET", headers={"accept" : "application/rdf+xml"})
      # TODO: check result is OK, then pass to Job.Parse
      

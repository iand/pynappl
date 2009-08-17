import httplib2
class MockHttp(httplib2.Http):
  responses = {}
  requests = {}

  def register_response(self, method, uri, headers, body):
    self.responses[(method.lower(), uri)] = (headers, body)

  def request(self, uri, method, body=None, headers={}):
    self.requests[(method.lower(), uri)] = (headers, body)
    if self.responses.has_key( (method.lower(), uri) ):
      return self.responses[(method, uri)]
    else:
      return None

  def received_request(self, method, uri):
    return self.requests.has_key( (method.lower(), uri) )
    
  def get_request(self, method, uri):
    return self.requests[(method.lower(), uri)]

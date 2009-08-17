import httplib2
class MockHttp(httplib2.Http):

  def __init__(self):
    self.responses = {}
    self.requests = {}

  def register(self, method, uri, body = '', response = httplib2.Response({})):
    self.responses[(method.lower(), uri)] = (response, body)

  def request(self, uri, method, body=None, headers={}):
    self.requests[(method.lower(), uri)] = (headers, body)
    if self.responses.has_key( (method.lower(), uri) ):
      return self.responses[(method.lower(), uri)]
    else:
      return (httplib2.Response({}), '')

  def received_request(self, method, uri):
    return self.requests.has_key( (method.lower(), uri) )
    
  def get_request(self, method, uri):
    return self.requests[(method.lower(), uri)]

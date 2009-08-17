import httplib2
class MockHttp(httplib2.Http):
	responses = {}
	def register_response(self, method, uri, headers, body):
		self.responses[(method, uri)] = (headers, body)
	def request(self, uri, method, body=None, headers={}):
		return self.responses[(method, uri)]

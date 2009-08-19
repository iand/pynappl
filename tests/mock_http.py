# mock_http.py - mock version of httplib2.Http class
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

import httplib2
class MockHttp(httplib2.Http):

  def __init__(self):
    self.responses = {}
    self.requests = {}
    self.username = None
    self.password = None

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

  def add_credentials(self, username, password):
    self.username = username
    self.password = password

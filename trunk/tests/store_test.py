import unittest
import pynappl
import urllib
from mock_http import MockHttp

class BuildUriTestCase(unittest.TestCase):

  def test_build_uri_abs(self):
    """build_uri returns absolute URIs if they are in store's URI space"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('http://example.com/store/foo'))

  def test_build_uri_rel(self):
    """build_uri appends relative URIs to the store URI"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('/foo'))

  def test_build_uri_rel_slashless(self):
    """build_uri ensures relative URIs are appended with a slash"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('foo'))
    

class DescribeTestCase(unittest.TestCase):

  def test_describe_single_uri_performs_get_on_metabox(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.describe('http://example.com/foo')
    self.assertTrue(client.received_request('get', 'http://example.com/store/meta?about=' + urllib.quote_plus('http://example.com/foo')))


class ReadJobTestCase(unittest.TestCase):
  def test_read_job_issues_get(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    job = store.read_job('http://example.com/store/jobs/123456789')
    self.assertTrue(client.received_request('get', 'http://example.com/store/jobs/123456789'))

  def test_read_job_sets_accept(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    job = store.read_job('http://example.com/store/jobs/123456789')

    (headers, body) = client.get_request('get', 'http://example.com/store/jobs/123456789')
    self.assertTrue(headers.has_key('accept'))
    self.assertEqual('application/rdf+xml', headers['accept'])


class ScheduleResetTestCase(unittest.TestCase):
  def test_schedule_reset_posts_to_job_queue_uri(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.schedule_reset()
    self.assertTrue(client.received_request('post', 'http://example.com/store/jobs'))

  def test_schedule_reset_sets_content_type(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.schedule_reset()

    (headers, body) = client.get_request('post', 'http://example.com/store/jobs')
    self.assertTrue(headers.has_key('content-type'))
    self.assertEqual('application/rdf+xml', headers['content-type'])

  def test_schedule_reset_sets_accept(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.schedule_reset()
    (headers, body) = client.get_request('post', 'http://example.com/store/jobs')
    self.assertTrue(headers.has_key('accept'))
    self.assertEqual('*/*', headers['accept'])
  



if __name__ == "__main__":
    unittest.main()



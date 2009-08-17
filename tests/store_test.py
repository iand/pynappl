import unittest
import pynappl
import urllib
import rdflib
import datetime as dt

from StringIO import StringIO


from mock_http import MockHttp

SINGLE_TRIPLE = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:foaf="http://xmlns.com/foaf/0.1/"><rdf:Description><foaf:name>scooby</foaf:name></rdf:Description></rdf:RDF>'

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

class ScheduleJobTestCase(unittest.TestCase):
  def submit_job(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = self.do_schedule(store)
    (header, body) = client.get_request('post', 'http://example.com/store/jobs')
    return (client, header, body)
    
  def parse_job_request(self, body):
    g = rdflib.ConjunctiveGraph()
    g.parse(StringIO(body), format="xml")
    return g

  def do_schedule(self, store, time=None, label=None):
    pass

  def post_job_and_get_graph(self):
    (client, headers, body) = self.submit_job();
    return self.parse_job_request(body)

  def test_schedule_job_posts_to_job_queue_uri(self):
    (client, headers, body) = self.submit_job()
    self.assertTrue(client.received_request('post', 'http://example.com/store/jobs'))

  def test_schedule_job_sets_content_type(self):
    (client, headers, body) = self.submit_job()
    self.assertTrue(headers.has_key('content-type'))
    self.assertEqual('application/rdf+xml', headers['content-type'])

  def test_schedule_job_sets_accept(self):
    (client, headers, body) = self.submit_job()
    self.assertTrue(headers.has_key('accept'))
    self.assertEqual('*/*', headers['accept'])
    
  def test_schedule_job_posts_rdfxml_where_triples_all_have_same_subject(self):
    g = self.post_job_and_get_graph()
    subj = None
    for s in g.subjects():
      if subj is None:
        self.assertTrue(True)
        subj = s
      else:
        self.assertEqual(subj, s)

  def test_schedule_job_posts_rdfxml_with_a_single_jobtype(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
    self.assertEqual(1, len(objects))

  def test_schedule_job_rdfxml_with_a_single_start_time(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime')))
    self.assertEqual(1, len(objects))

  def test_schedule_job_rdfxml_with_a_type_of_job_request(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#JobRequest', str(objects[0]))


  def test_schedule_job_posts_rdfxml_with_supplied_label(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = self.do_schedule(store, label='My job')
    (headers, body) = client.get_request('post', 'http://example.com/store/jobs')

    g = self.parse_job_request(body)
    
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label')))
    self.assertEqual(1, len(objects))
    self.assertEqual('My job', str(objects[0]))

  def test_schedule_job_posts_rdfxml_with_supplied_start_time(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = self.do_schedule(store, time=dt.datetime(2008, 7, 6, 5, 4, 3))
    (headers, body) = client.get_request('post', 'http://example.com/store/jobs')

    g = self.parse_job_request(body)
    
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime')))
    self.assertEqual(1, len(objects))
    self.assertEqual('2008-07-06T05:04:03Z', str(objects[0]))


class ScheduleResetTestCase(ScheduleJobTestCase):

  def do_schedule(self, store, time=None, label=None):
    return store.schedule_reset(time, label)

  def test_schedule_reset_data_posts_rdfxml_with_a_job_type_of_reset_data_job(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob', str(objects[0]))

class ScheduleSnapshotTestCase(ScheduleJobTestCase):
  def do_schedule(self, store, time=None, label=None):
    return store.schedule_snapshot(time, label)

  def test_schedule_reset_data_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#SnapshotJob', str(objects[0]))


class ScheduleReindexTestCase(ScheduleJobTestCase):
  def do_schedule(self, store, time=None, label=None):
    return store.schedule_reindex(time, label)

  def test_schedule_reindex_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#ReindexJob', str(objects[0]))

class ScheduleRestoreTestCase(ScheduleJobTestCase):
  def do_schedule(self, store, time=None, label=None):
    return store.schedule_restore('http://example.com/snapshot', time, label)

  def test_schedule_reindex_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#RestoreJob', str(objects[0]))

  def test_schedule_reindex_posts_rdfxml_with_supplied_snapshot_uri(self):
    g = self.post_job_and_get_graph()
    objects = list(g.objects(subject = None, predicate = rdflib.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#snapshotUri')))
    self.assertEqual(1, len(objects))
    self.assertEqual('http://example.com/snapshot', str(objects[0]))



class StoreDataTestCase(unittest.TestCase):
  def test_store_data_without_graph_posts_to_metabox(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE)
    self.assertTrue(client.received_request('post', 'http://example.com/store/meta'))

  def test_store_data_without_graph_sets_content_type(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE)

    (headers, body) = client.get_request('post', 'http://example.com/store/meta')
    self.assertTrue(headers.has_key('content-type'))
    self.assertEqual('application/rdf+xml', headers['content-type'])

  def test_store_data_without_graph_sets_accept(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE)

    (headers, body) = client.get_request('post', 'http://example.com/store/meta')
    self.assertTrue(headers.has_key('accept'))
    self.assertEqual('*/*', headers['accept'])

  def test_store_data_without_graph_sets_body(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE)

    (headers, body) = client.get_request('post', 'http://example.com/store/meta')
    self.assertEqual(SINGLE_TRIPLE, body)

  def test_store_data_with_graph_posts_to_graph(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE, 'foo')
    self.assertTrue(client.received_request('post', 'http://example.com/store/meta/graphs/foo'))

  def test_store_data_with_graph_sets_content_type(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE, 'foo')

    (headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
    self.assertTrue(headers.has_key('content-type'))
    self.assertEqual('application/rdf+xml', headers['content-type'])

  def test_store_data_with_graph_sets_accept(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE, 'foo')

    (headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
    self.assertTrue(headers.has_key('accept'))
    self.assertEqual('*/*', headers['accept'])

  def test_store_data_with_graph_sets_body(self):
    client = MockHttp()
    store = pynappl.Store('http://example.com/store', client=client)
    resp = store.store_data(SINGLE_TRIPLE, 'foo')

    (headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
    self.assertEqual(SINGLE_TRIPLE, body)


if __name__ == "__main__":
    unittest.main()



# store_test.py - unit tests for pynappl store class
# Copyright (C) 2009 Talis Information Ltd.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	02110-1301 USA

import unittest
import pynappl
import urllib
import httplib2
import rdflib.term, rdflib.graph
import datetime as dt
import tempfile
import os, os.path
from store_test_data import *

from StringIO import StringIO


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
		resp = store.describe('http://example.com/foo', True)
		self.assertTrue(client.received_request('get', 'http://example.com/store/meta?about=' + urllib.quote_plus('http://example.com/foo')))

class ReadJobTestCase(unittest.TestCase):
	def test_read_job_issues_get(self):
		client = MockHttp()
		client.register("get", JOB_URI, JOB_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		job = store.read_job(JOB_URI, True)
		self.assertTrue(client.received_request('get', JOB_URI))

	def test_read_job_sets_accept(self):
		client = MockHttp()
		client.register("get", JOB_URI, JOB_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		job = store.read_job(JOB_URI, True)

		(headers, body) = client.get_request('get', JOB_URI)
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
		g = rdflib.graph.ConjunctiveGraph()
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
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
		self.assertEqual(1, len(objects))

	def test_schedule_job_rdfxml_with_a_single_start_time(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime')))
		self.assertEqual(1, len(objects))

	def test_schedule_job_rdfxml_with_a_type_of_job_request(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')))
		self.assertEqual(1, len(objects))
		self.assertEqual('http://schemas.talis.com/2006/bigfoot/configuration#JobRequest', str(objects[0]))


	def test_schedule_job_posts_rdfxml_with_supplied_label(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = self.do_schedule(store, label='My job')
		(headers, body) = client.get_request('post', 'http://example.com/store/jobs')

		g = self.parse_job_request(body)
		
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label')))
		self.assertEqual(1, len(objects))
		self.assertEqual('My job', str(objects[0]))

	def test_schedule_job_posts_rdfxml_with_supplied_start_time(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = self.do_schedule(store, time=dt.datetime(2008, 7, 6, 5, 4, 3))
		(headers, body) = client.get_request('post', 'http://example.com/store/jobs')

		g = self.parse_job_request(body)
		
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#startTime')))
		self.assertEqual(1, len(objects))
		self.assertEqual('2008-07-06T05:04:03Z', str(objects[0]))


class ScheduleResetTestCase(ScheduleJobTestCase):

	def do_schedule(self, store, time=None, label=None):
		return store.schedule_reset(time, label)

	def test_schedule_reset_data_posts_rdfxml_with_a_job_type_of_reset_data_job(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
		self.assertEqual(1, len(objects))
		self.assertEqual(pynappl.JOB_TYPE_RESET, str(objects[0]))

class ScheduleSnapshotTestCase(ScheduleJobTestCase):
	def do_schedule(self, store, time=None, label=None):
		return store.schedule_snapshot(time, label)

	def test_schedule_reset_data_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
		self.assertEqual(1, len(objects))
		self.assertEqual(pynappl.JOB_TYPE_SNAPSHOT, str(objects[0]))


class ScheduleReindexTestCase(ScheduleJobTestCase):
	def do_schedule(self, store, time=None, label=None):
		return store.schedule_reindex(time, label)

	def test_schedule_reindex_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
		self.assertEqual(1, len(objects))
		self.assertEqual(pynappl.JOB_TYPE_REINDEX, str(objects[0]))

class ScheduleRestoreTestCase(ScheduleJobTestCase):
	def do_schedule(self, store, time=None, label=None):
		return store.schedule_restore('http://example.com/snapshot', time, label)

	def test_schedule_reindex_posts_rdfxml_with_a_job_type_of_snapshot_job(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#jobType')))
		self.assertEqual(1, len(objects))
		self.assertEqual(pynappl.JOB_TYPE_RESTORE, str(objects[0]))

	def test_schedule_reindex_posts_rdfxml_with_supplied_snapshot_uri(self):
		g = self.post_job_and_get_graph()
		objects = list(g.objects(subject = None, predicate = rdflib.term.URIRef('http://schemas.talis.com/2006/bigfoot/configuration#snapshotUri')))
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


	def test_store_data_with_content_type_sets_content_type(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_data(SINGLE_TRIPLE, content_type='text/turtle')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('text/turtle', headers['content-type'])


class StoreFileTestCase(unittest.TestCase):
	def setUp(self):
		self.file = tempfile.NamedTemporaryFile(delete=False)
		self.filename = self.file.name
		self.file.write(SINGLE_TRIPLE)
		self.file.close()

	def tearDown(self):
		os.remove(self.filename)
			
	def test_store_file_without_graph_posts_to_metabox(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename)
		self.assertTrue(client.received_request('post', 'http://example.com/store/meta'))

	def test_store_file_without_graph_sets_content_type(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_file_without_graph_sets_accept(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_file_without_graph_sets_body(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertEqual(SINGLE_TRIPLE, body)

	def test_store_file_with_graph_posts_to_graph(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename, 'foo')
		self.assertTrue(client.received_request('post', 'http://example.com/store/meta/graphs/foo'))

	def test_store_file_with_graph_sets_content_type(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_file_with_graph_sets_accept(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_file_with_graph_sets_body(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(self.filename, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertEqual(SINGLE_TRIPLE, body)
    
	def test_store_file_sets_content_type_from_filename(self):
		file = tempfile.NamedTemporaryFile(delete=False, suffix='.rdf')
		filename = file.name
		file.write(SINGLE_TRIPLE)
		file.close()

		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(filename)
		os.remove(filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])
    
	def test_store_file_sets_content_type_from_filename_nt(self):
		file = tempfile.NamedTemporaryFile(delete=False, suffix='.nt')
		filename = file.name
		file.write(SINGLE_TRIPLE)
		file.close()
    
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(filename)
		os.remove(filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('text/turtle', headers['content-type'])

	def test_store_file_sets_content_type_from_filename_ttl(self):
		file = tempfile.NamedTemporaryFile(delete=False, suffix='.ttl')
		filename = file.name
		file.write(SINGLE_TRIPLE)
		file.close()
    
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_file(filename)
		os.remove(filename)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('text/turtle', headers['content-type'])


class StoreGraphTestCase(unittest.TestCase):
	def setUp(self):
		self.graph = rdflib.graph.ConjunctiveGraph()
		self.graph.parse(StringIO(SINGLE_TRIPLE), format="xml")
	
	def is_isomorphic(self, data):
		g = rdflib.graph.ConjunctiveGraph()
		g.parse(StringIO(data), format="xml")
		return self.graph.isomorphic(g)
	
	def test_store_file_without_graph_posts_to_metabox(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph)
		self.assertTrue(client.received_request('post', 'http://example.com/store/meta'))

	def test_store_file_without_graph_sets_content_type(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_file_without_graph_sets_accept(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_file_without_graph_sets_body(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph)

		(headers, body) = client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(self.is_isomorphic(body))

	def test_store_file_with_graph_posts_to_graph(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph, 'foo')
		self.assertTrue(client.received_request('post', 'http://example.com/store/meta/graphs/foo'))

	def test_store_file_with_graph_sets_content_type(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_file_with_graph_sets_accept(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_file_with_graph_sets_body(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		resp = store.store_graph(self.graph, 'foo')

		(headers, body) = client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(self.is_isomorphic(body))


class StoreUrlTestCase(unittest.TestCase):
	def setUp(self):
		self.remote_url = 'http://example.org/data'
		self.client = MockHttp()
		self.client.register('get', self.remote_url, SINGLE_TRIPLE)
		self.store = pynappl.Store('http://example.com/store', client=self.client)
		self.graph = rdflib.graph.Graph()
		self.graph.parse(StringIO(SINGLE_TRIPLE), format="xml")
	
	def is_isomorphic(self, data):
		g = rdflib.graph.ConjunctiveGraph()
		g.parse(StringIO(data), format="xml")
		return self.graph.isomorphic(g)
	
	def test_store_url_without_graph_gets_supplied_url(self):
		resp = self.store.store_url(self.remote_url)
		self.assertTrue(self.client.received_request('get', self.remote_url))

	def test_store_url_without_graph_sets_accept_for_url_request(self):
		resp = self.store.store_url(self.remote_url)

		(headers, body) = self.client.get_request('get', self.remote_url)
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rdf+xml, application/xml;q=0.1, text/xml;q=0.1', headers['accept'])

	def test_store_url_without_graph_posts_to_metabox(self):
		resp = self.store.store_url(self.remote_url)
		self.assertTrue(self.client.received_request('post', 'http://example.com/store/meta'))

	def test_store_url_without_graph_sets_content_type(self):
		resp = self.store.store_url(self.remote_url)
		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_url_without_graph_sets_accept(self):
		resp = self.store.store_url(self.remote_url)
		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_url_without_graph_sets_body(self):
		resp = self.store.store_url(self.remote_url)

		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta')
		self.assertTrue(self.is_isomorphic(body))

	def test_store_url_with_graph_posts_to_graph(self):
		resp = self.store.store_url(self.remote_url, 'foo')
		self.assertTrue(self.client.received_request('post', 'http://example.com/store/meta/graphs/foo'))

	def test_store_url_with_graph_sets_content_type(self):
		resp = self.store.store_url(self.remote_url, 'foo')
		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_store_url_with_graph_sets_accept(self):
		resp = self.store.store_url(self.remote_url, 'foo')
		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])

	def test_store_url_with_graph_sets_body(self):
		resp = self.store.store_url(self.remote_url, 'foo')
		(headers, body) = self.client.get_request('post', 'http://example.com/store/meta/graphs/foo')
		self.assertTrue(self.is_isomorphic(body))


class AuthenticationTestCase(unittest.TestCase):
	def test_credentials_set_on_client(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client, username='scooby', password='mystery')
		self.assertEqual('scooby', client.username)
		self.assertEqual('mystery', client.password)

	def test_credentials_needs_username(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client, password='mystery')
		self.assertTrue(client.username is None)
		self.assertTrue(client.password is None)

	def test_credentials_needs_password(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client, username='scooby')
		self.assertTrue(client.username is None)
		self.assertTrue(client.password is None)


class UriTestCase(unittest.TestCase):
	def test_store_name_is_prefixed_with_api_uri(self):
		client = MockHttp()
		store = pynappl.Store("store", client=client)
		self.assertEqual("http://api.talis.com/stores/store", store.uri)
	
	def test_uri_is_stored(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertEqual('http://example.com/store', store.uri)

	def test_trailing_slash_on_uri_is_removed(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store/', client=client)
		self.assertEqual('http://example.com/store', store.uri)

class AccessStatusTestCase(unittest.TestCase):
	def test_is_writeable_is_true_for_read_write_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RW, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertTrue(store.is_writeable())

	def test_is_writeable_is_false_for_read_only_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RO, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertFalse(store.is_writeable())

	def test_is_writeable_is_false_for_unavailable_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_UN, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertFalse(store.is_writeable())

	def test_is_readable_is_true_for_read_write_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RW, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertTrue(store.is_readable())

	def test_is_readable_is_false_for_read_only_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RO, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertTrue(store.is_readable())

	def test_is_readable_is_false_for_unavailable_status(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_UN, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		self.assertFalse(store.is_readable())

	def test_status_reports_read_write(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RW, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(response, body) = store.status()
		self.assertEqual("store is read/write", body)

	def test_status_reports_read_only(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_RO, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(response, body) = store.status()
		self.assertEqual("store is read only (Being reindexed)", body)

	def test_status_reports_unavailable(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/access-status', STORE_ACCESS_STATUS_UN, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(response, body) = store.status()
		self.assertEqual("store is unavailable (Offline for maintenance)", body)

	def test_status_ignores_empty_status_message(self):
		client = MockHttp()
		data = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bf="http://schemas.talis.com/2006/bigfoot/configuration#"> 
	<rdf:Description rdf:about="http://example.com/store/config/access-status">
		<bf:statusMessage></bf:statusMessage>
		<bf:accessMode rdf:resource="http://schemas.talis.com/2006/bigfoot/statuses#read-write"/>
	</rdf:Description>
</rdf:RDF>"""
		client.register('get', 'http://example.com/store/config/access-status', data, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(response, body) = store.status()
		self.assertEqual("store is read/write", body)

class SparqlTestCase(unittest.TestCase):
	"""Test cases for sparql methods"""

	def test_select_performs_get_on_sparql_service(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.select('select * where {?s a ?o} limit 10', raw = True)
		self.assertTrue(client.received_request('get', 'http://example.com/store/services/sparql?query=' + urllib.quote_plus('select * where {?s a ?o} limit 10')))

	def test_select_returns_raw_result(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/services/sparql?query=' + urllib.quote_plus('select * where {?s a ?o} limit 10'), SELECT_DATA, httplib2.Response({'content-type':'application/sparql-results+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.select('select * where {?s a ?o} limit 10', raw = True)
		self.assertEqual(SELECT_DATA, body)

	def test_select_sets_accept(self):
		client = MockHttp()
		uri = 'http://example.com/store/services/sparql?query=' + urllib.quote_plus('select * where {?s a ?o} limit 10')
		client.register('get', uri, SELECT_DATA, httplib2.Response({'content-type':'application/sparql-results+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.select('select * where {?s a ?o} limit 10', raw = True)
		
		(headers, body) = client.get_request('get', uri)
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rdf+xml,application/sparql-results+xml', headers['accept'])
	
	def test_select_parse_result_correctly(self):
		client = MockHttp()
		uri = 'http://example.com/store/services/sparql?query=' + urllib.quote_plus('select * where {?s a ?o} limit 10')
		client.register('get', uri, SELECT_DATA, httplib2.Response({'content-type':'application/sparql-results+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		resp, result = store.select('select * where {?s a ?o} limit 10')
		
		headers, results = result
		
		self.assertEqual(["s", "o"], headers)
		self.assertEqual(2, len(results))
		
		self.assertEqual(["s", "o"], results[0].keys())
		self.assertEqual(rdflib.term.URIRef("http://oecd.dataincubator.org/"), results[0]["s"])
		self.assertEqual(rdflib.term.URIRef("http://rdfs.org/ns/void#Dataset"), results[0]["o"])
		
		self.assertEqual(["s", "o"], results[1].keys())
		self.assertEqual(rdflib.term.URIRef("http://oecd.dataincubator.org/glossary/segments/economic-outlook"), results[1]["s"])
		self.assertEqual(rdflib.term.URIRef("http://www.w3.org/2004/02/skos/core#Collection"), results[1]["o"])


class SearchTestCase(unittest.TestCase):
	"""Test cases for search methods"""

	def test_search_performs_get_on_contentbox(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/items?query=foo', SEARCH_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.search('foo', raw = True)
		self.assertTrue(client.received_request('get', 'http://example.com/store/items?query=foo'))

	def test_search_returns_raw_result(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/items?query=foo', SEARCH_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.search('foo', raw = True)
		self.assertEqual(SEARCH_DATA, body)

	def test_search_sets_accept(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/items?query=foo', SEARCH_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.search('foo', raw = True)
		
		(headers, body) = client.get_request('get', 'http://example.com/store/items?query=foo')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rss+xml', headers['accept'])

	
class SnapshotsTestCase(unittest.TestCase):
	"""Test cases for snapshot methods"""

	def test_snapshots_performs_get_on_snapshots_uri(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/snapshots', SNAPSHOT_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.snapshots(raw = True)
		self.assertTrue(client.received_request('get', 'http://example.com/store/snapshots'))

	def test_snaphots_returns_raw_result(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/snapshots', SNAPSHOT_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.snapshots(raw = True)
		self.assertEqual(SNAPSHOT_DATA, body)

	def test_snapshots_sets_accept(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/snapshots', SNAPSHOT_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.snapshots(raw = True)
		
		(headers, body) = client.get_request('get', 'http://example.com/store/snapshots')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rdf+xml', headers['accept'])

	def test_snaphots_returns_array_of_snapshot_uris(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/snapshots', SNAPSHOT_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, snapshot_list) = store.snapshots()
		self.assertEqual(1, len(snapshot_list))
		self.assertEqual("http://example.com/store/snapshots/20090821120029.tar", snapshot_list[0])

class FpmapTestCase(unittest.TestCase):
	"""Test cases for fpmap methods"""

	def read_fpmap(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/fpmaps/1', FPMAP_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.read_fpmap(raw = True)
		return (client, resp, body)

	def submit_fpmap(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		fpmap = pynappl.FieldPredicateMap('http://example.com/store/config/fpmaps/1')
		fpmap.from_rdfxml(FPMAP_DATA)
		resp = store.write_fpmap(fpmap)
		(header, body) = client.get_request('put', 'http://example.com/store/config/fpmaps/1')
		return (client, header, body)

	def test_read_fpmap_performs_get_on_fpmap_uri(self):
		(client, resp, body) = self.read_fpmap()
		self.assertTrue(client.received_request('get', 'http://example.com/store/config/fpmaps/1'))

	def test_read_fpmap_returns_raw_result(self):
		(client, resp, body) = self.read_fpmap()
		self.assertEqual(FPMAP_DATA, body)

	def test_read_fpmap_sets_accept(self):
		(client, resp, body) = self.read_fpmap()
		
		(headers, body) = client.get_request('get', 'http://example.com/store/config/fpmaps/1')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rdf+xml', headers['accept'])
		
	def test_write_fpmap_posts_to_fpmap_uri(self):
		(client, headers, body) = self.submit_fpmap()
		self.assertTrue(client.received_request('put', 'http://example.com/store/config/fpmaps/1'))

	def test_write_fpmap_sets_content_type(self):
		(client, headers, body) = self.submit_fpmap()
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_write_fpmap_sets_accept(self):
		(client, headers, body) = self.submit_fpmap()
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])


class QueryProfileTestCase(unittest.TestCase):
	"""Test cases for queryprofile methods"""

	def read_qprofile(self):
		client = MockHttp()
		client.register('get', 'http://example.com/store/config/queryprofiles/1', QPROFILE_DATA, httplib2.Response({'content-type':'application/rdf+xml'}))
		store = pynappl.Store('http://example.com/store', client=client)
		(resp, body) = store.read_query_profile(raw = True)
		return (client, resp, body)

	def submit_qprofile(self):
		client = MockHttp()
		store = pynappl.Store('http://example.com/store', client=client)
		qprofile = pynappl.QueryProfile('http://example.com/store/config/queryprofiles/1')
		qprofile.from_rdfxml(QPROFILE_DATA)
		resp = store.write_query_profile(qprofile)
		(header, body) = client.get_request('put', 'http://example.com/store/config/queryprofiles/1')
		return (client, header, body)

	def test_read_query_profile_performs_get_on_fpmap_uri(self):
		(client, resp, body) = self.read_qprofile()
		self.assertTrue(client.received_request('get', 'http://example.com/store/config/queryprofiles/1'))

	def test_read_query_profile_returns_raw_result(self):
		(client, resp, body) = self.read_qprofile()
		self.assertEqual(QPROFILE_DATA, body)

	def test_read_query_profile_sets_accept(self):
		(client, resp, body) = self.read_qprofile()
		(headers, body) = client.get_request('get', 'http://example.com/store/config/queryprofiles/1')
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('application/rdf+xml', headers['accept'])

	def test_write_query_profile_posts_to_fpmap_uri(self):
		(client, headers, body) = self.submit_qprofile()
		self.assertTrue(client.received_request('put', 'http://example.com/store/config/queryprofiles/1'))

	def test_write_query_profile_sets_content_type(self):
		(client, headers, body) = self.submit_qprofile()
		self.assertTrue(headers.has_key('content-type'))
		self.assertEqual('application/rdf+xml', headers['content-type'])

	def test_write_query_profile_sets_accept(self):
		(client, headers, body) = self.submit_qprofile()
		self.assertTrue(headers.has_key('accept'))
		self.assertEqual('*/*', headers['accept'])



if __name__ == "__main__":
	unittest.main()



# job_test.py - unit tests for pynappl job class
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

import unittest
import pynappl
import time

TEST_URI = "http://example.com/store/jobs/job1"
TEST_DATA = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:j.0="http://purl.org/dc/terms/" xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"> 
  <rdf:Description rdf:about="http://example.com/store/jobs/job1/progress2">
    <j.1:progressUpdateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:25:12Z</j.1:progressUpdateTime>
    <j.1:progressUpdateMessage>progress 2</j.1:progressUpdateMessage>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/jobs/job1/progress1">
    <j.1:progressUpdateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:12Z</j.1:progressUpdateTime>
    <j.1:progressUpdateMessage>progress 1</j.1:progressUpdateMessage>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/jobs/job1">
    <j.1:startTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2007-05-02T14:14:00Z</j.1:startTime>
    <rdfs:label>My Reset Data Job</rdfs:label>
    <j.1:progressUpdate rdf:resource="http://example.com/store/jobs/job1/progress1"/>
    <j.1:completionStatus rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#success"/>
    <j.0:created rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T00:18:53Z</j.0:created>
    <j.1:jobType rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob"/>
    <j.1:progressUpdate rdf:resource="http://example.com/store/jobs/job1/progress2"/>
    <rdf:type rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#JobRequest"/>
    <j.1:startMessage>ResetDataTask starting</j.1:startMessage>
    <j.1:endTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:14Z</j.1:endTime>
    <j.1:completionMessage>Reset store Complete.</j.1:completionMessage>
    <j.1:actualStartTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:11Z</j.1:actualStartTime>
  </rdf:Description>
</rdf:RDF>"""

TEST_DATA_NO_UPDATES = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:j.0="http://purl.org/dc/terms/" xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"> 
  <rdf:Description rdf:about="http://example.com/store/jobs/job1">
    <j.1:startTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2007-05-02T14:14:00Z</j.1:startTime>
    <rdfs:label>My Reset Data Job</rdfs:label>
    <j.1:completionStatus rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#success"/>
    <j.0:created rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T00:18:53Z</j.0:created>
    <j.1:jobType rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob"/>
    <rdf:type rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#JobRequest"/>
    <j.1:startMessage>ResetDataTask starting</j.1:startMessage>
    <j.1:endTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:14Z</j.1:endTime>
    <j.1:completionMessage>Reset store Complete.</j.1:completionMessage>
    <j.1:actualStartTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:11Z</j.1:actualStartTime>
  </rdf:Description>
</rdf:RDF>"""

class ParseTestCase(unittest.TestCase):
  def test_uri(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("http://example.com/store/jobs/job1", job.uri)
  
  def test_label(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("My Reset Data Job", job.label)
  
  def test_type(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob", job.type)
    self.assertEqual(pynappl.JOB_TYPE_RESET, job.type)
  
  def test_created(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual((2009, 8, 12, 0, 18, 53, 2, 224, -1), job.created)
  
  def test_start_time(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual((2007, 5, 2, 14, 14, 0, 2, 122, -1), job.start_time)
  
  def test_actual_start_time(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual((2009, 8, 12, 1, 19, 11, 2, 224, -1), job.actual_start_time)
  
  def test_snapshot_uri(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual(None, job.snapshot_uri)
  
  def test_start_message(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("ResetDataTask starting", job.start_message)
  
  def test_length_of_progress_updates(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual(2, len(job.progress_updates))
  
  def test_progress_updates_sorted_by_time(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    update1 = job.progress_updates[0]
    update2 = job.progress_updates[1]
    self.assertEqual("progress 1", update1.message)
    self.assertEqual("progress 2", update2.message)
  
  def test_progress_update_time(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    update = job.progress_updates[0]
    self.assertEqual((2009, 8, 12, 1, 19, 12, 2, 224, -1), update.time)
  
  def test_completion_status(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("http://schemas.talis.com/2006/bigfoot/configuration#success", job.completion_status)
    self.assertEqual(pynappl.JOB_STATUS_SUCCESS, job.completion_status)
  
  def test_completion_message(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual("Reset store Complete.", job.completion_message)
  
  def test_end_time(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    self.assertEqual((2009, 8, 12, 1, 19, 14, 2, 224, -1), job.end_time)

  def test_no_progress_updates(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA_NO_UPDATES)
    self.assertEqual(0, len(job.get_progress_updates()))



if __name__ == "__main__":
  unittest.main()

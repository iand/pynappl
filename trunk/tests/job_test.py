import unittest
import pynappl
import time

TEST_URI = "http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3"
TEST_DATA = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:j.0="http://purl.org/dc/terms/" xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"> 
  <rdf:Description rdf:about="http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3/767238a2-7309-424c-ab20-a40fb457c042">
    <j.1:progressUpdateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2009-08-12T01:19:12Z</j.1:progressUpdateTime>
    <j.1:progressUpdateMessage>Reset Data job running for store.</j.1:progressUpdateMessage>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3">
    <j.1:startTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2007-05-02T14:14:00Z</j.1:startTime>
    <rdfs:label>My Reset Data Job</rdfs:label>
    <j.1:progressUpdate rdf:resource="http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3/767238a2-7309-424c-ab20-a40fb457c042"/>
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
    self.assertEqual("http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3", job.uri)
  
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
    self.assertEqual(1, len(job.progress_updates))
  
  def test_progress_update_message(self):
    job = pynappl.Job.parse(TEST_URI, TEST_DATA)
    update = job.progress_updates[0]
    self.assertEqual("Reset Data job running for store.", update.message)
  
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
if __name__ == "__main__":
  unittest.main()

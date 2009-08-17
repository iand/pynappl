import time
import rdflib

class Job:
	SUCCESS = "http://schemas.talis.com/2006/bigfoot/configuration#success"
	ABORTED = "http://schemas.talis.com/2006/bigfoot/configuration#aborted"
	
	uri = None
	label = None
	type = None
	created = None
	start_time = None
	actual_start_time = None
	snapshot_uri = None
	start_message = None
	progress_updates = []
	completion_status = None
	completion_message = None
	end_time = None
	
	def __init__(self, uri, type, label="Job", start_time=time.localtime(), created=None):
		"""Constructor. Used in the reading/parsing code
		
		uri: a unique identifier for the job
		label: a description of the job
		type: the type of the job
		created: date-time the job was created in the system
		start_time: scheduled start time for the job"""
		
		self.uri = uri
		self.type = type
		self.label = label
		self.created = created
		self.start_time = start_time
		self.progress_updates = []
	
	def read_from_store(self, uri, store):
		"""Read a job from a store
		
		uri: uri of the job to read
		store: store from which the job will be read"""
		
		headers, data = store.get_job(uri)
		if headers["status"] != 200
			raise "Unable to read job from store. Response code was %s" % headers["status"]
		return self.parse(uri, resp.content)
	
	def parse(uri, xml)
		"""Parses job metadata returned from the platform as RDF/XML, creating a fully populated
		Job instance
		
		uri: uri of the job to be parsed
		xml: the RDF/XML text to be parsed"""
		
		g = rdflib.ConjunctiveGraph()
		g.parse(rdflib.StringInputSource(xml))
		
		s = rdflib.URIRef(uri)
		
		label = str(g.objects(s, rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#label")).next())
		type = str(g.objects(s, rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")).next())
		created = time.strptime(str(g.objects(s, rdflib.URIRef("http://purl.org/dc/terms/created")).next()), "%Y-%m-%dT%H:%M:%SZ")
		start_time = time.strptime(str(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#")).next()), "%Y-%m-%dT%H:%M:%SZ")
		job = Job(uri, label, type, start_time, created)
		
		if type == "http://schemas.talis.com/2006/bigfoot/configuration#RestoreJob":
			objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/snapshotUri")))
			if len(objects):
				job.snapshot_uri = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/actualStartTime")))
		if len(objects):
			job.actual_start_time = time.strptime(str(objects[0]), "%Y-%m-%dT%H:%M:%SZ")
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/startMessage")))
		if len(objects):
			job.start_message = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/completionMessage")))
		if len(objects):
			job.completion_message = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/endTime")))
		if len(objects):
			job.end_time = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/completionStatus")))
		if len(objects):
			job.completion_status = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/progressUpdate")))
		for object in objects:
			update = JobUpdate()
			
			subobjects = list(g.objects(object, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/progressUpdateMessage")))
			if len(subobjects):
				update.message = str(subobjects[0])
			
			subobjects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/progressUpdateTime")))
			if len(subobjects):
				update.time = time.strptime(str(subobjects[0]), "%Y-%m-%dT%H:%M:%SZ")
			
			self.progress_updates.append(update)
		
		return job
	
	def get_progress_updates(self):
		self.progress_updates.sort()
		return self.progress_updates
	
	def has_started(self):
		"""Has the job started?"""
		return self.actual_start_time != None
	
	def has_completed(self):
		"""Has the job completed?"""
		return self.completion_status != None
	
	def was_successful(self):
		"""Was the job successful?"""
		return self.has_completed() and self.completion_status == self.SUCCESS
	
	def is_running(self):
		"""Is the job still running?"""
		return self.has_started() and not self.has_completed()

class JobUpdate:
	#Just a placeholder
	
	message = None
	time = None

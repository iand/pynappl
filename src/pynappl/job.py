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
	progress_updates = None
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
	
	def parse(self, uri, xml)
		"""Parses job metadata returned from the platform as RDF/XML, creating a fully populated
		Job instance
		
		uri: uri of the job to be parsed
		xml: the RDF/XML text to be parsed"""
		
		g = rdflib.ConjunctiveGraph()
		g.parse(rdflib.StringInputSource(xml))
	job_el = REXML::XPath.first(root, "//*[@rdf:about='%s']" % uri, Pho::Namespaces::MAPPING )
	uri = job_el.attributes["rdf:about"]
	label = REXML::XPath.first(job_el, "rdfs:label", Pho::Namespaces::MAPPING ).text
	type_el = REXML::XPath.first(job_el, "rdf:type", Pho::Namespaces::MAPPING )
	type = type_el.attributes["rdf:resource"]
	created = REXML::XPath.first(job_el, "dcterms:created", Pho::Namespaces::MAPPING ).text
	start_time = REXML::XPath.first(job_el, "bf:startTime", Pho::Namespaces::MAPPING ).text
	
	job = Job.new(uri, label, type, start_time, created)
	if type == Pho::Jobs::RESTORE
	with_first(job_el, "bf:snapshotUri") do |uri|
	job.snapshot_uri = uri.attributes["rdf:resource"]
	end
	end
	
		with_first(job_el, "bf:actualStartTime") do |el|
			job.actual_start_time = el.text
		with_first(job_el, "bf:startMessage") do |el|
			job.start_message = el.text
		with_first(job_el, "bf:completionMessage") do |el|
			job.completion_message = el.text
		with_first(job_el, "bf:endTime") do |el|
			job.end_time = el.text
		with_first(job_el, "bf:completionStatus") do |el|
			job.completion_status = el.attributes["rdf:resource"]
		with_each(job_el, "bf:progressUpdate") do |el|
			update = JobUpdate.new
		with_first(el, "bf:progressUpdateMessage") do |msg|
			update.message = msg.text
		with_first(el, "bf:progressUpdateTime") do |time|
			update.time = time.text
		job.progress_updates << update
	
		return job 
	
	
	def progress_updates()
		@progress_updates.sort! { |x,y|
			x.time <=> y.time 
		}
	return @progress_updates
	
	#Has the job started?
	def started?
		return @actual_start_time != nil
	
	#Has the job completed?
	def completed?
		return @completion_status != nil

	#Was the job successful?
	def successful?
		return self.completed? && @completion_status == Pho::Job::SUCCESS

	#Is the job still running?
	def running?
		return started? && !completed? 

	def Job.with_first(el, xpath)
		found_el = REXML::XPath.first(el, xpath, Pho::Namespaces::MAPPING)
		if found_el != nil
			yield found_el

	def Job.with_each(el, xpath)
		REXML::XPath.each(el, xpath, Pho::Namespaces::MAPPING) do |e|
		root = e.document.root
		uri = e.attributes["rdf:resource"]
		ref_el = REXML::XPath.first(root, "//*[@rdf:about='#{uri}']", Pho::Namespaces::MAPPING)
		yield ref_el

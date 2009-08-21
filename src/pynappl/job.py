# job.py - facade for managing offline jobs on the Talis Platform
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

__all__ = ["Job", "JobUpdate", "JOB_STATUS_SUCCESS", "JOB_STATUS_ABORTED",
	"JOB_TYPE_RESET", "JOB_TYPE_SNAPSHOT", "JOB_TYPE_REINDEX", "JOB_TYPE_RESTORE"]

import time
import rdflib

JOB_STATUS_SUCCESS = "http://schemas.talis.com/2006/bigfoot/configuration#success"
JOB_STATUS_ABORTED = "http://schemas.talis.com/2006/bigfoot/configuration#aborted"

JOB_TYPE_RESET = "http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob"
JOB_TYPE_SNAPSHOT = "http://schemas.talis.com/2006/bigfoot/configuration#SnapshotJob"
JOB_TYPE_REINDEX = "http://schemas.talis.com/2006/bigfoot/configuration#ReindexJob"
JOB_TYPE_RESTORE = "http://schemas.talis.com/2006/bigfoot/configuration#RestoreJob"

class Job:
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
		if headers["status"] != 200:
			raise "Unable to read job from store. Response code was %s" % headers["status"]
		return self.parse(uri, resp.content)
	
	@staticmethod
	def parse(uri, xml):
		"""Parses job metadata returned from the platform as RDF/XML, creating a fully populated
		Job instance
		
		uri: uri of the job to be parsed
		xml: the RDF/XML text to be parsed"""
		
		g = rdflib.ConjunctiveGraph()
		g.parse(rdflib.StringInputSource(xml))
		
		s = rdflib.URIRef(uri)
		
		label = str(g.objects(s, rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#label")).next())
		type = str(g.objects(s, rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")).next())
		
		if type == "http://schemas.talis.com/2006/bigfoot/configuration#JobRequest":
			type = str(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#jobType")).next())
		
		created = time.strptime(str(g.objects(s, rdflib.URIRef("http://purl.org/dc/terms/created")).next()), "%Y-%m-%dT%H:%M:%SZ")
		start_time = time.strptime(str(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#startTime")).next()), "%Y-%m-%dT%H:%M:%SZ")
		job = Job(uri, type, label, start_time, created)
		
		if type == "http://schemas.talis.com/2006/bigfoot/configuration#RestoreJob":
			objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/snapshotUri")))
			if len(objects):
				job.snapshot_uri = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#actualStartTime")))
		if len(objects):
			job.actual_start_time = time.strptime(str(objects[0]), "%Y-%m-%dT%H:%M:%SZ")
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#startMessage")))
		if len(objects):
			job.start_message = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#completionMessage")))
		if len(objects):
			job.completion_message = str(objects[0])
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#endTime")))
		if len(objects):
			job.end_time = time.strptime(str(objects[0]), "%Y-%m-%dT%H:%M:%SZ")
		
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#completionStatus")))
		if len(objects):
			job.completion_status = str(objects[0])
		
		updates = {}
		objects = list(g.objects(s, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#progressUpdate")))
		for object in objects:
			update = JobUpdate()
			
			subobjects = list(g.objects(object, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#progressUpdateMessage")))
			if len(subobjects):
				update.message = str(subobjects[0])
			
			subobjects = list(g.objects(object, rdflib.URIRef("http://schemas.talis.com/2006/bigfoot/configuration#progressUpdateTime")))
			if len(subobjects):
				update.time = time.strptime(str(subobjects[0]), "%Y-%m-%dT%H:%M:%SZ")
			
			if not updates.has_key(str(subobjects[0])):
				updates[str(subobjects[0])] = []
			updates[str(subobjects[0])].append(update)
				

		keys = updates.keys()
		keys.sort()
		for update_group in [updates[key] for key in keys]:
			job.progress_updates.extend(update_group)
		
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
		return self.has_completed() and self.completion_status == JOB_STATUS_SUCCESS
	
	def is_running(self):
		"""Is the job still running?"""
		return self.has_started() and not self.has_completed()

class JobUpdate:
	#Just a placeholder
	
	message = None
	time = None

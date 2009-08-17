"""changeset.py
Support for using applying changesets to a store

Note:
	For the add() and remove() functions, URIs are represented by
	strings, and literals are represented by (text, lang, datatype)
	tuples. Either or both lang and datatype can be None. Where both
	are specified, lang takes precedence."""
__all__ = ["Changeset"]
import httplib2
import time
from errors import *
class Changeset(object):
	h = httplib2.Http()
	def __init__(self, store_uri=None, adds=[], removes=[], subject_of_change=None, created_date=time.strftime("%Y-%m-%dT%H:%M:%SZ"), creator_name="Anon", change_reason="Changed triples"):
		self.store_uri = (store_uri is not None and store_uri.endswith("/")) and store_uri[:-1] or store_uri
		self.adds = adds
		self.removes = removes
		self.subject_of_change = subject_of_change
		self.created_date = created_date
		self.creator_name = creator_name
		self.change_reason = change_reason
	def set_store_uri(self, store_uri):
		self.store_uri = store_uri.endswith("/") and store_uri[:-1] or store_uri
	def add(self, s, p, o):
		self.adds.append((s, p, o))
	def remove(self, s, p, o):
		self.removes.append((s, p, o))
	def set_subject_of_change(self, subject_of_change):
		self.subject_of_change = subject_of_change
	def set_created_date(self, created_date):
		self.created_date = created_date
	def set_creator_name(self, creator_name):
		self.creator_name = creator_name
	def set_change_reason(self, change_reason):
		self.change_reason = change_reason
	def login(self, un, pw):
		self.h.add_credentials(un, pw)
	def execute(self):
		if self.store_uri is None:
			raise InvalidCommandParameters("Store URI is not set")
		if self.subject_of_change is None:
			raise InvalidCommandParameters("Subject of change is not set")
		uri = self.store_uri + "/meta"
		s = "<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:cs=\"http://purl.org/vocab/changeset/schema#\">\n\t<cs:ChangeSet>\n\t\t<cs:subjectOfChange rdf:resource=\"%s\"/>\n\t\t<cs:createdDate>%s</cs:createdDate>\n\t\t<cs:creatorName>%s</cs:creatorName>\n\t\t<cs:changeReason>%s</cs:changeReason>\n" % (
			self.subject_of_change,
			self.created_date,
			self.creator_name,
			self.change_reason,
		)
		for s, p, o in self.adds:
			s += "\t\t<cs:addition>\n\t\t\t<rdf:Statement>\n\t\t\t\t<rdf:subject rdf:resource=\"%s\"/>\n\t\t\t\t<rdf:predicate rdf:resource=\"%s\"/>\n\t\t\t\t<rdf:object" % (s, p)
			if isinstance(o, tuple):
				if o[1] is not None:
					s += " xml:lang=\"%s\">%s</rdf:object>" % (o[1], o[0])
				elif o[2] is not None:
					s += " rdf:datatype=\"%s\">%s</rdf:object>" % (o[2], o[0])
				else:
					s += ">%s</rdf:object>" % o[0]
			else:
				s += " rdf:resource=\"%s\"/>" % o
			s += "\n\t\t\t</rdf:Statement>\n\t\t</cs:addition>\n"
		for s, p, o in self.removes:
			s += "\t\t<cs:removal>\n\t\t\t<rdf:Statement>\n\t\t\t\t<rdf:subject rdf:resource=\"%s\"/>\n\t\t\t\t<rdf:predicate rdf:resource=\"%s\"/>\n\t\t\t\t<rdf:object" % (s, p)
			if isinstance(o, tuple):
				if o[1] is not None:
					s += " xml:lang=\"%s\">%s</rdf:object>" % (o[1], o[0])
				elif o[2] is not None:
					s += " rdf:datatype=\"%s\">%s</rdf:object>" % (o[2], o[0])
				else:
					s += ">%s</rdf:object>" % o[0]
			else:
				s += " rdf:resource=\"%s\"/>" % o
			s += "\n\t\t\t</rdf:Statement>\n\t\t</cs:removal>\n"
		s += "\t</cs:ChangeSet>\n</rdf:RDF>\n"
		headers, data = self.h.request(uri, "POST", body=s, headers={"content-type" : "application/vnd.talis.changeset+xml"})
		if int(headers["status"]) in range(200, 300):
			pass
		else:
			raise CouldNotSendRequest("POST '%s': got status %s" % (uri, headers["status"]))

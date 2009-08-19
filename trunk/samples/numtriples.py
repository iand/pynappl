""" Uses FileManager tp list RDF files and the number of triples in each
Uses the same interface as FileManager"""

import pynappl
import rdflib

def callback(filename):
	if not filename.endswith(".rdf"):
		return "File is not an RDF file"
	g = rdflib.ConjunctiveGraph()
	g.parse(rdflib.FileInputSource(open(filename, "r")))
	triples = g.triples((None, None, None))
	ntriples = len(list(triples))
	print "%s has %d triples" % (filename, ntriples)

def main():
	pynappl.file_manager_main(callback=callback)

if __name__ == "__main__":
	main()

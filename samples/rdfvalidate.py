""" Uses FileManager to valdate RDF files
Uses the same interface as FileManager"""

import pynappl
import rdflib
import traceback
import sys

def callback(filename):
	g = rdflib.ConjunctiveGraph()
	try:
		g.parse(rdflib.FileInputSource(open(filename, "r")))
	except:
		lines = traceback.format_exception(*sys.exc_info())
		return "\n".join(lines)

def main():
	pynappl.file_manager_main(callback=callback, filter=r"\.rdf$")

if __name__ == "__main__":
	main()

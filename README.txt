pynappl is a simple client library for the Talis Platform. It draws inspiration from other similar client libraries

* Moriarty - http://code.google.com/p/moriarty/
* Pho - http://rubyforge.org/projects/pho/

== DEPENDENCIES ==

At least the following (there may be more, this is alpha software under constant revision):

* rdflib 3.0 - http://code.google.com/p/rdflib/
* httplib2 - http://code.google.com/p/httplib2/

== GETTING STARTED ==

Install rdflib 3.0 using easy_install:

sudo easy_install -U "rdflib>=3.0.0"

Edit ~/.bashrc and add

export PYTHONPATH=$PYTHONPATH:/<path to pynappl>/src

You can then apply these changes to your current shell session by executing 

source ~/.bashrc

Run the unit tests from the /tests directory:

python all_tests.py

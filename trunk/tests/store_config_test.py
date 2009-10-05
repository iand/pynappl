# store_config_test.py - unit tests for pynappl storeconfig class
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
import rdflib.namespace, rdflib.term

FRAME = rdflib.namespace.Namespace("http://schemas.talis.com/2006/frame/schema#")
BF = rdflib.namespace.Namespace("http://schemas.talis.com/2006/bigfoot/configuration#")

FPMAP_DATA= """<rdf:RDF
    xmlns:frm="http://schemas.talis.com/2006/frame/schema#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:j.0="http://schemas.talis.com/2006/bigfoot/configuration#" >
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#aimchatid">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/aimChatID"/>
    <frm:name>aimchatid2</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#surname">
    <frm:name>surname</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/surname"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#name">
    <frm:name>name</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/name"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#family_name">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/family_name"/>
    <frm:name>family_name</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#jabberid">
    <frm:name>jabberid</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/jabberID"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#yahoochatid">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/yahooChatID"/>
    <frm:name>yahoochatid</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#plan">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/plan"/>
    <frm:name>plan</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#firstname">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/firstName"/>
    <frm:name>firstname</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#nick">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/nick"/>
    <frm:name>nick</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#msnchatid">
    <frm:name>msnchatid</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/msnChatID"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#gender">
    <frm:name>gender</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/gender"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#givenname">
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/givenname"/>
    <frm:name>givenname</frm:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#olb">
    <frm:name>olb</frm:name>
    <frm:property rdf:resource="http://purl.org/vocab/bio/0.1/olb"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1#mboxsha1sum">
    <frm:name>mboxsha1sum</frm:name>
    <frm:property rdf:resource="http://xmlns.com/foaf/0.1/mbox_sha1sum"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/fpmaps/1">
    <rdf:type rdf:resource="http://schemas.talis.com/2006/bigfoot/configuration#FieldPredicateMap"/>
    <rdfs:label>default field/predicate map</rdfs:label>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#yahoochatid"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#mboxsha1sum"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#givenname"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#aimchatid"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#olb"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#gender"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#msnchatid"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#family_name"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#surname"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#nick"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#name"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#plan"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#firstname"/>
    <frm:mappedDatatypeProperty rdf:resource="http://example.com/store/fpmaps/1#jabberid"/>
  </rdf:Description>
</rdf:RDF>"""

QP_DATA="""<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:j.0="http://schemas.talis.com/2006/frame/schema#"
    xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" > 
  <rdf:Description rdf:about="http://example.com/store/config/queryprofiles/1#subject">
    <j.1:weight>5</j.1:weight>
    <j.0:name>subject</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/config/queryprofiles/1#subtitle">
    <j.1:weight>3</j.1:weight>
    <j.0:name>subtitle</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/config/queryprofiles/1#label">
    <j.1:weight>1</j.1:weight>
    <j.0:name>label</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/config/queryprofiles/1">
    <j.1:fieldWeight rdf:resource="http://example.com/store/config/queryprofiles/1#subtitle"/>
    <j.1:fieldWeight rdf:resource="http://example.com/store/config/queryprofiles/1#subject"/>
    <j.1:fieldWeight rdf:resource="http://example.com/store/config/queryprofiles/1#label"/>
  </rdf:Description>
</rdf:RDF>"""


class StoreConfigTestCase(unittest.TestCase):
	def test_get_first_fpmap_uri_default(self):
		config = pynappl.StoreConfig("http://example.com/store/config")
		self.assertEqual("http://example.com/store/config/fpmaps/1", config.get_first_fpmap_uri())

	def test_get_first_query_profile_uri_default(self):
		config = pynappl.StoreConfig("http://example.com/store/config")
		self.assertEqual("http://example.com/store/config/queryprofiles/1", config.get_first_query_profile_uri())
  
	def test_get_first_fpmap_uri_handles_legacy_uris(self):
		fpmap_uris = {
									'ajmg-dev1' : 'http://api.talis.com/stores/ajmg-dev1/indexes/default/fpmaps/default',
									'beobal-dev1' : 'http://api.talis.com/stores/beobal-dev1/indexes/default/fpmaps/default',
									'bib-sandbox' : 'http://api.talis.com/stores/bib-sandbox/indexes/m21Advanced/fpmaps/fpmap',
									'bib-talisuniplymouth-1' : 'http://api.talis.com/stores/bib-talisuniplymouth-1/config/fpmaps/1',
									'cenotelist' : 'http://api.talis.com/stores/cenotelist/indexes/default/fpmaps/fpmap',
									'cnimages' : 'http://api.talis.com/stores/cnimages/indexes/cnimages/fpmaps/fpmap',
									'danja-dev1' : 'http://api.talis.com/stores/danja-dev1/indexes/default/fpmaps/default',
									'dataMonitoring' : 'http://api.talis.com/stores/dataMonitoring/indexes/default/fpmaps/default',
									'engage-dev1' : 'http://api.talis.com/stores/engage-dev1/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant10' : 'http://api.talis.com/stores/engagetenant10/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant11' : 'http://api.talis.com/stores/engagetenant11/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant12' : 'http://api.talis.com/stores/engagetenant12/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant13' : 'http://api.talis.com/stores/engagetenant13/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant14' : 'http://api.talis.com/stores/engagetenant14/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant15' : 'http://api.talis.com/stores/engagetenant15/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant16' : 'http://api.talis.com/stores/engagetenant16/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant17' : 'http://api.talis.com/stores/engagetenant17/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant18' : 'http://api.talis.com/stores/engagetenant18/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant19' : 'http://api.talis.com/stores/engagetenant19/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant1' : 'http://api.talis.com/stores/engagetenant1/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant20' : 'http://api.talis.com/stores/engagetenant20/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant21' : 'http://api.talis.com/stores/engagetenant21/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant22' : 'http://api.talis.com/stores/engagetenant22/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant23' : 'http://api.talis.com/stores/engagetenant23/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant24' : 'http://api.talis.com/stores/engagetenant24/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant25' : 'http://api.talis.com/stores/engagetenant25/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant26' : 'http://api.talis.com/stores/engagetenant26/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant27' : 'http://api.talis.com/stores/engagetenant27/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant28' : 'http://api.talis.com/stores/engagetenant28/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant29' : 'http://api.talis.com/stores/engagetenant29/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant2' : 'http://api.talis.com/stores/engagetenant2/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant30' : 'http://api.talis.com/stores/engagetenant30/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant3' : 'http://api.talis.com/stores/engagetenant3/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant4' : 'http://api.talis.com/stores/engagetenant4/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant5' : 'http://api.talis.com/stores/engagetenant5/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant6' : 'http://api.talis.com/stores/engagetenant6/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant7' : 'http://api.talis.com/stores/engagetenant7/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant8' : 'http://api.talis.com/stores/engagetenant8/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenant9' : 'http://api.talis.com/stores/engagetenant9/indexes/metaboxIndex/fpmaps/fpmap',
									'engagetenantstore' : 'http://api.talis.com/stores/engagetenantstore/indexes/metaboxIndex/fpmaps/fpmap',
									'gatech' : 'http://api.talis.com/stores/gatech/indexes/m21Advanced/fpmap',
									'holdings' : 'http://api.talis.com/stores/holdings/indexes/m21Holdings/fpmaps/fpmap',
									'iand-dev1' : 'http://api.talis.com/stores/iand-dev1/indexes/default/fpmaps/default',
									'iand-dev2' : 'http://api.talis.com/stores/iand-dev2/indexes/default/fpmaps/default',
									'iand-dev3' : 'http://api.talis.com/stores/iand-dev3/indexes/default/fpmaps/default',
									'image-sandbox' : 'http://api.talis.com/stores/image-sandbox/indexes/image-sandbox/fpmaps/fpmap',
									'inst-5050' : 'http://api.talis.com/stores/inst-5050/indexes/m21Advanced/fpmaps/fpmap',
									'inst-u138' : 'http://api.talis.com/stores/inst-u138/indexes/m21Advanced/fpmaps/fpmap',
									'jingye-dev1' : 'http://api.talis.com/stores/jingye-dev1/indexes/default/fpmaps/default',
									'kwijibo-dev1' : 'http://api.talis.com/stores/kwijibo-dev1/indexes/default/fpmaps/default',
									'list-demo1' : 'http://api.talis.com/stores/list-demo1/indexes/metaboxIndex/fpmaps/fpmap',
									'list-dev1' : 'http://api.talis.com/stores/list-dev1/indexes/metaboxIndex/fpmaps/fpmap',
									'list-dev2' : 'http://api.talis.com/stores/list-dev2/indexes/metaboxIndex/fpmaps/fpmap',
									'list-dev3' : 'http://api.talis.com/stores/list-dev3/indexes/metaboxIndex/fpmaps/fpmap',
									'list-qa1' : 'http://api.talis.com/stores/list-qa1/indexes/metaboxIndex/fpmaps/fpmap',
									'list-qa2' : 'http://api.talis.com/stores/list-qa2/indexes/metaboxIndex/fpmaps/fpmap',
									'list-qa3' : 'http://api.talis.com/stores/list-qa3/indexes/metaboxIndex/fpmaps/fpmap',
									'list-tenants-dev' : 'http://api.talis.com/stores/list-tenants-dev/indexes/metaboxIndex/fpmaps/fpmap',
									'malcyl-dev1' : 'http://api.talis.com/stores/malcyl-dev1/indexes/default/fpmaps/default',
									'nuggetengage-demo1' : 'http://api.talis.com/stores/nuggetengage-demo1/indexes/metaboxIndex/fpmaps/fpmap',
									'nuggetengage-demo2' : 'http://api.talis.com/stores/nuggetengage-demo2/indexes/metaboxIndex/fpmaps/fpmap',
									'nuggetengage-demo3' : 'http://api.talis.com/stores/nuggetengage-demo3/indexes/metaboxIndex/fpmaps/fpmap',
									'nuggetengage-demo4' : 'http://api.talis.com/stores/nuggetengage-demo4/indexes/metaboxIndex/fpmaps/fpmap',
									'nuggetengage-qa1' : 'http://api.talis.com/stores/nuggetengage-qa1/indexes/metaboxIndex/fpmaps/fpmap',
									'quoll-dev1' : 'http://api.talis.com/stores/quoll-dev1/indexes/default/fpmaps/default',
									'schema-cache' : 'http://api.talis.com/stores/schema-cache/indexes/default/fpmaps/default',
									'silkworm-dev' : 'http://api.talis.com/stores/silkworm-dev/indexes/default/fpmaps/default',
									'silkworm' : 'http://api.talis.com/stores/silkworm/indexes/default/fpmaps/default',
									'source-dev1' : 'http://api.talis.com/stores/source-dev1/indexes/default/fpmaps/default',
									'source-qa1' : 'http://api.talis.com/stores/source-qa1/indexes/default/fpmaps/default',
									'tomh-dev1' : 'http://api.talis.com/stores/tomh-dev1/indexes/default/fpmaps/default',
									'ukbib' : 'http://api.talis.com/stores/ukbib/indexes/m21Advanced/fpmaps/fpmap',
									'union' : 'http://api.talis.com/stores/union/indexes/union/fpmaps/fpmap',
									'wikipedia' : 'http://api.talis.com/stores/wikipedia/indexes/abstracts/fpmaps/fpmap',
									'zephyr-cust10' : 'http://api.talis.com/stores/zephyr-cust10/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust11' : 'http://api.talis.com/stores/zephyr-cust11/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust12' : 'http://api.talis.com/stores/zephyr-cust12/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust13' : 'http://api.talis.com/stores/zephyr-cust13/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust14' : 'http://api.talis.com/stores/zephyr-cust14/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust15' : 'http://api.talis.com/stores/zephyr-cust15/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust16' : 'http://api.talis.com/stores/zephyr-cust16/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust17' : 'http://api.talis.com/stores/zephyr-cust17/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust18' : 'http://api.talis.com/stores/zephyr-cust18/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust19' : 'http://api.talis.com/stores/zephyr-cust19/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust1' : 'http://api.talis.com/stores/zephyr-cust1/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust2' : 'http://api.talis.com/stores/zephyr-cust2/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust3' : 'http://api.talis.com/stores/zephyr-cust3/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust4' : 'http://api.talis.com/stores/zephyr-cust4/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust5' : 'http://api.talis.com/stores/zephyr-cust5/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust6' : 'http://api.talis.com/stores/zephyr-cust6/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust7' : 'http://api.talis.com/stores/zephyr-cust7/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust8' : 'http://api.talis.com/stores/zephyr-cust8/indexes/metaboxIndex/fpmaps/fpmap',
									'zephyr-cust9' : 'http://api.talis.com/stores/zephyr-cust9/indexes/metaboxIndex/fpmaps/fpmap',
			}

		for store_name, fpmap_uri in fpmap_uris.items():
			config = pynappl.StoreConfig("http://api.talis.com/stores/%s/config" % store_name)
			self.assertEqual(fpmap_uri, config.get_first_fpmap_uri())


	def test_get_first_query_profile_uri_handles_legacy_uris(self):
		qp_uris = {
						'ajmg-dev1' : 'http://api.talis.com/stores/ajmg-dev1/indexes/default/queryprofiles/default',
						'beobal-dev1' : 'http://api.talis.com/stores/beobal-dev1/indexes/default/queryprofiles/default',
						'bib-sandbox' : 'http://api.talis.com/stores/bib-sandbox/indexes/m21Advanced/queryprofiles/default',
						'bib-talisuniplymouth-1' : 'http://api.talis.com/stores/bib-talisuniplymouth-1/config/queryprofiles/1',
						'cenotelist' : 'http://api.talis.com/stores/cenotelist/indexes/default/queryprofiles/default',
						'cnimages' : 'http://api.talis.com/stores/cnimages/indexes/cnimages/queryprofiles/default',
						'danja-dev1' : 'http://api.talis.com/stores/danja-dev1/indexes/default/queryprofiles/default',
						'dataMonitoring' : 'http://api.talis.com/stores/dataMonitoring/indexes/default/queryprofiles/default',
						'engage-dev1' : 'http://api.talis.com/stores/engage-dev1/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant10' : 'http://api.talis.com/stores/engagetenant10/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant11' : 'http://api.talis.com/stores/engagetenant11/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant11' : 'http://api.talis.com/stores/engagetenant11/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant13' : 'http://api.talis.com/stores/engagetenant13/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant14' : 'http://api.talis.com/stores/engagetenant14/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant15' : 'http://api.talis.com/stores/engagetenant15/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant16' : 'http://api.talis.com/stores/engagetenant16/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant17' : 'http://api.talis.com/stores/engagetenant17/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant18' : 'http://api.talis.com/stores/engagetenant18/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant19' : 'http://api.talis.com/stores/engagetenant19/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant1' : 'http://api.talis.com/stores/engagetenant1/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant20' : 'http://api.talis.com/stores/engagetenant20/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant21' : 'http://api.talis.com/stores/engagetenant21/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant22' : 'http://api.talis.com/stores/engagetenant22/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant23' : 'http://api.talis.com/stores/engagetenant23/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant24' : 'http://api.talis.com/stores/engagetenant24/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant25' : 'http://api.talis.com/stores/engagetenant25/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant26' : 'http://api.talis.com/stores/engagetenant26/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant27' : 'http://api.talis.com/stores/engagetenant27/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant28' : 'http://api.talis.com/stores/engagetenant28/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant29' : 'http://api.talis.com/stores/engagetenant29/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant2' : 'http://api.talis.com/stores/engagetenant2/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant30' : 'http://api.talis.com/stores/engagetenant30/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant3' : 'http://api.talis.com/stores/engagetenant3/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant4' : 'http://api.talis.com/stores/engagetenant4/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant5' : 'http://api.talis.com/stores/engagetenant5/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant6' : 'http://api.talis.com/stores/engagetenant6/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant7' : 'http://api.talis.com/stores/engagetenant7/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant8' : 'http://api.talis.com/stores/engagetenant8/indexes/metaboxIndex/queryprofiles/default',
						'engagetenant9' : 'http://api.talis.com/stores/engagetenant9/indexes/metaboxIndex/queryprofiles/default',
						'engagetenantstore' : 'http://api.talis.com/stores/engagetenantstore/indexes/metaboxIndex/queryprofiles/default',
						'gatech' : 'http://api.talis.com/stores/gatech/indexes/m21Advanced/queryprofiles/default',
						'holdings' : 'http://api.talis.com/stores/holdings/indexes/m21Holdings/queryprofiles/default',
						'iand-dev1' : 'http://api.talis.com/stores/iand-dev1/indexes/default/queryprofiles/default',
						'iand-dev2' : 'http://api.talis.com/stores/iand-dev2/indexes/default/queryprofiles/default',
						'iand-dev3' : 'http://api.talis.com/stores/iand-dev3/indexes/default/queryprofiles/default',
						'image-sandbox' : 'http://api.talis.com/stores/image-sandbox/indexes/image-sandbox/queryprofiles/default',
						'inst-5050' : 'http://api.talis.com/stores/inst-5050/indexes/m21Advanced/queryprofiles/default',
						'inst-u138' : 'http://api.talis.com/stores/inst-u138/indexes/m21Advanced/queryprofiles/default',
						'jingye-dev1' : 'http://api.talis.com/stores/jingye-dev1/indexes/default/queryprofiles/default',
						'kwijibo-dev1' : 'http://api.talis.com/stores/kwijibo-dev1/indexes/default/queryprofiles/default',
						'list-demo1' : 'http://api.talis.com/stores/list-demo1/indexes/metaboxIndex/queryprofiles/default',
						'list-dev1' : 'http://api.talis.com/stores/list-dev1/indexes/metaboxIndex/queryprofiles/default',
						'list-dev2' : 'http://api.talis.com/stores/list-dev2/indexes/metaboxIndex/queryprofiles/default',
						'list-dev3' : 'http://api.talis.com/stores/list-dev3/indexes/metaboxIndex/queryprofiles/default',
						'list-qa1' : 'http://api.talis.com/stores/list-qa1/indexes/metaboxIndex/queryprofiles/default',
						'list-qa2' : 'http://api.talis.com/stores/list-qa2/indexes/metaboxIndex/queryprofiles/default',
						'list-qa3' : 'http://api.talis.com/stores/list-qa3/indexes/metaboxIndex/queryprofiles/default',
						'list-tenants-dev' : 'http://api.talis.com/stores/list-tenants-dev/indexes/metaboxIndex/queryprofiles/default',
						'malcyl-dev1' : 'http://api.talis.com/stores/malcyl-dev1/indexes/default/queryprofiles/default',
						'nuggetengage-demo1' : 'http://api.talis.com/stores/nuggetengage-demo1/indexes/metaboxIndex/queryprofiles/default',
						'nuggetengage-demo2' : 'http://api.talis.com/stores/nuggetengage-demo2/indexes/metaboxIndex/queryprofiles/default',
						'nuggetengage-demo3' : 'http://api.talis.com/stores/nuggetengage-demo3/indexes/metaboxIndex/queryprofiles/default',
						'nuggetengage-demo4' : 'http://api.talis.com/stores/nuggetengage-demo4/indexes/metaboxIndex/queryprofiles/default',
						'nuggetengage-qa1' : 'http://api.talis.com/stores/nuggetengage-qa1/indexes/metaboxIndex/queryprofiles/default',
						'quoll-dev1' : 'http://api.talis.com/stores/quoll-dev1/indexes/default/queryprofiles/default',
						'schema-cache' : 'http://api.talis.com/stores/schema-cache/indexes/default/queryprofiles/default',
						'silkworm-dev' : 'http://api.talis.com/stores/silkworm-dev/indexes/default/queryprofiles/default',
						'silkworm' : 'http://api.talis.com/stores/silkworm/indexes/default/queryprofiles/default',
						'source-dev1' : 'http://api.talis.com/stores/source-dev1/indexes/default/queryprofiles/default',
						'source-qa1' : 'http://api.talis.com/stores/source-qa1/indexes/default/queryprofiles/default',
						'tomh-dev1' : 'http://api.talis.com/stores/tomh-dev1/indexes/default/queryprofiles/default',
						'ukbib' : 'http://api.talis.com/stores/ukbib/indexes/m21Advanced/queryprofiles/default',
						'union' : 'http://api.talis.com/stores/union/indexes/union/queryprofiles/default',
						'wikipedia' : 'http://api.talis.com/stores/wikipedia/indexes/abstracts/queryprofiles/default',
						'zephyr-cust10' : 'http://api.talis.com/stores/zephyr-cust10/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust11' : 'http://api.talis.com/stores/zephyr-cust11/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust12' : 'http://api.talis.com/stores/zephyr-cust12/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust13' : 'http://api.talis.com/stores/zephyr-cust13/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust14' : 'http://api.talis.com/stores/zephyr-cust14/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust15' : 'http://api.talis.com/stores/zephyr-cust15/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust16' : 'http://api.talis.com/stores/zephyr-cust16/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust17' : 'http://api.talis.com/stores/zephyr-cust17/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust18' : 'http://api.talis.com/stores/zephyr-cust18/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust19' : 'http://api.talis.com/stores/zephyr-cust19/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust1' : 'http://api.talis.com/stores/zephyr-cust1/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust2' : 'http://api.talis.com/stores/zephyr-cust2/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust3' : 'http://api.talis.com/stores/zephyr-cust3/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust4' : 'http://api.talis.com/stores/zephyr-cust4/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust5' : 'http://api.talis.com/stores/zephyr-cust5/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust6' : 'http://api.talis.com/stores/zephyr-cust6/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust7' : 'http://api.talis.com/stores/zephyr-cust7/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust8' : 'http://api.talis.com/stores/zephyr-cust8/indexes/metaboxIndex/queryprofiles/default',
						'zephyr-cust9' : 'http://api.talis.com/stores/zephyr-cust9/indexes/metaboxIndex/queryprofiles/default',

			}

		for store_name, qp_uri in qp_uris.items():
			config = pynappl.StoreConfig("http://api.talis.com/stores/%s/config" % store_name)
			self.assertEqual(qp_uri, config.get_first_query_profile_uri())


class FPMapTestCase(unittest.TestCase):
	def test_uri(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/config/fpmaps/1")
		self.assertEqual("http://example.com/store/config/fpmaps/1", fpmap.uri)

	def test_add_mapping_adds_one_mapped_datatype_property(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = None, predicate = FRAME["mappedDatatypeProperty"]))
		self.assertEqual(1, len(mappings))

	def test_add_mapping_adds_mapped_datatype_property_with_fpmap_as_subject(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		self.assertEqual(1, len(mappings))

	def test_add_mapping_adds_mapped_datatype_property_with_hash_uri(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		self.assertEqual('http://example.com/store/fpmaps/1#pred', str(mappings[0]))

	def test_add_mapping_adds_mapped_datatype_property_with_one_name(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		names = list(g.objects(subject = mappings[0], predicate = FRAME["name"]))
		self.assertEqual(1, len(names))
		
	def test_add_mapping_adds_mapped_datatype_property_with_name_of_correct_value(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		names = list(g.objects(subject = mappings[0], predicate = FRAME["name"]))
		self.assertEqual("pred", str(names[0]))

	def test_add_mapping_adds_mapped_datatype_property_with_one_property(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		properties = list(g.objects(subject = mappings[0], predicate = FRAME["property"]))
		self.assertEqual(1, len(properties))
		
	def test_add_mapping_adds_mapped_datatype_property_with_property_of_correct_value(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		properties = list(g.objects(subject = mappings[0], predicate = FRAME["property"]))
		self.assertEqual("http://example.com/pred", str(properties[0]))

	def test_add_mapping_returns_uri_of_mapping(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		mapping_uri = fpmap.add_mapping("http://example.com/pred", "pred")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		self.assertEqual(mapping_uri, str(mappings[0]))
		
	def test_add_mapping_adds_mapped_datatype_property_with_one_analyzer(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred", analyzer="http://example.com/analyzer")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		names = list(g.objects(subject = mappings[0], predicate = BF["analyzer"]))
		self.assertEqual(1, len(names))
		
	def test_add_mapping_adds_mapped_datatype_property_with_analyzer_of_correct_value(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred", analyzer="http://example.com/analyzer")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		analyzers = list(g.objects(subject = mappings[0], predicate = BF["analyzer"]))
		self.assertEqual("http://example.com/analyzer", str(analyzers[0]))

	def test_remove_mapping(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		mapping_uri = fpmap.add_mapping("http://example.com/pred", "pred")
		mapping_uri2 = fpmap.add_mapping("http://example.com/pred2", "pred2")

		fpmap.remove_mapping("http://example.com/pred")

		g = fpmap.graph()
		mapping_object_triples = list(g.triples((None, None, rdflib.term.URIRef(mapping_uri))))
		self.assertEqual(0, len(mapping_object_triples))

		mapping_subject_triples = list(g.objects((rdflib.term.URIRef(mapping_uri), None, None)))
		self.assertEqual(0, len(mapping_subject_triples))

	def test_mappings_returns_dictionary(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		mapping_uri = fpmap.add_mapping("http://example.com/pred", "pred")
		mapping_uri2 = fpmap.add_mapping("http://example.com/pred2", "pred2")

		mappings = fpmap.mappings()
		
		self.assertEqual("pred", mappings["http://example.com/pred"]['name'])
		self.assertEqual("pred2", mappings["http://example.com/pred2"]['name'])


	def test_from_rdfxml(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.from_rdfxml(FPMAP_DATA)
		mappings = fpmap.mappings()
		self.assertEqual("surname", mappings['http://xmlns.com/foaf/0.1/surname']['name'] )
		self.assertEqual("aimchatid2", mappings['http://xmlns.com/foaf/0.1/aimChatID']['name'] )
		self.assertEqual("name", mappings['http://xmlns.com/foaf/0.1/name']['name'] )
		self.assertEqual("family_name", mappings['http://xmlns.com/foaf/0.1/family_name']['name'] )
		self.assertEqual("jabberid", mappings['http://xmlns.com/foaf/0.1/jabberID']['name'] )
		self.assertEqual("yahoochatid", mappings['http://xmlns.com/foaf/0.1/yahooChatID']['name'] )
		self.assertEqual("plan", mappings['http://xmlns.com/foaf/0.1/plan']['name'] )
		self.assertEqual("firstname", mappings['http://xmlns.com/foaf/0.1/firstName']['name'] )
		self.assertEqual("nick", mappings['http://xmlns.com/foaf/0.1/nick']['name'] )
		self.assertEqual("msnchatid", mappings['http://xmlns.com/foaf/0.1/msnChatID']['name'] )
		self.assertEqual("gender", mappings['http://xmlns.com/foaf/0.1/gender']['name'] )
		self.assertEqual("givenname", mappings['http://xmlns.com/foaf/0.1/givenname']['name'] )
		self.assertEqual("mboxsha1sum", mappings['http://xmlns.com/foaf/0.1/mbox_sha1sum']['name'] )
		self.assertEqual("olb", mappings['http://purl.org/vocab/bio/0.1/olb']['name'] )

	def test_add_mapping_multiple_times_loses_earlier_values(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "pred")
		fpmap.add_mapping("http://example.com/pred", "prednew")
		g = fpmap.graph()
		mappings = list(g.objects(subject = rdflib.term.URIRef(fpmap.uri), predicate = FRAME["mappedDatatypeProperty"]))
		names = list(g.objects(subject = mappings[0], predicate = FRAME["name"]))
		self.assertEqual(1, len(names))
		self.assertEqual("prednew", str(names[0]))

	def test_add_mapping_normalises_name(self):
		fpmap = pynappl.FieldPredicateMap("http://example.com/store/fpmaps/1")
		fpmap.add_mapping("http://example.com/pred", "PR.E D!")
		mappings = fpmap.mappings()
		self.assertEqual("pred", mappings["http://example.com/pred"]['name'])


class QueryProfileTestCase(unittest.TestCase):
	def test_uri(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		self.assertEqual("http://example.com/store/config/queryprofiles/1", qp.uri)

	def test_add_field_weight_adds_one_fieldweight_property(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = None, predicate = BF["fieldWeight"]))
		self.assertEqual(1, len(weights))

	def test_add_field_weight_adds_only_one_fieldweight_property_with_qp_as_subject(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		self.assertEqual(1, len(weights))

	def test_add_field_weight_adds_only_one_fieldweight_property_with_hash_uri(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		self.assertEqual("http://example.com/store/config/queryprofiles/1#pred", str(weights[0]))

	def test_add_field_weight_adds_one_name(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		names = list(g.objects(subject = weights[0], predicate = FRAME["name"]))
		self.assertEqual(1, len(names))
		
	def test_add_mapping_adds_name_of_correct_value(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		names = list(g.objects(subject = weights[0], predicate = FRAME["name"]))
		self.assertEqual("pred", str(names[0]))

	def test_add_field_weight_adds_one_weight(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		weight_values = list(g.objects(subject = weights[0], predicate = BF["weight"]))
		self.assertEqual(1, len(weight_values))
		
	def test_add_field_weight_adds_weight_of_correct_value(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		weight_values = list(g.objects(subject = weights[0], predicate = BF["weight"]))
		self.assertEqual("2.0", str(weight_values[0]))

	def test_add_field_weight_returns_uri_of_field_weight(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		field_weight_uri = qp.add_field_weight("pred", "2.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		self.assertEqual(field_weight_uri, str(weights[0]))


	def test_remove_field_weight(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		field_weight_uri1 = qp.add_field_weight("pred", "2.0")
		field_weight_uri2 = qp.add_field_weight("pred2", "4.5")

		qp.remove_field_weight("pred")

		g = qp.graph()
		object_triples = list(g.triples((None, None, rdflib.term.URIRef(field_weight_uri1))))
		self.assertEqual(0, len(object_triples))

		subject_triples = list(g.objects((rdflib.term.URIRef(field_weight_uri1), None, None)))
		self.assertEqual(0, len(subject_triples))

	def test_weights_returns_dictionary(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		field_weight_uri1 = qp.add_field_weight("pred", "2.0")
		field_weight_uri2 = qp.add_field_weight("pred2", "4.5")

		weights = qp.weights()
		self.assertEqual("2.0", weights["pred"])
		self.assertEqual("4.5", weights["pred2"])

	def test_add_field_weight_multiple_times_loses_earlier_values(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.add_field_weight("pred", "2.0")
		qp.add_field_weight("pred", "8.0")
		g = qp.graph()
		weights = list(g.objects(subject = rdflib.term.URIRef(qp.uri), predicate = BF["fieldWeight"]))
		weight_values = list(g.objects(subject = weights[0], predicate = BF["weight"]))
		self.assertEqual(1, len(weight_values))
		self.assertEqual("8.0", str(weight_values[0]))

	def test_from_rdfxml(self):
		qp = pynappl.QueryProfile("http://example.com/store/config/queryprofiles/1")
		qp.from_rdfxml(QP_DATA)
		weights = qp.weights()
		self.assertEqual("5", weights["subject"])
		self.assertEqual("3", weights["subtitle"])
		self.assertEqual("1", weights["label"])


  
if __name__ == "__main__":
  unittest.main()

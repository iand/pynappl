SINGLE_TRIPLE = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:foaf="http://xmlns.com/foaf/0.1/"><rdf:Description><foaf:name>scooby</foaf:name></rdf:Description></rdf:RDF>'
SINGLE_TRIPLE_TURTLE = '[] foaf:name "scooby" .'
SINGLE_TRIPLE_NTRIPLES = '_:a foaf:name "scooby" .'
JOB_URI = "http://example.com/store/jobs/a193f791-b29e-4802-b54e-0d8587d747b3"
JOB_DATA = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:j.0="http://purl.org/dc/terms/" xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
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

STORE_ACCESS_STATUS_RW = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bf="http://schemas.talis.com/2006/bigfoot/configuration#">
  <rdf:Description rdf:about="http://example.com/store/config/access-status">
    <bf:accessMode rdf:resource="http://schemas.talis.com/2006/bigfoot/statuses#read-write"/>
  </rdf:Description>
</rdf:RDF>"""

STORE_ACCESS_STATUS_RO = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bf="http://schemas.talis.com/2006/bigfoot/configuration#">
  <rdf:Description rdf:about="http://example.com/store/config/access-status">
    <bf:retryInterval>30</bf:retryInterval>
    <bf:statusMessage>Being reindexed</bf:statusMessage>
    <bf:accessMode rdf:resource="http://schemas.talis.com/2006/bigfoot/statuses#read-only"/>
  </rdf:Description>
</rdf:RDF>"""

STORE_ACCESS_STATUS_UN = """<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bf="http://schemas.talis.com/2006/bigfoot/configuration#">
  <rdf:Description rdf:about="http://example.com/store/config/access-status">
    <bf:retryInterval>30</bf:retryInterval>
    <bf:statusMessage>Offline for maintenance</bf:statusMessage>
    <bf:accessMode rdf:resource="http://schemas.talis.com/2006/bigfoot/statuses#unavailable"/>
  </rdf:Description>
</rdf:RDF>"""

SELECT_DATA = """<?xml version="1.0"?>
<sparql xmlns="http://www.w3.org/2005/sparql-results#">
  <head>
    <variable name="s"/>
    <variable name="o"/>
  </head>
  <results>
    <result>
      <binding name="s">
        <uri>http://oecd.dataincubator.org/</uri>
      </binding>
      <binding name="o">
        <uri>http://rdfs.org/ns/void#Dataset</uri>
      </binding>
    </result>
    <result>
      <binding name="s">
        <uri>http://oecd.dataincubator.org/glossary/segments/economic-outlook</uri>
      </binding>
      <binding name="o">
        <uri>http://www.w3.org/2004/02/skos/core#Collection</uri>
      </binding>
    </result>
  </results>
</sparql>"""

SEARCH_DATA="""<?xml version='1.0' encoding='UTF-8'?><rdf:RDF xmlns="http://purl.org/rss/1.0/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:ns.0="http://purl.org/vocab/bio/0.1/" xmlns:relevance="http://a9.com/-/opensearch/extensions/relevance/1.0/" xmlns:ns.1="http://www.w3.org/2004/02/skos/core#" xmlns:ns.2="http://xmlns.com/foaf/0.1/" xmlns:ns.3="http://www.w3.org/2002/07/owl#" xmlns:os="http://a9.com/-/spec/opensearch/1.1/"><channel rdf:about="http://api.talis.com/stores/openlibrary/items?query=potter&amp;max=2&amp;offset=0&amp;sort=&amp;xsl=&amp;content-type="><title>potter</title><link>http://api.talis.com/stores/openlibrary/items?query=potter&amp;max=2&amp;offset=0&amp;sort=&amp;xsl=&amp;content-type=</link><description>Results of a search for potter on openlibrary</description><items><rdf:Seq rdf:about="urn:uuid:8f60e82f-d54f-4bbf-a401-a17248dba9b8"><rdf:li resource="http://ol.dataincubator.org/a/OL956224A" /><rdf:li resource="http://ol.dataincubator.org/a/OL953208A" /></rdf:Seq></items><os:startIndex>0</os:startIndex><os:itemsPerPage>2</os:itemsPerPage><os:totalResults>71</os:totalResults></channel><item rdf:about="http://ol.dataincubator.org/a/OL956224A"><title>Item</title><link>http://ol.dataincubator.org/a/OL956224A</link><ns.2:name>Norman Potter</ns.2:name><ns.1:prefLabel>Norman Potter</ns.1:prefLabel><ns.3:sameAs><rdf:Description rdf:about="http://openlibrary.org/a/OL956224A" /></ns.3:sameAs><rdf:type><rdf:Description rdf:about="http://xmlns.com/foaf/0.1/Person" /></rdf:type><relevance:score>1.0</relevance:score></item><item rdf:about="http://ol.dataincubator.org/a/OL953208A"><title>Item</title><link>http://ol.dataincubator.org/a/OL953208A</link><ns.2:name>Potter, Margaret</ns.2:name><ns.1:prefLabel>Potter, Margaret</ns.1:prefLabel><ns.3:sameAs><rdf:Description rdf:about="http://openlibrary.org/a/OL953208A" /></ns.3:sameAs><rdf:type><rdf:Description rdf:about="http://xmlns.com/foaf/0.1/Person" /></rdf:type><ns.0:event><rdf:Description rdf:about="http://ol.dataincubator.org/events/69910" /></ns.0:event><relevance:score>1.0</relevance:score></item></rdf:RDF>"""

SNAPSHOT_DATA="""<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:j.0="http://schemas.talis.com/2006/bigfoot/configuration#" >
  <rdf:Description rdf:about="http://example.com/store">
    <j.0:snapshot rdf:resource="http://example.com/store/snapshots/20090821120029.tar"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://example.com/store/snapshots/20090821120029.tar">
    <j.0:md5 rdf:resource="http://example.com/store/snapshots/20090821120029.tar.md5"/>
    <j.0:filesize>1 MB</j.0:filesize>
    <dc:date>12:00 21-August-2009</dc:date>
  </rdf:Description>
</rdf:RDF>"""

FPMAP_DATA="""<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:j.0="http://schemas.talis.com/2006/frame/schema#" >
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#name">
    <j.0:name>name</j.0:name>
    <j.0:property rdf:resource="http://xmlns.com/foaf/0.1/name"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publisher">
    <j.0:name>publisher</j.0:name>
    <j.0:property rdf:resource="http://purl.org/dc/elements/1.1/publisher"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#date">
    <j.0:name>date</j.0:name>
    <j.0:property rdf:resource="http://vocab.org/bio/0.1/date"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#preflabel">
    <j.0:name>preflabel</j.0:name>
    <j.0:property rdf:resource="http://www.w3.org/2004/02/skos/core#prefLabel"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1">
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publishplace"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#lcclassification"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#label"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#oclcnum"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#pagination"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publisher"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#lccn"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#comment"/>

    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#bystatement"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#subject"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#date"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publishcountry"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#title"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#numberofpages"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#name"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#issued"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#subtitle"/>

    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#preflabel"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#canonicaluri"/>
    <j.0:mappedDatatypeProperty rdf:resource="http://api.talis.com/stores/openlibrary/config/fpmaps/1#type"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publishplace">
    <j.0:name>publishplace</j.0:name>
    <j.0:property rdf:resource="http://olrdf.appspot.com/key/publish_place"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#title">
    <j.0:name>title</j.0:name>
    <j.0:property rdf:resource="http://purl.org/dc/elements/1.1/title"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#label">
    <j.0:name>label</j.0:name>
    <j.0:property rdf:resource="http://www.w3.org/2000/01/rdf-schema#label"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#type">
    <j.0:name>type</j.0:name>
    <j.0:property rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#oclcnum">
    <j.0:name>oclcnum</j.0:name>
    <j.0:property rdf:resource="http://purl.org/ontology/bibo/oclcnum"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#comment">
    <j.0:name>comment</j.0:name>
    <j.0:property rdf:resource="http://www.w3.org/2000/01/rdf-schema#comment"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#subject">
    <j.0:name>subject</j.0:name>
    <j.0:property rdf:resource="http://purl.org/dc/elements/1.1/subject"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#lccn">
    <j.0:name>lccn</j.0:name>
    <j.0:property rdf:resource="http://purl.org/ontology/bibo/lccn"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#bystatement">
    <j.0:name>bystatement</j.0:name>
    <j.0:property rdf:resource="http://olrdf.appspot.com/key/by_statement"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#issued">
    <j.0:name>issued</j.0:name>
    <j.0:property rdf:resource="http://purl.org/dc/terms/issued"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#subtitle">
    <j.0:name>subtitle</j.0:name>
    <j.0:property rdf:resource="http://open.vocab.org/terms/subtitle"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#publishcountry">
    <j.0:name>publishcountry</j.0:name>
    <j.0:property rdf:resource="http://olrdf.appspot.com/key/publish_country"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#canonicaluri">
    <j.0:name>canonicaluri</j.0:name>
    <j.0:property rdf:resource="http://open.vocab.org/terms/canonicalUri"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#numberofpages">
    <j.0:name>numberofpages</j.0:name>
    <j.0:property rdf:resource="http://open.vocab.org/terms/numberOfPages"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#lcclassification">
    <j.0:name>lcclassification</j.0:name>
    <j.0:property rdf:resource="http://olrdf.appspot.com/key/lc_classification"/>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/fpmaps/1#pagination">
    <j.0:name>pagination</j.0:name>
    <j.0:property rdf:resource="http://olrdf.appspot.com/key/pagination"/>
  </rdf:Description>
</rdf:RDF>
"""

QPROFILE_DATA = """<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:j.0="http://schemas.talis.com/2006/frame/schema#"
    xmlns:j.1="http://schemas.talis.com/2006/bigfoot/configuration#" >
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#subject">
    <j.1:weight>1</j.1:weight>
    <j.0:name>subject</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#subtitle">
    <j.1:weight>1</j.1:weight>
    <j.0:name>subtitle</j.0:name>

  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#issued">
    <j.1:weight>1</j.1:weight>
    <j.0:name>issued</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#preflabel">
    <j.1:weight>1</j.1:weight>

    <j.0:name>preflabel</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#lccn">
    <j.1:weight>1</j.1:weight>
    <j.0:name>lccn</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#name">

    <j.1:weight>1</j.1:weight>
    <j.0:name>name</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#comment">
    <j.1:weight>1</j.1:weight>
    <j.0:name>comment</j.0:name>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publishplace">
    <j.1:weight>1</j.1:weight>
    <j.0:name>publishplace</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#date">
    <j.1:weight>1</j.1:weight>
    <j.0:name>date</j.0:name>

  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#numberofpages">
    <j.1:weight>1</j.1:weight>
    <j.0:name>numberofpages</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#title">
    <j.1:weight>1</j.1:weight>

    <j.0:name>title</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publishcountry">
    <j.1:weight>1</j.1:weight>
    <j.0:name>publishcountry</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#bystatement">

    <j.1:weight>1</j.1:weight>
    <j.0:name>bystatement</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#oclcnum">
    <j.1:weight>1</j.1:weight>
    <j.0:name>oclcnum</j.0:name>
  </rdf:Description>

  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#canonicaluri">
    <j.1:weight>1</j.1:weight>
    <j.0:name>canonicaluri</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#lcclassification">
    <j.1:weight>1</j.1:weight>
    <j.0:name>lcclassification</j.0:name>

  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#pagination">
    <j.1:weight>1</j.1:weight>
    <j.0:name>pagination</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#label">
    <j.1:weight>1</j.1:weight>

    <j.0:name>label</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publisher">
    <j.1:weight>1</j.1:weight>
    <j.0:name>publisher</j.0:name>
  </rdf:Description>
  <rdf:Description rdf:about="http://api.talis.com/stores/openlibrary/config/queryprofiles/1">

    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#numberofpages"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#name"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#preflabel"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#comment"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#subtitle"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#label"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#oclcnum"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publisher"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#subject"/>

    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#title"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#lccn"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publishcountry"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#pagination"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#publishplace"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#issued"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#date"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#canonicaluri"/>
    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#lcclassification"/>

    <j.1:fieldWeight rdf:resource="http://api.talis.com/stores/openlibrary/config/queryprofiles/1#bystatement"/>
  </rdf:Description>
</rdf:RDF>"""

# Introduction #

`pynappl` includes a simple command-line utility named `tshell` that allows the user to manually enter and execute  commands against the [Talis Platform](http://www.talis.com/platform). This document provides a brief introduction on how to use the tshell program.


# Getting Started #

The `tshell` program can be found in the `/bin` directory of the pynappl distribution. To start using `tshell` simply type the name of the program in the console:

```
> ./tshell
>>>
```

The Talis Platform is organised into areas called [stores](http://n2.talis.com/wiki/Store) that group together data and services for accessing it. The majority of `tshell` commands act on a store which you can set with the `use` command. For example to set the active store to "space" (i.e. http://api.talis.com/stores/space ):

```
>>> use space
>>>
```

To get a list of commands in the shell use the `help` command:

```
>>> help
```

To exit the shell simply use the `exit` command:

```
>>> exit
>
```

**Note:** in this document, lines prefixed with one angle bracket (>) indicate commands typed on your operating system's console, whereas lines prefixed with three angle brackets (>>>) indicate commands typed in `tshell`


# Exploring a Store #

`tshell` provides several utility commands for exploring the data in a store. These can be useful when you are unfamiliar with a store and want to discover what kind of data it contains. For example, you can see a list of the RDF classes used in the store's metabox:

```
>>> use space
>>> show classes
0. http://rdfs.org/ns/void#Dataset
1. http://purl.org/net/schemas/space/Discipline
2. http://purl.org/net/schemas/space/Launch
3. http://purl.org/net/schemas/space/LaunchSite
4. http://purl.org/net/schemas/space/MissionRole
5. http://purl.org/net/schemas/space/Mission
6. http://xmlns.com/foaf/0.1/Person
7. http://purl.org/net/schemas/space/Spacecraft
8. http://xmlns.com/foaf/0.1/Image
9. http://purl.org/ontology/po/Episode
>>>
```

Once you have a list of classes used in the store you can sample the data in that class using the `sample` command:

```
>>> sample <http://xmlns.com/foaf/0.1/Person>
0. http://nasa.dataincubator.org/person/eugeneandrewcernan
1. http://nasa.dataincubator.org/person/neilaldenarmstrong
2. http://nasa.dataincubator.org/person/donnfultoneisele
3. http://nasa.dataincubator.org/person/leroygordoncooperjr
4. http://nasa.dataincubator.org/person/edgardeanmitchell
5. http://nasa.dataincubator.org/person/charlesmossdukejr
6. http://nasa.dataincubator.org/person/joehenryengle
7. http://nasa.dataincubator.org/person/jackrobertlousma
8. http://nasa.dataincubator.org/person/brucemccandlessii
9. http://nasa.dataincubator.org/person/johnwattsyoung
>>>
```

It can be a bit tedious to type out the full URI of a class so `tshell` lets you use prefixed names like this:

```
>>> sample foaf:Person
0. http://nasa.dataincubator.org/person/eugeneandrewcernan
1. http://nasa.dataincubator.org/person/neilaldenarmstrong
2. http://nasa.dataincubator.org/person/donnfultoneisele
3. http://nasa.dataincubator.org/person/leroygordoncooperjr
4. http://nasa.dataincubator.org/person/edgardeanmitchell
5. http://nasa.dataincubator.org/person/charlesmossdukejr
6. http://nasa.dataincubator.org/person/joehenryengle
7. http://nasa.dataincubator.org/person/jackrobertlousma
8. http://nasa.dataincubator.org/person/brucemccandlessii
9. http://nasa.dataincubator.org/person/johnwattsyoung
>>>
```

`tshell` comes with an inbuilt set of prefix mappings. You can see them with the `list prefixes` command:

```
>>> list prefixes
foaf: <http://xmlns.com/foaf/0.1/>
owl: <http://www.w3.org/2002/07/owl#>
xsd: <http://www.w3.org/2001/XMLSchema#>
bibo: <http://purl.org/ontology/bibo/>
rdfs: <http://www.w3.org/2000/01/rdf-schema#>
skos: <http://www.w3.org/2004/02/skos/core#>
void: <http://rdfs.org/ns/void#>
geonames: <http://www.geonames.org/ontology/>
dc: <http://purl.org/dc/elements/1.1/>
rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
rel: <http://purl.org/vocab/relationship/>
dbp: <http://dbpedia.org/resource/>
cs: <http://purl.org/vocab/changeset/schema#>
ov: <http://open.vocab.org/terms/>
dct: <http://purl.org/dc/terms/>
rss: <http://purl.org/rss/1.0/>
geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
dbpo: <http://dbpedia.org/ontology/>
>>>
```

You can add your own prefixes with the `prefix` command. For example, we could add a prefix for the space vocabulary used by the space store like this:

```
>>> prefix space <http://purl.org/net/schemas/space/>
>>>
```

Now we can sample the space launches:

```
>>> sample space:Launch
0. http://nasa.dataincubator.org/launch/1957-001
1. http://nasa.dataincubator.org/launch/1957-002
2. http://nasa.dataincubator.org/launch/1958-001
3. http://nasa.dataincubator.org/launch/1958-002
4. http://nasa.dataincubator.org/launch/1958-003
5. http://nasa.dataincubator.org/launch/1958-004
6. http://nasa.dataincubator.org/launch/1958-005
7. http://nasa.dataincubator.org/launch/1958-006
8. http://nasa.dataincubator.org/launch/1958-007
9. http://nasa.dataincubator.org/launch/1958-008
>>>
```

The `describe` command allows us to fetch the store's description of any resource. Normally it is used with a URI in angle brackets just like the `sample` command earlier. You could also use a prefixed name if there is a suitable prefix for the URI. However, there is an even simpler method. You may have noticed that each result of the `sample` command is numbered. Whenever you see a numbered list in `tshell` you can use the number as a shortcut for the URI. So to fetch a description of http://nasa.dataincubator.org/launch/1958-001 we could type:

```
>>> describe 2
@prefix space: <http://purl.org/net/schemas/space/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://nasa.dataincubator.org/launch/1958-001> a space:Launch;
    space:launched "1958-02-01"^^xsd:date;
    space:launchsite <http://nasa.dataincubator.org/launchsite/capecanaveral>;
    space:launchvehicle "Jupiter C (Juno I)";
    space:spacecraft <http://nasa.dataincubator.org/spacecraft/1958-001A> .

>>>
```

The numbered shortcuts persist until a new results list is shown. So we can describe item 5 on the list:

```
>>> describe 5
@prefix space: <http://purl.org/net/schemas/space/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://nasa.dataincubator.org/launch/1958-004> a space:Launch;
    space:launched "1958-05-15"^^xsd:date;
    space:launchsite <http://nasa.dataincubator.org/launchsite/tyuratambaikonurcosmodrome>;
    space:launchvehicle "Modified SS-6 (Sapwood)";
    space:spacecraft <http://nasa.dataincubator.org/spacecraft/1958-004B> .


>>>
```

We can continue exploring the data using the `describe` command:

```
>>> describe <http://nasa.dataincubator.org/spacecraft/1958-004B>
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix space: <http://purl.org/net/schemas/space/> .

<http://nasa.dataincubator.org/spacecraft/1958-004B> a space:Spacecraft;
    dc:description "Sputnik 3 was an automatic scientific laboratory spacecraft. It was 
    conically-shaped and was 3.57 m long. The scientific instrumentation 
    (twelve instruments) provided data on pressure and composition of the upper 
    atmosphere, concentration of charged particles, photons in cosmic rays, heavy 
    nuclei in cosmic rays, magnetic and electrostatic fields, and meteoric particles. 
    The outer radiation belts of the Earth were detected during the flight. The 
    spacecraft remained in orbit until April 6, 1960. ";
    space:agency "U.S.S.R";
    space:alternateName "00008";
    space:discipline <http://nasa.dataincubator.org/discipline/astronomy>,
        <http://nasa.dataincubator.org/discipline/earthscience>,
        <http://nasa.dataincubator.org/discipline/lifescience>,
        <http://nasa.dataincubator.org/discipline/spacephysics>;
    space:internationalDesignator "1958-004B";
    space:launch <http://nasa.dataincubator.org/launch/1958-004>;
    space:mass "1327.0";
    foaf:homepage <http://nssdc.gsfc.nasa.gov/database/MasterCatalog?sc=1958-004B>;
    foaf:name "Sputnik 3" .

>>> 
```

# Searching #

As well as exploring a store using the `show classes`, `sample` and `describe` commands, `tshell` allows you to free text search the data in a store. The `search` command is used like this:

```
>>> search james
0. STS 51C (http://nasa.dataincubator.org/spacecraft/1985-010A)
1. Apollo 15 Command and Service Module (CSM) (http://nasa.dataincubator.org/spacecraft/1971-063A)
2. STS 48 (http://nasa.dataincubator.org/spacecraft/1991-063A)
3. James Benson Irwin (http://nasa.dataincubator.org/person/jamesbensonirwin)
4. James Alton McDivitt (http://nasa.dataincubator.org/person/jamesaltonmcdivitt)
5. Gemini 4 (http://nasa.dataincubator.org/spacecraft/1965-043A)
6. James Arthur Lovell, Jr. (http://nasa.dataincubator.org/person/jamesarthurlovelljr)
7. Apollo 13 Command and Service Module (CSM) (http://nasa.dataincubator.org/spacecraft/1970-029A)
8. STS 41C (http://nasa.dataincubator.org/spacecraft/1984-034A)
9. Apollo 9 (http://nasa.dataincubator.org/spacecraft/1969-018A)
>>> 
```

Once again we have a numbered result list so we can `describe` any result on that list very simply:

```
>>> describe 6
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix space: <http://purl.org/net/schemas/space/> .

<http://nasa.dataincubator.org/person/jamesarthurlovelljr> a foaf:Person;
    space:performed <http://nasa.dataincubator.org/mission/apollo-11/role/backup-commander>,
        <http://nasa.dataincubator.org/mission/apollo-11/role/capsule-communicator/3>,
        <http://nasa.dataincubator.org/mission/apollo-13/role/commander>,
        <http://nasa.dataincubator.org/mission/apollo-8/role/command-module-pilot>;
    foaf:name "James Arthur Lovell, Jr." .

>>>
```

# SPARQL #

`tshell` makes executing SPARQL queries very simple. The `sparql` command takes a single argument which is the SPARQL query to run. The one limitation is that the sparql query must be all on a single line. For clarity in the examples below, the sparql query is split over several lines but you should ensure they are all entered on a single line when you use the `sparql` command.

For SPARQL select queries, the results are shown as a simple table:

```
>>> sparql select * where {?s a  <http://xmlns.com/foaf/0.1/Person> . } limit 10
                           s                            
========================================================
http://nasa.dataincubator.org/person/eugeneandrewcernan 
http://nasa.dataincubator.org/person/neilaldenarmstrong 
 http://nasa.dataincubator.org/person/donnfultoneisele  
http://nasa.dataincubator.org/person/leroygordoncooperjr
 http://nasa.dataincubator.org/person/edgardeanmitchell 
 http://nasa.dataincubator.org/person/charlesmossdukejr 
   http://nasa.dataincubator.org/person/joehenryengle   
 http://nasa.dataincubator.org/person/jackrobertlousma  
 http://nasa.dataincubator.org/person/brucemccandlessii 
  http://nasa.dataincubator.org/person/johnwattsyoung   
```

SPARQL describe and construct queries show the results as turtle:

```
>>> sparql describe <http://nasa.dataincubator.org/person/johnwattsyoung>
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix space: <http://purl.org/net/schemas/space/> .

<http://nasa.dataincubator.org/person/johnwattsyoung> a foaf:Person;
    space:performed <http://nasa.dataincubator.org/mission/apollo-10/role/command-module-pilot>,
        <http://nasa.dataincubator.org/mission/apollo-13/role/backup-commander>,
        <http://nasa.dataincubator.org/mission/apollo-13/role/capsule-communicator/3>,
        <http://nasa.dataincubator.org/mission/apollo-16/role/commander>,
        <http://nasa.dataincubator.org/mission/apollo-17/role/backup-commander>,
        <http://nasa.dataincubator.org/mission/apollo-17/role/capsule-communicator/8>,
        <http://nasa.dataincubator.org/mission/apollo-7/role/backup-command-module-pilot>,
        <http://nasa.dataincubator.org/mission/apollo-7/role/capsule-communicator/4>;
    foaf:name "John Watts Young" .
>>> 
```

When you use the `sparql` command `tshell` will automatically expand prefixed URIs using your existing prefix mappings. That means you can write SPARQL queries very naturally like this:

```
>>> sparql select ?name ?image where { ?spacecraft foaf:name ?name ; foaf:depiction ?image.} limit 5
   name    |                               image                              
===========+==================================================================
Sputnik 1  |     http://nssdc.gsfc.nasa.gov/planetary/image/sputnik_asm.jpg   
Sputnik 2  |    http://nssdc.gsfc.nasa.gov/image/spacecraft/sputnik2_vsm.jpg  
Explorer 1 |     http://nssdc.gsfc.nasa.gov/image/spacecraft/explorer_1.gif   
Vanguard 1 | http://nssdc.gsfc.nasa.gov/image/spacecraft/vanguard_1_rocket.jpg
Pioneer 1  |    http://nssdc.gsfc.nasa.gov/image/spacecraft/pioneer_able.gif  
>>> 
```

This expansion of prefixes also works for datatypes:

```
>>> sparql ask where { ?launch space:launched "1969-07-16"^^xsd:date.}
Yes
>>> 
```

It makes long and complex queries easier to manage:

```
>>> sparql construct { ?spacecraft foaf:name ?name; space:agency ?agency; 
    space:mass ?mass. } where { ?launch space:launched "1969-07-16"^^xsd:date. 
    ?spacecraft space:launch ?launch; foaf:name ?name; space:agency ?agency; 
    space:mass ?mass. }
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix space: <http://purl.org/net/schemas/space/> .

<http://nasa.dataincubator.org/spacecraft/1969-059A> space:agency "United States";
    space:mass "28801.0";
    foaf:name "Apollo 11 Command and Service Module (CSM)" .

<http://nasa.dataincubator.org/spacecraft/1969-059B> space:agency "United States";
    space:mass "13300.0";
    foaf:name "Apollo 11 SIVB" .

<http://nasa.dataincubator.org/spacecraft/1969-059C> space:agency "United States";
    space:mass "15065.0";
    foaf:name "Apollo 11 Lunar Module / EASEP" .


>>> 
```

# Storing RDF #

`tshell` provides a `store` command for loading RDF data from your local filesystem into a store's metabox. Most stores are secured for writes so you will need to provide authentication details. You can do this using the `login` command:

```
>>> login
Username: user
Password: ******
>>> 
```

This authentication lasts until you exit `tshell` or you use the `login` command. There is no logout command as yet. If you attempt an action that requires authentication, you will be prompted as part of that command:


```
>>> store /tmp/data.rdf
Unauthorized
Username: user
Password: ******
>>>
```

**Note:** the type of data being stored is determined from the file extension. .nt and .ttl are uploaded as text/turtle.

# Patching Data #

As well as loading RDF into a store, `tshell` provides commands for making small changes to the data. The `add` command enables you to add a single triple to the store's metabox:

```
>>> add <http://example.com/jane> <http://xmlns.com/foaf/0.1/name> "Jane"
>>> describe <http://example.com/jane>
@prefix dir: <http://schemas.talis.com/2005/dir/schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.com/jane>
    dir:etag "db0d4985-ca5c-43b2-a88d-f968c5f71b1e";
    foaf:name "Jane" .
    
>>> 
```

The `add` command also expands prefixed names just like the `sparql` command:

```
>>> add <http://example.com/jane> rdf:type foaf:Person
>>> describe <http://example.com/jane>
@prefix dir: <http://schemas.talis.com/2005/dir/schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.com/jane> a foaf:Person
    dir:etag "db0d4985-ca5c-43b2-a88d-f968c5f71b1e";
    foaf:name "Jane" .
    
>>> 
```

The counterpart to the `add` command is the `remove` command, which allows you to remove triples from a store. Behind the scenes the `remove` command creates a [changeset](http://n2.talis.com/wiki/Changesets) and posts it to the store for you.

```
>>> remove <http://example.com/jane> rdf:type foaf:Person
Applying changeset 1/1 (927 bytes)...
>>> describe <http://example.com/jane>
@prefix dir: <http://schemas.talis.com/2005/dir/schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.com/jane> 
    dir:etag "7c805259-844f-4f52-88f7-ffac82b31595";
    foaf:name "Jane" .

>>> 
```

You can remove multiple triples at the same time by omitting one of the arguments to the `remove` command. For example, to remove all rdf:type properties from a resource:

```
>>> add <http://example.com/jane> rdf:type foaf:Person
>>> add <http://example.com/jane> rdf:type foaf:Agent
>>> describe <http://example.com/jane>
@prefix dir: <http://schemas.talis.com/2005/dir/schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.com/jane> a foaf:Agent,
        foaf:Person;
    dir:etag "cb1267b3-2cd1-4e25-b864-37113e84a81c";
    foaf:name "Jane" .


>>> remove <http://example.com/jane> rdf:type
Querying data...
Applying changeset 1/1 (1325 bytes)...
>>> describe <http://example.com/jane>
@prefix dir: <http://schemas.talis.com/2005/dir/schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.com/jane> 
    dir:etag "fc3a89ac-17ee-4263-851f-015a2e5ef5e6";
    foaf:name "Jane" .

```

Arguments in the subject and predicate position can be omitted by specifying a single hyphen (-) in their place. For example, you can remove all triples that specify things are of rdf:type foaf:Person like this:

```
>>> add <http://example.com/jane> rdf:type foaf:Person
>>> add <http://example.com/john> rdf:type foaf:Person
>>> add <http://example.com/jane> foaf:name "Jane"
>>> add <http://example.com/john> foaf:name "John"
>>> sample foaf:Person
0. http://example.com/jane
1. http://example.com/john
>>> remove - rdf:type foaf:Person
Querying data...
Applying changeset 1/1 (1680 bytes)...
>>> sample foaf:Person
>>> 
```

Obviously you should be careful when using the `remove` command because this wildcard behaviour could remove more triples than you were expecting. Also it is not designed for large scale data editing, but for small patches to the data.

# Store Management #

Talis Platform stores support a number of [bulk operations](http://n2.talis.com/wiki/Job) that enable the data in the store to be managed. `tshell` supports a number of them. To take a snapshot of a store use the `snapshot` command. This schedules a snapshot job with the Talis Platform and waits for it to complete. The snapshot job creates a tar file containing all the RDF and binary content in the store and makes it available for download.

```
>>> snapshot
Job scheduled at 'http://api.talis.com/stores/mystore/jobs/aacb7f53-2bbb-4a55-b104-e64fb31a64e8'
Waiting for job to complete
Job in progress: Creating temporary files.
Job finished
Snapshot is at 'http://api.talis.com/stores/mystore/snapshots/20100515143207.tar'
>>> 
```

A related command is `backup` which performs a snapshot but also downloads it to a local file. You need to supply the filename which must be in a writeable location.

```
>>> backup /tmp/backup.tar
Job scheduled at 'http://api.talis.com/stores/mystore/jobs/8e4a8eaf-0a54-4646-9cb1-b341705c80ab'
Waiting for job to complete
Job in progress: Creating temporary files.
Job in progress: Setting the store to read write.
Job finished
Downloading 'http://api.talis.com/stores/mystore/snapshots/20100515143416.tar' to '/tmp/backup.tar'
>>> 
```

The `reset` command clears all of the data out of a store. It's probably best to take a backup of a store before resetting it because there is no undo!

```
>>> reset
Job scheduled at 'http://api.talis.com/stores/mystore/jobs/ed77463d-8b42-4b36-be68-32e04a2023f5'
Waiting for job to complete
Job in progress: Reset Data job running for store.
Job finished
>>> 
```

The `reindex` command request a reindex job be scheduled and run. This is needed if you update the store's field/predicate map.

The `restore` command restores a snapshot to the store. You need to supply the location of a valid snapshot to be restored. This can be a URI or it can be the filename of a local file. If you supply the latter `tshell` will upload the snapshot to the store's contentbox and perform the restore from there.

```
>>> restore http://api.talis.com/stores/mystore/snapshots/20100515143416.tar
Job scheduled at 'http://api.talis.com/stores/mystore/jobs/9ba448ab-2fc4-4da7-9688-b8ad52627432'
Waiting for job to complete
Job in progress: Checking if store exists.
Job finished
>>>

>>> restore /tmp/backup.tar
To restore from a local file, it needs to be uploaded to the content box.
Continue? (y/n) y
Job scheduled at 'http://api.talis.com/stores/mystore/jobs/d839371f-5557-4f6d-8473-871f2ead70c3'
Waiting for job to complete
Job in progress: Checking if store exists.
Job finished
>>> 
```


# Configuring a Store #

One of the important tasks when using a Talis Platform store is configuring the [field/predicate map](http://n2.talis.com/wiki/Field_Predicate_Map) for free text searching. Many people find this quite complex so `tshell` aims to make this process very simple by providing an interactive field/predicate map editor. To start the editor, just type the `fpmap` command. You should see the fpmap prompt:

```
>>> fpmap
fpmap> 
```

To see the current field/predicate map use the `view` command:

```
fpmap> view
http://example.com/terms/signals -> s
http://purl.org/rss/1.0/title -> title
fpmap> 
```

You can add a mapping using the `add` command which takes a property URI and a short field name as arguments:

```
fpmap> add <http://xmlns.com/foaf/0.1/name> name
fpmap*> view
http://xmlns.com/foaf/0.1/name -> name
http://example.com/terms/signals -> s
http://purl.org/rss/1.0/title -> title
fpmap*> 
```

Note that the fpmap prompt now displays an asterisk. This indicates that the field/predicate map has unsaved changes. As usual, the `add` command supports prefixed names for URIs:

```
fpmap*> add foaf:surname surname
fpmap*> view
http://xmlns.com/foaf/0.1/name -> name
http://example.com/terms/signals -> s
http://purl.org/rss/1.0/title -> title
http://xmlns.com/foaf/0.1/surname -> surname
fpmap*> 
```

To remove a mapping, use the `remove` command:

```
fpmap*> remove <http://example.com/terms/signals>
fpmap*> view
http://xmlns.com/foaf/0.1/name -> name
http://purl.org/rss/1.0/title -> title
http://xmlns.com/foaf/0.1/surname -> surname
fpmap*> 
```

Finally, when your changes are complete, use the `save` command and `exit` to leave the fpmap editor:

```
fpmap*> save
fpmap> exit
>>>
```

If you change the fpmap you may want to reindex or reload your data.

# Scripting #

`tshell` supports running batches of commands as scripts. To use this feature, create a file containing the commands you want to execute. For example, the following could be in a file called /tmp/space-classes

```
use space
show classes
```

You can now run this script with `tshell` simply by specifying it as a parameter on the command line:

```
> ./tshell /tmp/space-classes
0. http://rdfs.org/ns/void#Dataset
1. http://purl.org/net/schemas/space/Discipline
2. http://purl.org/net/schemas/space/Launch
3. http://purl.org/net/schemas/space/LaunchSite
4. http://purl.org/net/schemas/space/MissionRole
5. http://purl.org/net/schemas/space/Mission
6. http://xmlns.com/foaf/0.1/Person
7. http://purl.org/net/schemas/space/Spacecraft
8. http://xmlns.com/foaf/0.1/Image
9. http://purl.org/ontology/po/Episode
```

You can also execute this script from within `tshell` by using the `run` command:

```
>>> run /tmp/space-classes
0. http://rdfs.org/ns/void#Dataset
1. http://purl.org/net/schemas/space/Discipline
2. http://purl.org/net/schemas/space/Launch
3. http://purl.org/net/schemas/space/LaunchSite
4. http://purl.org/net/schemas/space/MissionRole
5. http://purl.org/net/schemas/space/Mission
6. http://xmlns.com/foaf/0.1/Person
7. http://purl.org/net/schemas/space/Spacecraft
8. http://xmlns.com/foaf/0.1/Image
9. http://purl.org/ontology/po/Episode
```

Here's a neat trick. If you are using a UNIX based system then you can take advantage of the shebang notation to make your scripts automatically executable by `tshell`. Modify the "space-classes" file to look like the following and rthen make it executable.

```
#! /path/to/pynappl/bin/tshell
use space
show classes
```

Now you can run the comand without needing to specify the `tshell` component:

```
> ./space-classes
0. http://rdfs.org/ns/void#Dataset
1. http://purl.org/net/schemas/space/Discipline
2. http://purl.org/net/schemas/space/Launch
3. http://purl.org/net/schemas/space/LaunchSite
4. http://purl.org/net/schemas/space/MissionRole
5. http://purl.org/net/schemas/space/Mission
6. http://xmlns.com/foaf/0.1/Person
7. http://purl.org/net/schemas/space/Spacecraft
8. http://xmlns.com/foaf/0.1/Image
9. http://purl.org/ontology/po/Episode
```

`tshell` also allows you to save the commands you executed in your session to a file. Use the `save history` command and specify a filename the commands should be saved to:

```
>>> save history /tmp/history.txt
>>>
```

## Example Scripts ##

This script backups up a store, resets it and then loads in some data:

```
#! /path/to/pynappl/bin/tshell
use mystore
login user password
backup /path/to/backups/mystore-backup.tar
reset
store /path/to/data/mydata.ttl
```
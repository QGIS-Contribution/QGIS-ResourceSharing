Implementation addendum
-----------------------

R script support
................

R scripts that are placed in::

  collections``/<collections registry name>/rscripts

will be imported into the default

  processing/rscripts

folder in user QGIS directory.
If that directory is in the Proccessing R Provider
``R scripts folder`` path, the scripts will become available
in the Processing Toolbox under R.

The "QGIS Resources Sharing Repository" (https://github.com/qgis/QGIS-Resources)
contains the QGIS 2 R online scripts, and serves as a
demonstion.


Conversation Ale-Akbar from 15/07/2016
.......................................


We need an independent function (no qgis imports!) to check the XML before we import it,
we need to check for wrong SVG or images paths (or whatever other paths could be in there).

The same or similar function could maybe be useful to import or export projects.

The idea is that we can re-use the same function when the user wants to create
a collection before she exports/share it.

The function should be able to fix the paths (relative!) and to optionally copy
the SVGs/images in the right place before exporting/sharing.



Pseudo code:

def fix_collection(collection_path, xml, default_search_paths=[], additional_search_paths=[], copy=False):
    """/home/ale/Collection 1 (2303210392103921039)
    <xml .... ?>
    ~/ale/.qgis2/svg
    ~/ale/.qgis2/svg
    ~/ale/.qgis2/svg
    """
    for each path inside xml
        find the SVG or the IMAGE in default search path
        find the SVG or the IMAGE in additional search path
        if found:
            if path is wrong:
                if copy:
                    copy SVGs to collection in the right place
                fix path
        else:
            add to error list
    return fixed_xml, errors_warnings

# Call as
fixed_xml = fix_collection('/collection_path (0231232131)/', '<xml ....>', [QgsApplication.instance().pkgDataPath() + '/svg/', QgsApplication.instance().qgisSettingsDirPath() + '/svg/'], ['/svg1/', '/svg2'])



Conversation Ale-Akbar from 11/07/2016
.......................................


We discussed again how to import SVGs and symbols and some problems:

1. what to do with SVG paths stored in styles or symbols XMLs when they contain wrong relative paths
2. how to deal with duplicated symbol names
3. how to import symbols XML and group them at the same time

1. we decided to do some post-import processing with the XMLs to rewrite the wrong
   paths to add the name (with hash) of the collection, so that the rewrite will be, for example:

from::

    <prop k="name" v="../../my_svg_path/svg/transport_fuel.svg"/>

to::

    <prop k="name" v="Collection 1 (6d38d61abd52a05495dfd3189b04)/svg/transport_fuel.svg"/>


2. Akbar had the good idea of adding the collection hash to all symbol names, this
   will avoid name collisions and solve the 3. at the same time because we could
   easily group the symbols querying for the hash in the name




Conversation Ale-Akbar from 08/07/2016
.......................................

We discussed again how to import SVGs and symbols:

SVGs
----

Now saved in ``/home/user/.qgis2/symbology_sharing/collections/6d38d61abd52a05495dfd3189b04900a3cc73c36/svg/`

Problem: in the GUI SVG selector tree all collections appear under "User Symbols"
Solution: move all the symbology sharing related collections outside `.qgis2` (in the parent folder)

Problem: in the GUI SVG selector tree all collections appear with the hash `6d38d61abd52a05495dfd3189b04900a3cc73c36`
Solution: the only purpose of the hash is to avoid collection name collisions, we can change the folder name to be the name of the collection followed by the hash in brackets, like::

    /home/ale/.qgis2/symbology_sharing
    ├── collections
    │   ├── King's Landing (6d38d61abd52a05495dfd3189b04900a3cc73c36)
    │   │   ├── colorramp
    │   │   │   └── rainbows.xml
    │   │   ├── image
    │   │   │   └── QGis_Logo.png
    │   │   ├── license
    │   │   ├── preview
    │   │   │   ├── osm_spatialite_googlemaps_lines.qml.png
    │   │   │   └── osm_spatialite_googlemaps.png
    │   │   ├── style
    │   │   │   ├── osm_spatialite_googlemaps_lines.qml
    │   │   │   ├── osm_spatialite_googlemaps_multipolygon.qml
    │   │   │   └── osm_spatialite_googlemaps_places.qml
    │   │   ├── svg
    │   │   │   └── Blank_shield.svg
    │   │   └── symbol
    │   │       ├── osm_symbols.xml
    │   │       ├── symbol_collection_svg.xml
    │   │       ├── symbol_qgisdefault_svg.xml
    │   │       └── symbol_rasterimagefill.xml
    │   └── Westeros (ed86f2b4406dbd2c9afce1da12436836a89d3a5b)
    │       └── license


Symbols
-------

Problem: The symbol import from XML GUI in QGIS does not seem to work!

TODO:
* check if the bug is reported in the hub
* try to make a python test case using the API
* try to fix it

Problem: symbols names must be unique

TODO:
* check why it is like that (ask to qgis-dev list and Martin and Nyall)
* what if the constraint is removed upstream?
* what if the symbol search is done first using the name **and** the group and then (if nothing was found) by using the name alone?
* other option: ask the user what to do (rename the imported || rename the old one || overwrite the old one)


Conversation Ale-Akbar from 01/07/2016
.......................................


We discussed how to import SVGs and symbols:

SVGs
----

Add the SVG path to the settings as QgsApplication does

QString myPaths = settings.value( "svg/searchPathsForSVG", QDir::homePath() ).toString();


Symbols
---------

Using the API provided by QgsStyleV2 for:

#. tag all symbols with the collection id
#. create a group with the name of the collection and place all symbols inside (check for other groups with the same name and add a suffix if needed)
#. place all symbols in the group

Collection removal
------------------

#. remove the path from SVG paths setting
#. remove all tagged symbols
#. find the empty group starting with the same name of the collection and delete it



Conversation Ale-Akbar from 24/06/2016
.......................................

https://github.com/akbargumbira/qgis_symbology_sharing/blob/master/symbology_sharing/repository_manager.py#L12

Shouldn't this be a DIRECTORY of repositories? It's better to rename this to DIRECTORY
to avoid confusion with the actual REPOSITORIES

In my mind, we have 3 objects:

DIRECTORY of repositories, a list of URLs where to fetch metadata.ini for the repos
          this is the same as plugins.xml for plugin manager
REPOSITORY, a set of collections, described by metadata.ini
COLLECTION, a set of QGIS resources


Example repository DIRECTORY file::

    git@github.com/anitagraser/QGIS-style-repo-dummy.git # Official repo
    git@github.com:qgis/QGIS.git # My Amazing repo
    http://www.repo.com/repo1 # Repository title
    ftp://ftp.repo.cmo/repo1  # Title of this FTP repo
    scp://user@server:/fany_repo # SSH repo
    ...

Or, CSV::

    git@github.com/anitagraser/QGIS-style-repo-dummy.git,Official repository
    http://www.repo.com/repo1,Repository title


Example metadata.ini::

    [general]
    author=Anita Graser
    email=anitagraser@gmx.at
    collections=collection_1, collection_2

    [collection_1]
    name=OSM Spatialite Googlemaps
    tags=osm, spatialite, google maps, roads
    description=The collection contains a complete resources to create a coherent map that looks similar to the old Google Maps style from OSM data in a SpatiaLite database
    qgis_minimum_version=2.0
    qgis_maximum_version=2.99

    [collection_2]
    name=OSM Spatialite Googlemaps 2
    tags=osm, spatialite, google maps, roads
    description=The collection 2 contains a complete resources to create a coherent map that looks similar to the old Google Maps style from OSM data in a SpatiaLite database
    qgis_minimum_version=2.0
    qgis_maximum_version=2.99



Let's recap:

1. the QGIS user launch the plugins
2. the plugin enters DISCOVERY phase: fetches the DIRECTORY to get a list of REPOSITORIES
3. the plugin loops through the REPOSITORIES and fetches metadata.ini
4. the plugin handle updates for installed collections [TODO]
5. the plugin is ready for COLLECTIONs browsing/installing etc.

steps 2-4 are done automatically if a flag is set in the settings (default True).

This process is somewhat similar to what happens for QGIS plugin manager.

Notes:
1. DIRECTORY of repos, store a list of remote repos with their protocol, if an handler for that
   protocol does **not** exists we warn the user and skip that repo
2. every time we access the network we do it through QgsNetworkAccessManager (https://qgis.org/api/classQgsNetworkAccessManager.html)
   in order to use credentials stored in QGIS auth DB
3. if a new repo appears in the DIRECTORY file we should ask the user if
   he wants to add id (default = "Add all new repos"), low priority:
   just add them all at this time
4. low priority: we could store the name in the DIRECTORY of repos, by
   using csv or a # separator or whatever you think is best

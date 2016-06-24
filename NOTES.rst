Implementation addendum
-----------------------

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


Example repository DIRECTORY file:
git@github.com/anitagraser/QGIS-style-repo-dummy.git # Official repo
git@github.com:qgis/QGIS.git # My Amazing repo
http://www.repo.com/repo1 # Repository title
ftp://ftp.repo.cmo/repo1  # Title of this FTP repo
scp://user@server:/fany_repo # SSH repo
...

Or, CSV:
git@github.com/anitagraser/QGIS-style-repo-dummy.git,Official repository
http://www.repo.com/repo1,Repository title


Example metadata.ini:

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

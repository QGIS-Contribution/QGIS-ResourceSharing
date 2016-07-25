---
layout: page
title: "Creating Metadata"
category: doc
date: 2016-07-25 14:58:04
---

In the root of the repository, you need to create a metadata file defining 
the information about the repository and the collections inside the repository. 

The metadata file (```metadata.ini```) needs to have ```general``` section 
with this information:

**Name** | **Status** | **Description**
author | Required | Author's name
email | Required | Author's email
collection | Required | List of the collection register name separated by comma (This has to match with the directory name of the collection)


For each collection, you need to also define its metadata. The section must 
be named by its register name defined in the general section. This is the 
contents of the collection section:

**Name** | **Status** | **Description**
name | Required | The name of the collection that will be shown
tags | Required | List of tags separated by comma
description | Required | Additional information describing the collection
preview | Optional | List of preview images relative to ```preview``` directory separated by comma
qgis_minimum_version | Required | Dotted notation of minimum QGIS version
qgis_maximum_vesion | Required | Dotted notation of maximum QGIS version


This is an example of the ```metadata.ini``` file:

```
[general]
author=Anita Graser
email=anitagraser@gmx.at
collections=osm_spatialite_googlemaps,flowmap


[osm_spatialite_googlemaps]
name=OSM Spatialite Googlemaps
tags=osm, spatialite, google maps, roads
description=The collection contains a complete resources to create a coherent map that looks similar to the old Google Maps style from OSM data in a SpatiaLite database
preview=osm_spatialite_googlemaps.png, osm_spatialite_googlemaps_lines.qml.png
qgis_minimum_version=2.0
qgis_maximum_version=2.99

[flowmap]
name=Flowmap
tags=flows, arrows
description=The collection contains styles for flow maps
preview=preview.png
qgis_minimum_version=2.0
qgis_maximum_version=2.99
```





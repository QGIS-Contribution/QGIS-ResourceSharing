---
layout: page
title: "Creating Metadata"
category: author
date: 2016-07-25 14:58:04
order: 4
---

In the root of the repository, you need to create a metadata file defining 
the information about the repository and the collections inside the repository. 

The metadata file (```metadata.ini```) needs to have ```general``` section 
with this information:

**Name** | **Status** | **Description**
collection | Required | List of the collection register name separated by comma (This has to match with the directory name of the collection)

For each collection, you need to also define its metadata. The section must 
be named by its register name defined in the general section. This is the 
contents of the collection section:

**Name** | **Status** | **Description**
name | Required | The name of the collection that will be shown
author | Required | Author's name
email | Required | Author's email
tags | Required | List of tags separated by comma
description | Required | Additional information describing the collection
preview | Optional | List of preview images relative to the collection root separated by comma
qgis_minimum_version | Optional | Dotted notation of minimum QGIS version. If not specified, the minimum version will be 2.0
qgis_maximum_version | Optional | Dotted notation of maximum QGIS version. If not specified, the maxium version will be 3.99
license | Optional | The license of the collection e.g GNU GPL
license_file | Optional | License file path relative to the collection root

This is an example of the ```metadata.ini``` file:

```
[general]
collections=osm_spatialite_googlemaps,flowmap

[osm_spatialite_googlemaps]
name=OSM Spatialite Googlemaps
author=Anita Graser
email=anitagraser@gmx.at
tags=osm, spatialite, google maps, roads
description=The collection contains a complete resources to create a coherent map that looks similar to the old Google Maps style from OSM data in a SpatiaLite database
preview=image/osm_spatialite_googlemaps.png, image/osm_spatialite_googlemaps_lines.png
qgis_minimum_version=2.0
qgis_maximum_version=2.99

[flowmap]
name=Flowmap
author=Anita Graser
email=anitagraser@gmx.at
tags=flows, arrows
description=The collection contains styles for flow maps
preview=preview/preview.png
qgis_minimum_version=2.0
qgis_maximum_version=2.99
```





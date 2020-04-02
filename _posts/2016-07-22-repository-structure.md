---
layout: page
title: "Repository structure"
category: author
date: 2016-07-22 17:04:29
order: 3
---

In order for the plugin to be able to read the repository correctly, the 
repository must have a specific structure. Generally the structure looks like
this:

    Repository root
    ├── README (encouraged)
    ├── metadata.ini (required)
    └── collections
        ├── [Collection1 register id] (the id string used in "collections" in metadata.ini)
        │   ├── image (optional, containing all kinds of image files)
        │   ├── models (optional, containing Processing models)
        │   ├── preview (encouraged, containing previews for the collection, referenced in metadata.ini)
        │   ├── processing (optional, containing Python Processing scripts)
        │   ├── rscripts (optional, containing R scripts)
        │   ├── style (optional, containing QML files - QGIS Layer style)
        │   ├── svg (optional, containing SVG files)
        │   ├── symbol (optional, containing symbol definition XML files)
        │   └── lisence file (encouraged)
        ├── [Collection2 register id] (the id string used in "collections" in metadata.ini)
        │   ├── image (optional, containing all kinds of image files)
        │   ├── models (optional, containing Processing models)
        │   ├── preview (encouraged, containing previews for the collection, referenced in metadata.ini)
        │   ├── processing (optional, containing Python Processing scripts)
        │   ├── rscripts (optional, containing R scripts)
        │   ├── style (optional, containing QML files - QGIS Layer style)
        │   ├── svg (optional, containing SVG files)
        │   ├── symbol (optional, containing symbol definition XML files)
        │   └── lisence file (encouraged)
        ├── ...
        └── [CollectionN register id] (the id string used in "collections" in metadata.ini)
            ├── image (optional, containing all kinds of image files)
            ├── models (optional, containing Processing models)
            ├── processing (optional, containing Python Processing scripts)
            ├── rscripts (optional, containing R scripts)
            ├── style (optional, containing QML files - QGIS Layer style)
            ├── svg (optional, containing SVG files)
            ├── symbol (optional, containing symbol definition XML files)
            └── lisence file (encouraged)
        
Check the
[QGIS Resources Repository](https://github.com/QGIS/QGIS-Resources) and
[this test repository](https://github.com/akbargumbira/qgis_resources_data/)
for github repository examples.

              
              
               
                

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

If the *QGIS Resource Sharing plugin* shall be able to make the
resources available to QGIS users in a convenient way, you have
to place them where the plugin expects them to be:

* Layer style (QML) files belong in the ***style*** directory.

* Processing models belong in the ***models*** directory.

* Processing (Python) scripts belong in the ***processing*** directory.

* R script (for use with the Processing R plugin) belong in in the
  ***rscripts*** directory.

* Symbol XML files belong in the ***symbol*** directory.
  Symbol images are expected to be in the ***image*** directory and
  symbol SVGs are expected to be in the ***svg*** directory.

* SVGs belong in the ***svg*** directory.

* Images belong in the ***image*** directory.

Check the
[QGIS Resources Repository](https://github.com/QGIS/QGIS-Resources) and
[this test repository](https://github.com/QGIS-Contribution/QGIS_Test-Resources)
for github repository examples.

              
              
               
                

---
layout: page
title: "Repository Structure"
category: doc
date: 2016-07-22 17:04:29
order: 3
---

In order for the plugin to be able to read the repository correctly, the 
repository must have a specific structure. Generally the structure looks like
 this:

```
* Repository root
    * Readme file (optional) - *file*
    * metadata.ini (required, fixed name) - *file*
    * collections (required, fixed name) - *directory*
        * [Collection Register Name] (The name registered in metadata) - *directory*
            * image (optional, fixed name) - *directory*
                * PNG, JPEG, other image files that can be used for raster fill
            * preview (optional, fixed name) - *directory*
                * Image files for your collection preview (could be screenshots of the map using the collection)  
            * processing (optional, fixed name) - *directory*
                * Python processing scripts
            * svg (optional, fixed name) - *directory*
                * SVG files that will be added into the QGIS SVG search path
            * symbol (optional, fixed name) - *directory*
                * The symbol XML files that will be installed in QGIS Style Manager
            * license file (encouraged) - *file*
```              


To see an example of a repository, check this github repository [Test Repository](https://github.com/akbargumbira/qgis_resources_data/)

              
              
               
                

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
        └── [Collection register name] (the name registered in metadata)
            ├── image (optional, containing all kinds of image files)
            ├── processing (optional, containing Python Processing scripts)
            ├── models (optional, containing Processing models)
            ├── rscripts (optional, containing R scripts)
            ├── svg (optional, containing SVG files)
            └── symbol (optional, containing symbol definition XML files)

To see an example of a repository, check this github repository [Test Repository](https://github.com/akbargumbira/qgis_resources_data/)

              
              
               
                

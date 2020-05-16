---
layout: page
title: "Installing a collection"
category: user
date: 2016-08-09 11:13:13
order: 2
---
Now that you have the **QGIS Resource Sharing** plugin installed,
you can browse available collections (from the repositories
registered in the ```Settings``` tab) and install them in your
file system, making them available to QGIS.

The first time you use the plugin, there will be no collections
in the ``All collections`` tab.
But once you have loaded the available repositories, the
officially approved collections should be there.
Loading the repositories is done by pushing the
``Reload Repositories`` button in the ``Settings`` tab.

It is a good idea to ***reload*** the repositories now and then,
so that your local copies are kept up-to-date.

To install a collection, you go to the ``All collections`` tab,
select it and click the ```Install``` button (below the collection
description).
The resources in the collection will be installed (the location
in the file system depends on their type).

**Note**: When you have installed a collection from a repository,
the complete *repository* will be duplicated in your local file
system (under ``resource_sharing/repositories`` in the QGIS
user directory). In addition, the *collection* will be added under
the *collections* directory (for instance,
``resource_sharing/collections``), with a, for most people,
unintelligible name (the *QGIS R script collection* from the
*QGIS Official Repository* is located in the
``resource_sharing/collections/8bc41c8c4fe90615b47eef7c81199fa6d7148fb3``
directory).
The collection folder will have sub-folders for the resources -
branches in the
<a href="../author/repository-structure.html">repository structure</a>.

#### SVG
If the collection contains SVGs, the path to the collections
folder will be included in your QGIS SVG search path.
The SVGs will be available when editing symbols (under the
``User Symbols`` section in **SVG Groups**).

![SVG Group]({{ site.baseurl }}/assets/svg_group.png)
  
#### Symbol
The symbols, colorramps, textformats (since version 0.14.0) and
labelsettings (since version 0.14.0) from the style XML files in the
collection will become available in the Style Manager. 

![Style Manager]({{ site.baseurl }}/assets/style_manager.png)

For each symbol XML file, the plugin will create a tag where the last
part of the name is the filename of the XML file (without the *.xml*).
The first part of the tag name identifies the collection.
Click on the tabs ```All```, ```Marker```, ```Line```, ```Fill```,
```Color Ramp```, ```Text Format``` or ```Label Settings```
to see the items installed from the collection.

#### Expression (since version 0.15.0)
The expressions defined in the collection's expression (JSON) files
are made available under *User expressions* in the expression
dialogue for QGIS versions 3.12 and higher.
The (JSON) file name is used as a prefix in the expression name.

#### Style
For QML styles, the plugin will resolve the image or SVG paths for you.
You can click on the ```Open folder``` button to see where in the file
system the QML style file is located, for later use.

#### Processing Script
The Python scripts will be copied to the processing scripts folder and
thereby become available for use in the Processing Toolbox under the
```Scripts``` menu.

![Processing Toolbox Scripts]({{ site.baseurl }}/assets/processing_toolbox_scipts.png)

#### Processing Model (since version 0.10.0)
The model fioles will be copied to the processing models folder and
become available for use in the Processing Toolbox under the
```Models``` menu.

![Processing Toolbox Models]({{ site.baseurl }}/assets/processing_toolbox_models.png)

#### R Script (since version 0.9.0)
The R scripts in the collection will be copied to the R scripts folder
and become available for use in the Processing Toolbox under the
```R``` menu.

![Processing Toolbox R]({{ site.baseurl }}/assets/processing_toolbox_r.png)

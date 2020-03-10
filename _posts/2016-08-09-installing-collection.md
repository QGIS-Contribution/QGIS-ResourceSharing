---
layout: page
title: "Installing a collection"
category: user
date: 2016-08-09 11:13:13
order: 2
---
Now that you have the **QGIS Resource Sharing** plugin installed,
you can browse available collections (from the repositories
registered in the ```Settings``` tab) and install them on your
local machine.

The first time you use the plugin, there will not be any
collections to be found in the ``All`` tab.
But once you have loaded the available repositories, the
officially approved collections should be there.
Loading the repositories is done by pushing the
``Reload Repositories`` button in the ``Settings`` tab.

It is a good idea to ***reload*** the repositories now and then,
so that your local copies are kept up-to-date.

To install a collection, you go to the ``All`` tab, select it
and click the ```Install``` button (below the collection
description).
The resources in the collection will be installed (the location
in the file system depends on their type).

.. note:: When you have installed a collection from a repository, the
   complete repository will be duplicated on your local file
   system (under ``resource_sharing/repositories`` in the QGIS
   user directory).

#### SVG
If the collection contains SVGs, they will be copied to your file
system, and the path will be included in your QGIS SVG search path.
The SVGs will be available when editing symbols (under the
``User Symbols`` section in **SVG Groups**).

![SVG Group]({{ site.baseurl }}/assets/svg_group.png)
  
#### Symbol
The symbols and colorramps from the collection (defined by an XML 
file) will become available in the Style Manager. 

![Style Manager]({{ site.baseurl }}/assets/style_manager.png)

For each symbol XML file, the plugin will create a child group with the same
name as the XML file.
Click on the tab ```Marker```, ```Line```, ```Fill```, or ```Color ramp```
to see the items installed from the collection.
 
#### Style
For QML styles, the plugin will resolve the image or SVG paths for you.
You can click on the ```Open folder``` button to see where the QML style
is, for later use.

#### Processing Script
After the installation, the processing scripts in the collection will be 
available for use in the Processing Toolbox under the ```Scripts``` menu.

![Processing Toolbox Scripts]({{ site.baseurl }}/assets/processing_toolbox_scipts.png)

#### Processing Model
After the installation, the processing models in the collection will be 
available for use in the Processing Toolbox under the ```Models``` menu.

![Processing Toolbox Models]({{ site.baseurl }}/assets/processing_toolbox_models.png)

#### R Script
After the installation, the R scripts in the collection will be available for use
in the Processing Toolbox under the ```R``` menu.

![Processing Toolbox R]({{ site.baseurl }}/assets/processing_toolbox_r.png)

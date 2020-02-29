---
layout: page
title: "Installing a collection"
category: user
date: 2016-08-09 11:13:13
order: 2
---
Now that you have the **QGIS Resource Sharing** plugin installed,
you can browse the available collections (from the repositories
registered in the ```Settings``` tab) and install them on your
local machine.
To install a collection, you select the collection you want to install
and click the ```Install``` button below the collection description.
The resources in the collection will be installed (the location
in the file system depends on their type).

#### SVG
If the collection contains SVGs, they will be added, and the path
will be included in your QGIS SVG search path.
The SVGs will be available when editing symbols (under the
``User Symbols`` section in **SVG Groups**).

![SVG Group]({{ site.baseurl }}/assets/svg_group.png)
  
#### Symbol
The symbols and colorramps from the collection (defined by the XML 
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

![Processing Toolbox]({{ site.baseurl }}/assets/processing_toolbox.png)

#### Processing Model
After the installation, the processing models in the collection will be 
available for use in the Processing Toolbox under the ```Models``` menu.

#### R Script
After the installation, the R scripts in the collection will be available for use
in the Processing Toolbox under the ```R``` menu.

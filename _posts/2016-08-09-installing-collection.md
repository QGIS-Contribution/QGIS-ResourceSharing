---
layout: page
title: "Installing Collection"
category: user
date: 2016-08-09 11:13:13
order: 2
---
Now that you have **QGIS Resource Sharing** plugin installed, you can browse 
the collections available from the repositories registered in the 
```Settings``` tab and install them on your local machine. To install a 
collection, you just simply need to click the collection you want to install 
and click ```Install``` button below the collection description. For each 
type of resources in the collection, the plugin will install them differently.

#### SVG
If the collection contains SVGs, it will be added to SVG search paths in your
 QGIS. You can directly use those SVGs when you want to edit a symbol to
  use one of the SVG from the collection. The SVGs should be available under 
  ```Resource Sharing``` section in **SVG Groups**

![SVG Group]({{ site.baseurl }}/assets/svg_group.png)
  
#### Symbol
The symbols and colorramps from the collection (defined by the XML 
file) will be installed in the Style Manager. 

![Style Manager]({{ site.baseurl }}/assets/style_manager.png)

For each symbol XML file, the plugin will create a child group with name equals
to the file name. Please click on the tab ```Marker```, ```Line```, 
```Fill```, or ```Color ramp``` to see the items installed from the collection.
 
#### Style
For QML style, the plugin will not do anything other than resolving the image
 or svg paths for you. You can click ```Open folder``` and see where the QML 
 style is for later use.
 

#### Processing Script
After the installation, the processing scripts in the collection will be 
available for use in the Processing Toolbox under ```Scripts``` menu.

![Processing Toolbox]({{ site.baseurl }}/assets/processing_toolbox.png)

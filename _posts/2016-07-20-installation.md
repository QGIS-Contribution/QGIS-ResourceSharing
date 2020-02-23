---
layout: page
title: "Installing the Plugin"
category: user 
date: 2016-07-20 17:03:00
order: 1
---

#### From the QGIS Plugin Manager

To install the plugin, you use **QGIS Plugin Manager**. In
QGIS, go to the ```Plugin``` menu and choose
```Manage and Install Plugins...```
Search for ```QGIS Resources Sharing```
 in the search box of the dialog in the ```All``` tab. Select the ```QGIS 
 Resources Sharing``` plugin and click ```Install```

![Search Plugin]({{ site.baseurl }}/assets/search_plugin.png)


#### From the repository 
If you are adventurous and would like to get the latest code of the plugin, 
you can install it directly from the repository.
The repository is on 
Github - [here](https://github.com/QGIS-Contribution/QGIS-ResourceSharing).
There are 2 ways to get the plugin:

* Download the zip from github: [ZIP Develop](https://github
.com/akbargumbira/qgis_resources_sharing/archive/develop.zip), extract the 
zip, and copy the extracted root directory into your local QGIS plugins directory 
(for QGIS3 on Linux: ```~/.local/share/QGIS/QGIS3/profiles/default/python/plugins```,
on Windows: ```C:\Users\{username}\AppData\Roaming\QGIS\QGIS3\profiles\default\\python\plugins```)
  
* Use git: clone the repository in the plugin directory, or clone in
 your preferred location and add a symbolic link in the local plugins directory.

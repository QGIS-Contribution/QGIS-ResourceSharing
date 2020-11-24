---
layout: page
title: "Installing the plugin"
category: user
date: 2016-07-20 17:03:00
order: 1
---

#### From the QGIS Plugin Manager

To install the plugin, you use **QGIS Plugin Manager**.

1. Go to the ```Plugin``` menu and choose
   ```Manage and Install Plugins...```
2. Search for ```QGIS Resource Sharing``` in the search box
   of the dialog in the ```All``` tab
3. Select the ```QGIS Resource Sharing``` plugin and click
   ```Install```

![Search Plugin]({{ site.baseurl }}/assets/search_plugin.png)

#### From the repository

If you are adventurous and would like to get the latest code of the
plugin, you can install it directly from the repository.
The repository is on Github -
[here](https://github.com/QGIS-Contribution/QGIS-ResourceSharing).
There are 2 ways to get the plugin:

* Download the zip from github:
  [ZIP Master](https://github.com/QGIS-Contribution/QGIS-ResourceSharing/archive/master.zip),
  extract the zip, and copy the extracted root directory into your
  local QGIS plugin directory
  (for QGIS3 on Linux:
  ```~/.local/share/QGIS/QGIS3/profiles/default/python/plugins```,
  on Windows:
  ```C:\Users\{username}\AppData\Roaming\QGIS\QGIS3\profiles\default\\python\plugins```)

* Use git to clone the repository in your plugin directory, or clone
  it somewhere else and add a symbolic link to it in your plugin
  directory.

#### Locating and starting the plugin in the QGIS GUI

The plugin has its own toolbar (*Resource Sharing*, with only one
action).
You can enable / disable the toolbar in *View-> Toolbars*, and move
it (drag and drop) to a convenient location in the GUI.
The plugin can also be started from the *Web* menu
(*Web-> Resource Sharing*) and a submenu of the *Plugins* menu
(*Plugins-> Resource Sharing -> Resource Sharing*).

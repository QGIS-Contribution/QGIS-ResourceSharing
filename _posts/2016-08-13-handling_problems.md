---
layout: page
title: "Handling problems"
category: user
date: 2016-08-13 17:11:10
order: 5
---

***Polluted SVG search path***

If the local collection directories have changed location in
the file system, the SVG search path may not have been updated,
and the old location will still be included in the search path.
Old locations can be removed from the search path by editing
*searchPathsForSVG* under ``svg`` in the QGIS settings
(*Settings-> Options-> Advanced*), or in the QGIS3.ini file
that is located under `QGIS` in the user QGIS folder.

***Strange tag names in Style Manager***

Earlier versions of the plugin used non-inutitive tag names
for grouping symbols, colormaps, labelsettings and textformats
in the Style Manager. This has been improved in later versions.

To clean up the "mess", right-click the strange tag names in
the right part of the Style Manager dialogue and *Remove*.

Reload the collections to get the style elements from the
collections back in the Style Manager.

***Empty tags in Style Manager***

Earlier versions may also have tag names that have no associated
elements.
In the Style Manager right-click on the "empty" tag and *Remove*.

***Collection directories are not removed***
If there are subdirectories in the collections directory
(``/.local/share/QGIS/QGIS3/profiles/default/resource_sharing/collections``
on Ubuntu,
``C:\Users\<user>\AppData\Roaming\QGIS\QGIS3\profiles\default\resource_sharing\collections``
on Windows)
that do not correspond to installed collections, you can safely
remove them.

***Repository directories are not removed***

If there are subdirectories in the repositories directory
(``/.local/share/QGIS/QGIS3/profiles/default/resource_sharing/repositories``
on Ubuntu,
``C:\Users\<user>\AppData\Roaming\QGIS\QGIS3\profiles\default\resource_sharing\repositories``
on Windows)
that do not correspond to officially approved QGIS repositories,
you can safely remove them.

***Starting with a clean sheet***

If everything has turned out to be a mess (might happen after
plugin upgrades that adds new "features"), and you would like
to remove all installed collections and clean up, you can:

* Remove the resource_sharing directory in your QGIS user
  folder
  (``/.local/share/QGIS/QGIS3/profiles/default/QGIS``
  on Ubuntu,
  ``C:\Users\<user>\AppData\Roaming\QGIS\QGIS3\profiles\default\QGIS``
  on Windows).
  That will remove the cache, the local copies/clones of the
  repositories and the local copies of the collections.
* Remove ``localCollectionDir`` under ``[ResourceSharing]`` in
  QGIS settings (*Settings-> Options-> Advanced*), or in
  the QGIS3.ini file that is located under QGIS in the user
  QGIS folder.
* Remove ``repository`` under ``[ResourceSharing]`` in
  QGIS settings (*Settings-> Options-> Advanced*), or in
  the QGIS3.ini file that is located under QGIS in the user
  QGIS folder).
* If you have used an early version (pre 0.10.0), you may also
  want to remove the ``~/QGIS/Resource Sharing`` directory.
* Remove all Resource Sharing related directories from the SVG
  search path by editing *searchPathsForSVG* under ``svg`` in
  QGIS settings (*Settings-> Options-> Advanced*), or in
  the QGIS3.ini file that is located under `QGIS` in the user
  QGIS folder.
* Reinstall the plugin

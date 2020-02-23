---
layout: page
title: "Release Workflow"
category: dev
date: 2016-09-04 19:32:12
order: 3
---

Follow these steps to release the plugin:

* Update ```metadata.txt``` changing the version and add updating the changelog
* The branch to release should be ```master```.
  If you want to release from the ```develop``` branch, please make a PR
  to the ```master``` branch first. 
* Run ```make release```. This will create a package, add a GitHub version release
  tag, and publish the plugin to ```plugin.qgis.org```.
* Voila, the new version of the plugin should be published!
  Please check if you can upgrade the plugin in QGIS without problems.
* Make a release on Github and highlight all the new features and fixes of
  the new version.

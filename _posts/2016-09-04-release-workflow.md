---
layout: page
title: "Release Workflow"
category: dev
date: 2016-09-04 19:32:12
order: 2
---

To release the plugin, please follow these steps:

* Update metadata.txt changing the version and add changelog
* The working branch to release should be ```master``` branch. If you want to
 release from the ```develop``` branch (in case that you don't have any new 
 features in develop that you want to release), please make a PR to 
 ```master``` branch first. 
* Run ```make release```. This will create a package, release tag version to 
github, and publish the plugin to ```plugin.qgis.org```.
* Voila, the new version of the plugin should be published! Please check in your QGIS if you can upgrade the plugin without problems.



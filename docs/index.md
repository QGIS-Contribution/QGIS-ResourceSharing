---
layout: default
title: "Home"
---

### The QGIS Resource Sharing Plugin

If you have ever wanted to share QGIS resources easily with your peers, this plugin comes to the rescue!

The QGIS Resource Sharing plugin allows QGIS users to share resources (symbols, layer styles, SVGs, images, expressions, processing models, processing scripts, Dataset QA checklists,  and R scripts) in repositories that other users can access.

A QGIS Resource Sharing repository could be a remote GIT repository (currently Github, Gitlab and Bitbucket public repositories are supported), local file system collections, or zipped collections on the Web.

![the plugin]({{ site.baseurl }}/assets/app.png)

![settings-repositories]({{ site.baseurl }}/assets/repositories.png)

Collections are stored locally. By default, they are placed under the user's QGIS directory.

Git based collections are downloaded using git *clone* and updated using git *pull*, meaning that the complete repository will be stored locally, and that you can use a git client to suggest changes, keep it updated
(pull)...

The plugin lets you update the repositories through the GUI (the *Reload repositories* button in *Settings*).

The plugin was initially implemented as a Google Summer of Code project in 2016 for QGIS under the OSGeo organization by Akbar Gumbira (student), Alessandro Pasotti (mentor), Anita Graser (mentor), and with the help of Richard Duivenvoorde, Tim Sutton, and others in the QGIS community.

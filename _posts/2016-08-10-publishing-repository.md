---
layout: page
title: "Publishing your repository"
category: author
date: 2016-08-10 14:18:42
order: 5
---
When everything is done, and you have published the repository somewhere,
you can add the repository from your QGIS.
You may wondering if you can have your repository included as a default
repository that will be shown to all QGIS users without them needing to
add manually the repository.
Well, yes, you can do that.
 
To offer your repository as a default repository, fork the
[QGIS official resource repository](https://github.com/qgis/QGIS-Resources),
update the
[```directory.csv```](https://github.com/qgis/QGIS-Resources/blob/master/directory.csv)
file and make a pull request to the upstream project.

If your offer is accepted, and the pull request merged, your repository
will be listed among the "approved" repositories and its collections will
be available to everyone through the *Resource Sharing* plugin the next
time they start QGIS.

---
layout: page
title: "Contributing"
category: dev
date: 2016-07-20 17:30:10
order: 1
---

You are welcome to make a patch on GitHub by issuing pull request
[here](https://github.com/QGIS-Contribution/QGIS-ResourceSharing).

Also, if you experience problems with the plugin, or have suggestions
for improvement, please add an issue there.

If contributing code, it would be nice if you check it with pep8
and make sure that the tests are not broken by running:

```
pep8 resource_sharing
nose2 -s test --with-coverage
```
 
This project uses git submodules for the test data.
To clone the project completely, do:

```
git clone git@github.com:akbargumbira/qgis_resources_sharing.git <the destination directory>
cd <the destination directory>
git submodule init
git submodule update
```

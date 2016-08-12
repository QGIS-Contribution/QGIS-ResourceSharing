---
layout: page
title: "Contributing"
category: dev
date: 2016-07-20 17:30:10
---

You are welcome to make a patch by issuing pull request on Github [here](https://github.com/akbargumbira/qgis_resources_sharing). If there is any 
concern or discussion needed, please make an issue there. Please make sure 
that pep8 and the tests are not broken by running:

```
pep8 resource_sharing
nose2 -s test --with-coverage
```
 
This project uses git submodule for the test data. To clone the project completely, do:

```
git clone git@github.com:akbargumbira/qgis_resources_sharing.git <the destination directory>
cd <the destination directory>
git submodule init
git submodule update
```

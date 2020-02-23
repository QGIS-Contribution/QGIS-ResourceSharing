---
layout: page
title: "Adding a repository"
category: user
date: 2016-08-11 23:11:10
order: 3
---

To add a repository and see all the collections available in that repository, 
go to the ```Settings``` tab, click ```Add```, and specify the name and the 
URL of the repository.
If authentication is needed to access the repository, add the
configuration.

![Add repository]({{ site.baseurl }}/assets/settings.png)

If the repository is successfully added, you can now browse the collections
available from that repository in the ```All``` tab and install them.

There are four kinds of repositories that you can add (see table below).

Type | URL Example | Description
--- | --- | ---
Github |  https://github.com/qgis/QGIS-Resources.git | Works only for Github public repositories
Bitbucket |  https://bitbucket.org/gisuser/qgis-style-repo-useful.git | Works only for Bitbucket public repositories
File system | file:///home/gisuser/dev/repositories/qgis_resources | Pointing to the repository root in your local file system 
HTTP(s) with zip collections | https://github.com/qgis/QGIS-Resources | Pointing to the base URL of the repository. The metadata should be available in this URL http(s)://[base_url]/metadata.ini. The collections should be in http(s)://[base_url]/collections/[collection_name]>.zip

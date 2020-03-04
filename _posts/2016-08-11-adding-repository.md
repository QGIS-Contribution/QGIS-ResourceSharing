---
layout: page
title: "Adding a repository"
category: user
date: 2016-08-11 23:11:10
order: 3
---

To add a repository and get access to the collections available in it,
go to the ```Settings``` tab, click ```Add```, and specify a name
for the repository (you are free to call it whatever you like) and its
URL.
If authentication is needed to access the repository, add the
configuration.

![Add repository]({{ site.baseurl }}/assets/settings.png)

If the repository is successfully added, you can now also see its
collections in the ```All``` tab and install them from there.

There are four kinds of repositories that you can add (see table below).

Type | URL Example | Description
--- | --- | ---
GitHub |  https://github.com/qgis/QGIS-Resources.git | Works only for GitHub public repositories
Bitbucket |  https://bitbucket.org/gisuser/qgis-style-repo-useful.git | Works only for Bitbucket public repositories
File system | file:///home/gisuser/dev/repositories/qgis_resources | Pointing to the repository root in your local file system 
HTTP(s) with zip collections | https://github.com/qgis/QGIS-Resources | Pointing to the base URL of the repository. Metadata must be available, with this URL: http(s)://[base_url]/metadata.ini. The collections should be in http(s)://[base_url]/collections/[collection_name].zip

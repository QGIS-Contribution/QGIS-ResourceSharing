---
layout: page
title: "Adding Repository"
category: user
date: 2016-08-11 23:11:10
order: 3
---

To add a repository and see all the collections available in that repository, 
please go to the ```Settings``` tab, click ```Add```, fill the name and the 
URL of the repository. If there is authentication configuration needed to access the 
repository, please add the configuration.

![Add repository]({{ site.baseurl }}/assets/settings.png)

If the repository is added successfully, you can now browse the collections 
available from that repository in ```All`` tab and install them.

There are 4 kinds of repository that you can add. See this table:

Type | URL Example | Description
--- | --- | ---
Github |  https://github.com/akbargumbira/qgis_resources_sharing.git | Works 
only for Github public repositories
Bitbucket |  https://bitbucket.org/akbargumbira/qgis-style-repo-dummy.git | Works 
only for Bitbucket public repositories
File system | file:///home/akbar/dev/repositories/qgis_resources | Pointing 
to the repository root in your local file system
HTTP(s) with zip collections | http://www.akbargumbira.com/qgis_resources | 
Pointing to the base URL of the repository. The metadata should be available 
in this URL http(s)://<base_url>/metadata.ini. The collections should be in http
(s)://<base_url>/collections/<collection_name>.zip

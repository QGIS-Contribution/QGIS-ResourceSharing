---
layout: page
title: "Plugin configuration"
category: user
date: 2016-08-12 17:11:10
order: 4
---

Local collections directory
---------------------------

The location of the local file system directory that contains the installed
collections is controlled in settings: ``localCollectionDir`` under ``Resource Sharing``.

For versions up to, and including 0.9.0, the default location is ``~/QGIS/Resource Sharing``.
And the location can not be changed.

Since version 0.10.0, the default location is  ``<QGIS Home>/resource_sharing/collections``,
and the user can specify an alternative location using the ``localCollectionDir`` setting
in QGIS.ini. If the alternative location does not exist in the file system, the plugin will
try to create it.
Changing the location in settings will not move the collections.

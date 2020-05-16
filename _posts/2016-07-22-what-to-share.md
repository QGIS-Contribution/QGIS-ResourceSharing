---
layout: page
title: "What to share?"
category: author
date: 2016-07-22 17:06:34
order: 2
---

A repository contains collections to be shared.
A collection is a set of resources that belong together.
Either because they can be used to create a coherent map design
or do a specific task, or because they form a natural group.
 
The items that supported by the QGIS Resource Sharing plugin are
(plugin version in parenthesis):

Item | Notes
--- | ---
Expressions (0.15) | JSON files with user expressions (QGIS 3.12 and later).
Images | SVG files or other image files that can be used as svg markers or raster fills. Can be referenced from symbols and styles.
Symbols | XML files that can contain marker, line and fill symbols and also colorramps, textformattings (0.14) and labelsettings (0.14).
Layer styles | QML files.
Processing scripts | Python processing scripts.
Models (0.10) | Models for the *Graphical modeler*.
R scripts (0.9) | *Processing R Provider* plugin **R scripts**.

Note that you can include other QGIS resources in the repository 
(composer templates, project files, ...) as well.
They will be available in the collection directory, but the
plugin will not do anything with them.

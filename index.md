---
layout: default
title: "Home"
---

### The QGIS Resource Sharing Plugin
If you have ever wanted to share QGIS resources easily with your peers, 
this plugin comes to the rescue!

The QGIS Resource Sharing plugin allows QGIS users to share resources
(symbols, layer styles, SVGs, images, expressions, processing models,
processing scripts, Dataset QA checklists,  and R scripts) in
repositories that other users can access.

A QGIS Resource Sharing repository could be a remote GIT repository
(currently Github, Gitlab and Bitbucket public repositories are
supported), local file system collections, or zipped collections on
the Web. 

![the plugin]({{ site.baseurl }}/assets/app.png)

![settings-repositories]({{ site.baseurl }}/assets/repositories.png)

Collections are stored locally. By default, they are placed under
the user's QGIS directory.
Git based collections are downloaded using git *clone* and updated using
git *pull*, meaning that the complete repository will be stored locally,
and that you can use a git client to suggest changes, keep it updated
(pull), ...
The plugin lets you update the repositories through the GUI (the
*Reload repositories* button in *Settings*).

The plugin was initially implemented as a Google Summer of Code project
in 2016 for QGIS under the OSGeo organization by Akbar Gumbira (student),
Alessandro Pasotti (mentor), Anita Graser (mentor), and with the help of
Richard Duivenvoorde, Tim Sutton, and others in the QGIS community.

**Changelog**

* 0.16.0
  * GUI improvements (#138, #139, #140, #141)
  * Add button for reloading the QGIS directory of approved resources (#145)
  * Fix bug in the handling of QGIS directory updates (#146)
  * Add support for checklists (#151) - @ricardogsilva
* 0.15.1
  * Fix incorrect handling of searchPathsForSVG setting (#135)
  * Handle XML parsing exceptions for QML files*0.15.0 - Support expressions (#130). Switch to Python pathlib.
* 0.14.1
  * Also support QGIS 3.4 (avoid install of style labelsettings and textformatting for v. < 3.10 - #127)
  * Try another way to avoid [WinError 5] on Microsoft Windows (#103)
* 0.14.0
  * Style import improvements (fix colorramp support, add support for label settings and text formats, clean up Style Manager tags) (#113, #114, #116, #118)
  * Change collection directory names from a hash to a more user friendly name (composition of the name of the collection and its repository) (#110)
  * Preserve the installed collections when renaming a repository (#121)
  *  Documentation updates (#105, #109, #113)
* 0.13.1
  * Fix #44 (files removed from repository are still being installed from cache)
* 0.13.0
  * GUI updates (#100)
  * Provide installation summary (#6)
  * Avoid (parent) tag with no members in QGIS 3 style documents (#101)
  * Fix reloading problems ([WinError 5]) with Microsoft Windows (#103)
  * Other minor issues (#104)
* 0.12.0 - Make font sizes OK on HiDPI systems (#3)
  * Disable editing and removal of "official" repositories in Settings (#93)
  * Avoid ResourceWarning when installing a collection (#95)
  * Stop using the collection name for naming directories (#99)
  * Fixed parsing metadata issue - byte decoding (#41)
  * Update dulwich to v0.19.15
  * Update of bootstrap to v4.4.1
  * Update jquery to v3.4.1
* 0.11.1
  * Reduce log level to avoid exception on missing name or URL in directory (#64)
* 0.11.0
  * Check for missing repository name and URL in directory (#64)
  * Correct link to documentation
* 0.10.0
  * Added support for Processing models (#42)
  * Make the plugin available from the web menu (#68)
  * Fixing log message levels (#71)
  * Add the action to the toolbar (#70)
  * Avoid breaking when collections with incompatible QGIS versions are encountered (#60)
  * Avoid [WinErr 32] (#80)
* 0.9.0
  * Added support for R scripts (#57)
* 0.8.0
  * Fix issue #59 (deleting repositories does not work)
* 0.7.0
  * Flip experimental flag
  * Merge PR from havatv (issue #60 - avoid breaking on incompatible versions)
* 0.6.0
  * Experimental version for QGIS 3
* 0.5.2
  * Add support for gitlab and gogs repositories (PR by Salvatore Larosa - gh username: slarosa)
* 0.5.1
  * Allow authors to add license details in the collection
  * Fixed problem in QGIS < 2.12 as a result of using the new QgsAuthManager
* * Change the behavior of updating and removing directory in settings (This fixed #34)
* * Use the new official QGIS resource repository (https://github.com/qgis/QGIS-Resources)
* 0.5.0
  * Wohooo first release!

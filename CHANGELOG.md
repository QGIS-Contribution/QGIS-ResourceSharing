# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## 1.1.0 - 2024-05-13

### Bugs fixes 🐛

* fix: CI fails because of broken Qt ppa by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/303>
* CI: fix minimum python version by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/306>

### Features and enhancements 🎉

* Do not use reserved keyword id as a function parameter by @ptitjano in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/326>
* refacto: use plugin title from metadata to name the logger by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/334>
* improve(ui): complete i18n and add some icons by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/335>

### Tooling 🔧

* tooling: bump dev dependencies and update git hooks by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/301>
* tooling: update VS Code configuration by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/302>
* ci: run tests against embedded requirements changes by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/315>
* ci: run tests against testing deps changes by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/318>
* docs: use new GitHub Pages workflow instead of gh-pages branch by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/320>

### Other Changes

* Update metadata.txt about tags by @Gustry in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/279>
* packaging: pin qgis-plugin-ci version by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/319>
* chore(deps): replace semver with packaging by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/333>
* update(packaging): set QGIS maximum version  by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/336>

### New Contributors

* @Gustry made their first contribution in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/279>
* @ptitjano made their first contribution in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/326>

## 1.1.0-beta1 - 2024-01-19

### Bugs fixes 🐛

* fix: CI fails because of broken Qt ppa by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/303>
* CI: fix minimum python version by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/306>

### Tooling 🔧

* tooling: bump dev dependencies and update git hooks by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/301>
* tooling: update VS Code configuration by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/302>
* ci: run tests against embedded requirements changes by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/315>
* ci: run tests against testing deps changes by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/318>

### Other Changes

* Update metadata.txt about tags by @Gustry in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/279>
* packaging: pin qgis-plugin-ci version by @Guts in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/319>

### New Contributors

* @Gustry made their first contribution in <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/pull/279>

## 1.0.0 - 2022-09-05

* Tests have been refactored to use GitHub Actions and restoring code coverage
* Handle case where one of default repositories is unreachable
* Minor bug fixes spotted during tests refactoring
* See 1.0.0-beta1 release notes for complete changes since the last stable version

## 1.0.0-beta1 - 2022-04-28

* Improved integration of external libraries (#166)
* Improved development environment (#168) - thanks to @Guts
* Enable translation for the plugin UI and add partial French translation
* Use GitHub Actions to build and embed external dependencies, to package and release the plugin
* Upgrade Bootstrap to 4.6.1
* Remove QGIS 2 / PyQt4 imports
* Clean up some really old-school code

## 0.16.0 - 2020-08-29

* GUI improvements (#138, #139, #140, #141)
* Add button for reloading the QGIS directory of approved resources (#145)
* Fix bug in the handling of QGIS directory updates (#146)
* Add support for checklists (#151) - @ricardogsilva

---

## 0.15.1 - 2020-05-16

* Fix incorrect handling of searchPathsForSVG setting (#135)
* Handle XML parsing exceptions for QML files\*0.15.0 - Support expressions (#130). Switch to Python pathlib.

---

## 0.14.1 - 2020-04-25

* Also support QGIS 3.4 (avoid install of style labelsettings and textformatting for v. < 3.10 - #127)
* Try another way to avoid [WinError 5] on Microsoft Windows (#103)

---

## 0.14.0 - 2020-04-23

* Style import improvements (fix colorramp support, add support for label settings and text formats, clean up Style Manager tags) (#113, #114, #116, #118)
* Change collection directory names from a hash to a more user friendly name (composition of the name of the collection and its repository) (#110)
* Preserve the installed collections when renaming a repository (#121)
* Documentation updates (#105, #109, #113)

---

## 0.13.1 - 2020-04-11

* Fix #44 (files removed from repository are still being installed from cache)

---

## 0.13.0 - 2020-04-10

* GUI updates (#100)
* Provide installation summary (#6)
* Avoid (parent) tag with no members in QGIS 3 style documents (#101)
* Fix reloading problems ([WinError 5]) with Microsoft Windows (#103)
* Other minor issues (#104)

---

## 0.12.0 - 2020-03-28

* Make font sizes OK on HiDPI systems (#3)
* Disable editing and removal of "official" repositories in Settings (#93)
* Avoid ResourceWarning when installing a collection (#95)
* Stop using the collection name for naming directories (#99)
* Fixed parsing metadata issue - byte decoding (#41)
* Update dulwich to v0.19.15
* Update of bootstrap to v4.4.1
* Update jquery to v3.4.1

---

## 0.11.1 - 2020-03-03

* Reduce log level to avoid exception on missing name or URL in directory (#64)

---

## 0.11.0 - 2020-02-29

* Check for missing repository name and URL in directory (#64)
* Correct link to documentation

---

## 0.10.0 - 2020-02-26

* Added support for Processing models (#42)
* Make the plugin available from the web menu (#68)
* Fixing log message levels (#71)
* Add the action to the toolbar (#70)
* Avoid breaking when collections with incompatible QGIS versions are encountered (#60)
* Avoid [WinErr 32] (#80)

---

## 0.9.0 - 2020-02-15

* Added support for R scripts (#57)

---

## 0.8.0 - 2020-02-10

* Fix issue #59 (deleting repositories does not work)

---

## 0.7.0 - 2020-02-07

* Flip experimental flag
* Merge PR from havatv (issue #60 - avoid breaking on incompatible versions)

---

## 0.6.0 - 2018-12-04

* Experimental version for QGIS 3

---

## 0.5.2 - 2017-11-05

* Add support for gitlab and gogs repositories (PR by Salvatore Larosa - gh username: slarosa)

---

## 0.5.1 - 2016-08-31

* Allow authors to add license details in the collection
* Fixed problem in QGIS < 2.12 as a result of using the new QgsAuthManager
* Change the behavior of updating and removing directory in settings (This fixed #34)
* Use the new official QGIS resource repository (<https://github.com/qgis/QGIS-Resources>)

---

## 0.5.0 - 2016-08-15

* Wohooo first release!

# Packaging and deployment

## Packaging

This plugin is using the [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci/) tool to perform packaging operations.  
The package command is performing a `git archive` run based on changelog.

```bash
# package a specific version (which must be already documented in the changelog)
qgis-plugin-ci package 1.3.1
# package latest version
qgis-plugin-ci package latest
```

## Release a version

Everything is done through the continuous deployment:

1. Add the new version to the `CHANGELOG.md`
1. Change the version number in `__about__.py`
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "This version rocks!"`
1. Push tag to main branch: `git push origin 0.3.0`

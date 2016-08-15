SHELL := /bin/bash

WORK_DIR = /tmp/qgis_resource_sharing
VERSION=`cat metadata.txt | grep ^version | sed 's/version=//g'`

clean:
	@-find . -name '*~' -exec rm {} \;
	@-find . -name '*.pyc' -exec rm {} \;
	@-find . -name '*.pyo' -exec rm {} \;
	@# Clean stray merge working files from git
	@-find . -name '*.orig' -exec rm {} \;

zip:
	@echo "Making zip package in the WORK_DIR"
	@mkdir -p $(WORK_DIR)
	@echo $(VERSION)
	@git archive `git branch | grep '\*'| sed 's/^\* //g'` | tar -x $(WORKDIR)

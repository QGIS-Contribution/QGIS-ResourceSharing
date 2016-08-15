SHELL := /bin/bash

PLUGIN = qgis_resource_sharing
WORK_DIR = /tmp/${PLUGIN}
OUTPUT=${WORK_DIR}/${PLUGIN}.zip

VERSION=`cat metadata.txt | grep ^version | sed 's/version=//g'`

release: zip release-tag
	@python plugin_upload.py ${OUTPUT}

zip:
	@echo "Making zip package in the WORK_DIR"
	@mkdir -p ${WORK_DIR}/${PLUGIN}
	@echo $(VERSION)
	@git archive `git branch | grep '\*'| sed 's/^\* //g'` | tar -x -C ${WORK_DIR}/${PLUGIN}
	@rm -rf ${WORK_DIR}/${PLUGIN}/.git*
	@rm -rf ${WORK_DIR}/${PLUGIN}/test
	@rm -rf ${WORK_DIR}/${PLUGIN}/scripts
	@rm -rf ${WORK_DIR}/${PLUGIN}/.travis.yml
	@rm -rf ${WORK_DIR}/${PLUGIN}/.coverage
	@rm -rf ${WORK_DIR}/${PLUGIN}/.coveragerc
	@rm -rf ${WORK_DIR}/${PLUGIN}/pylintrc
	@cd ${WORK_DIR} && zip -r ${OUTPUT} * --exclude \*.pyc
	@echo "Your plugin archive has been generated:"
	@ls -lah ${OUTPUT}
	@echo "${OUTPUT}"

release-tag:
	@echo "Version: " ${VERSION}
	@git tag v${VERSION} -m "Version ${VERSION}"
	@git push origin v${VERSION}

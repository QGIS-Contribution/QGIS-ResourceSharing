#!/usr/bin/env bash

# Run test in a local QGIS 3 testing docker

IMAGE=qgis/qgis
QGIS_VERSION_TAG=latest

PLUGIN_NAME="qgis_resource_sharing"

PATHH=$(dirname `readlink -f $0`)/..

xhost +

docker run -d --name qgis-testing-environment \
    -v ${PATHH}:/tests_directory \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e WITH_PYTHON_PEP=false \
    -e ON_TRAVIS=false \
    -e MUTE_LOGS=true \
    -e CI=true \
    -e NO_MODALS=1 \
    -e DISPLAY=${DISPLAY} \
    ${IMAGE}:${QGIS_VERSION_TAG}


sleep 10


# Install deps
docker exec -it qgis-testing-environment sh -c "qgis_setup.sh $PLUGIN_NAME"


#docker exec -it qgis-testing-environment sh -c "qgis"
echo "Test Result: " $?

# Run the real test

time docker exec -it qgis-testing-environment sh -c "cd /tests_directory && qgis_testrunner.sh test_suite.test_qgis3"


# Comment in case you wanted to debug the containers
docker kill qgis-testing-environment
docker rm qgis-testing-environment

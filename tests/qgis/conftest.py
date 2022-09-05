import pytest


@pytest.fixture(autouse=True)
def setup(qgis_app):
    qgis_app.initQgis()


@pytest.fixture(autouse=True)
def teardown(qgis_app):
    qgis_app.exit()

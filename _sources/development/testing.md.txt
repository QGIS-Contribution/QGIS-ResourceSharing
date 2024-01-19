# Tests

Tests are written in 2 separate folders:

- `tests/unit`: testing code which is independent of QGIS API
- `tests/qgis`: testing code which depends on QGIS API

## Requirements

- QGIS {{ qgis_version_min }}+

```bash
python -m pip install -U pip
python -m pip install -U -r requirements/testing.txt
```

## Running tests

```bash
# run all tests with PyTest and Coverage report
python -m pytest

# run only unit tests
python -m pytest tests/unit

# run only QGIS tests
python -m pytest tests/qgis

# run a specific test module using standard unittest
python -m unittest tests.unit.test_plg_metadata

# run a specific test function using standard unittest
python -m unittest tests.unit.test_plg_metadata.TestPluginMetadata.test_version_semver
```

### Using Docker

Build the image:

```bash
docker build --pull --rm -f "tests/tests_qgis.dockerfile" -t qgis_lts:plugin_tester .
```

Run tests:

```bash
docker run -v "$(pwd):/tmp/plugin" qgis_lts:plugin_tester python3 -m pytest
```

Please note that will use the root rights on some folders.

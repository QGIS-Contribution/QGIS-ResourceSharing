#! python3  # noqa E265

"""
    Test repository base handler.

    From unittest: `python -m unittest tests.qgis.test_handler_base`
"""

# PyQGIS
from qgis.testing import start_app, unittest

# Plugin
from qgis_resource_sharing.repository_handler import (
    BaseRepositoryHandler,
    FileSystemHandler,
)

# Tests suite
from tests.qgis.base import BaseTestPlugin


class TestBaseHandler(BaseTestPlugin):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.base_handler = BaseRepositoryHandler(self.get_sample_repository_url())
        self.fs_handler = FileSystemHandler(self.get_sample_repository_url())

    def test_get_handler(self):
        handler = self.base_handler.get_handler(self.get_sample_repository_url())
        self.assertEqual(handler.__class__.__name__, "FileSystemHandler")

    def test_is_git_repository(self):
        self.assertEqual(self.fs_handler.is_git_repository, False)

    def test_parse_metadata(self):
        """Testing parsing the metadata."""
        # check if repository metadata can be fetched
        result, _ = self.fs_handler.fetch_metadata()
        self.assertTrue(result)

        # parse repository metadata
        collections = self.fs_handler.parse_metadata()

        # it should be only 1 collection defined there
        self.assertEqual(len(collections), 1)

        test_collection = collections[0]

        # check some values
        self.assertIsInstance(test_collection, dict)
        self.assertEqual(len(test_collection.keys()), 14)
        self.assertIsInstance(test_collection.get("author"), str)
        self.assertIsInstance(test_collection.get("license_url"), str)
        self.assertIsInstance(test_collection.get("preview"), list)
        self.assertEqual(len(test_collection.get("preview")), 2)
        self.assertIsInstance(test_collection.get("status"), int)

        # compare collection
        expected_collection = {
            "author": "Akbar Gumbira",
            "author_email": "akbargumbira@gmail.com",
            "description": "The collection contains various resources for testing",
            "license": "GNU GPL",
            "license_url": f"{self.get_sample_repository_url()}/collections/test_collection/LICENSE.txt",
            "name": "Akbar's Test Collection",
            "preview": [
                f"{self.get_sample_repository_url()}/collections/test_collection/preview/prev_1.png",
                f"{self.get_sample_repository_url()}/collections/test_collection/preview/prev_2.png",
            ],
            "qgis_max_version": "3.99",
            "qgis_min_version": "3.10",
            "register_name": "test_collection",
            "repository_name": "",
            "repository_url": self.get_sample_repository_url(),
            "status": 0,
            "tags": "test, symbol, svg, processing",
        }
        self.assertDictEqual(test_collection, expected_collection)


if __name__ == "__main__":
    unittest.main()

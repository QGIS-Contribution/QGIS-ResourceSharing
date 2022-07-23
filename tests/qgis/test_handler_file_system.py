#! python3  # noqa E265

"""
    Test repository file system handler.

    From unittest: `python -m unittest tests.qgis.test_handler_file_system`
"""

# PyQGIS
from qgis.testing import start_app, unittest

# Plugin
from qgis_resource_sharing.repository_handler import FileSystemHandler

# Tests suite
from tests.qgis.base import BaseTestPlugin


class TestFileSystemHandler(BaseTestPlugin):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.fs_handler = FileSystemHandler(self.get_sample_repository_url())

    def test_can_handle(self):
        """Test can_handle function."""
        url = "file:///home/akbar/dev"
        self.fs_handler.url = url
        self.assertTrue(self.fs_handler.can_handle())

        url = "http:///home/akbar/dev"
        self.fs_handler.url = url
        self.assertFalse(self.fs_handler.can_handle())

    def test_fetch_metadata(self):
        """Test fetch_metadata function."""
        # TC1: Normal successful testcase
        self.assertIsNone(self.fs_handler.metadata)
        status, _ = self.fs_handler.fetch_metadata()
        self.assertTrue(status)
        self.assertIsNotNone(self.fs_handler.metadata)
        metadata_path = self.get_fixtures_path("repository_dummy/metadata.ini")

        with open(metadata_path, "r") as metadata_file:
            expected_content = metadata_file.read()

        self.assertEqual(self.fs_handler.metadata, expected_content)


if __name__ == "__main__":
    unittest.main()

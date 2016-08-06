# coding=utf-8
from qgis.testing import start_app, unittest
import nose2

from PyQt4.QtCore import QUrl
from resource_sharing.resource_handler.symbol_resolver_mixin import (
    resolve_path
)
from test.utilities import test_data_path


class TestSymbolResolverMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def test_resolve_path(self):
        """Test resolving the path works correctly."""
        collection_path = test_data_path('collections', 'test_collection')
        search_paths = []

        # Test case 1: local path
        img_path = test_data_path(
            'collections', 'test_collection', 'svg', 'blastoise.svg')
        fixed_path = resolve_path(img_path, collection_path, search_paths)
        self.assertEqual(img_path, fixed_path)

        # Test case 2: local url
        img_path = test_data_path(
            'collections', 'test_collection', 'svg', 'blastoise.svg')
        img_url = QUrl.fromLocalFile(img_path)
        fixed_path = resolve_path(
            img_url.toString(), collection_path, search_paths)
        self.assertEqual(fixed_path, img_path)

        # Test case 3:  http url
        img_path = 'http://qgis.org/test/image.svg'
        img_url = QUrl.fromLocalFile(img_path)
        fixed_path = resolve_path(
            img_url.toString(), collection_path, search_paths)
        self.assertEqual(fixed_path, img_path)

        # Test case 4: checking in the svg local collection path
        img_path = '/you/would/not/find/this/charizard.svg'
        fixed_path = resolve_path(img_path, collection_path, search_paths)
        expected_path = test_data_path(
            'collections', 'test_collection', 'svg', 'charizard.svg')
        self.assertEqual(fixed_path, expected_path)

        # Test case 5: checking in the image local collection path
        img_path = '/you/would/not/find/this/pikachu.png'
        fixed_path = resolve_path(img_path, collection_path, search_paths)
        expected_path = test_data_path(
            'collections', 'test_collection', 'image', 'pikachu.png')
        self.assertEqual(fixed_path, expected_path)

        # Test case 6: checking in the search paths
        search_paths = [
            test_data_path(
                'collections', 'test_collection', 'preview')
        ]
        img_path = 'prev_1.png'
        fixed_path = resolve_path(img_path, collection_path, search_paths)
        expected_path = test_data_path(
            'collections', 'test_collection', 'preview', 'prev_1.png')
        self.assertEqual(fixed_path, expected_path)


if __name__ == "__main__":
    nose2.main()

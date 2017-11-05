# coding=utf-8
import unittest

from resource_sharing.collection_manager import CollectionManager


class TestCollections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_get_collection_id(self):
        """Testing get_collection_id."""
        collections_manager = CollectionManager()
        collection_name = 'Westeros Map'
        repository_url = 'https://github.com/john.doe/my_map'
        collection_id = collections_manager.get_collection_id(
            collection_name, repository_url)
        expected_id = '01ece258a505a060830bcecce29f16333f706538'
        self.assertEqual(collection_id, expected_id)


if __name__ == '__main__':
    unittest.main()

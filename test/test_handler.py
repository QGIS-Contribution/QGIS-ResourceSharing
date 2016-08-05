# coding=utf-8
from qgis.testing import start_app, unittest
import nose2

from resource_sharing.repository_handler import (
    BaseRepositoryHandler,
    FileSystemHandler,
    GithubHandler,
    BitBucketHandler)
from utilities import test_repository_url


class TestBaseHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.base_handler = BaseRepositoryHandler(test_repository_url())
        self.fs_handler = FileSystemHandler(test_repository_url())

    def test_get_handler(self):
        handler = self.base_handler.get_handler(test_repository_url())
        self.assertTrue(isinstance(handler, FileSystemHandler))

    def test_is_git_repository(self):
        self.assertEqual(self.fs_handler.is_git_repository, False)

    def test_parse_metadata(self):
        """Testing parsing the metadata."""
        self.fs_handler.fetch_metadata()
        collections = self.fs_handler.parse_metadata()
        # There's only 1 collection defined there
        self.assertEqual(len(collections), 1)
        expected_collection = {
            'status': 0,
            'description':
                u'The collection contains various resources for testing',
            'tags': u'test, symbol, svg, processing',
            'register_name': u'test_collection',
            'repository_url': u'file:///home/akbar/dev/python/qgis_resources_sharing/test/data',
            'name': u"Akbar's Test Collection",
            'author': u'Akbar Gumbira',
            'author_email': u'akbargumbira@gmail.com',
            'qgis_min_version': u'2.0',
            'qgis_max_version': u'2.99',
            'preview': [
                u'file:///home/akbar/dev/python/qgis_resources_sharing/test/data/collections/test_collection/prev_1.png',
                u'file:///home/akbar/dev/python/qgis_resources_sharing/test/data/collections/test_collection/prev_2.png'
            ]
        }
        self.assertDictEqual(collections[0], expected_collection)


class TestRepositoryHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.valid_github_https = 'https://github.com/anitagraser/QGIS-style-repo-dummy.git'
        self.valid_bitbucket_https = 'https://akbargumbira@bitbucket.org/akbargumbira/qgis-style-repo-dummy.git'

    def test_set_url(self):
        """Testing setting url of a remote repository"""
        # Test Github
        remote_repo = GithubHandler(self.valid_github_https)
        expected_host = 'github.com'
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = 'anitagraser'
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = 'QGIS-style-repo-dummy'
        self.assertEqual(remote_repo.git_repository, expected_repository)

        # Test Bitbucket
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_host = 'bitbucket.org'
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = 'akbargumbira'
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = 'qgis-style-repo-dummy'
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_get_metadata_url(self):
        """Testing metadata url is set correctly."""
        # Github Repo
        remote_repo = GithubHandler(self.valid_github_https)
        expected_metadata_url = 'https://raw.githubusercontent.com/anitagraser/QGIS-style-repo-dummy/master/metadata.ini'
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

        # Bitbucket Repo
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_metadata_url = 'https://bitbucket.org/akbargumbira/qgis-style-repo-dummy/raw/master/metadata.ini'
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

if __name__ == '__main__':
    nose2.main()

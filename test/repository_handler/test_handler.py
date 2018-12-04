# coding=utf-8
from qgis.testing import start_app, unittest

from resource_sharing.repository_handler import (
    BaseRepositoryHandler,
    FileSystemHandler,
    GithubHandler,
    BitBucketHandler,
    GogsHandler)

try:
    from ..utilities import test_data_path, test_repository_url
except SystemError:
    from test.utilities import test_data_path, test_repository_url



class TestBaseHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.base_handler = BaseRepositoryHandler(test_repository_url())
        self.fs_handler = FileSystemHandler(test_repository_url())

    def test_get_handler(self):
        handler = self.base_handler.get_handler(test_repository_url())
        self.assertEqual(handler.__class__.__name__, 'FileSystemHandler')

    def test_is_git_repository(self):
        self.assertEqual(self.fs_handler.is_git_repository, False)

    def test_parse_metadata(self):
        """Testing parsing the metadata."""
        result, _ = self.fs_handler.fetch_metadata()
        self.assertTrue(result)
        collections = self.fs_handler.parse_metadata()
        # There's only 1 collection defined there
        self.assertEqual(len(collections), 1)

        expected_collection = {
            'status': 0,
            'description':
                u'The collection contains various resources for testing',
            'tags': u'test, symbol, svg, processing',
            'register_name': u'test_collection',
            'repository_url': test_repository_url(),
            'name': u"Akbar's Test Collection",
            'author': u'Akbar Gumbira',
            'author_email': u'akbargumbira@gmail.com',
            'qgis_min_version': u'2.0',
            'qgis_max_version': u'3.99',
            'license': 'GNU GPL',
            'license_url': '%s/collections/test_collection/LICENSE.txt' %test_repository_url(),
            'preview': [
                '%s/collections/test_collection/preview/prev_1.png' % test_repository_url(),
                '%s/collections/test_collection/preview/prev_2.png' % test_repository_url()
            ]
        }
        self.assertDictEqual(collections[0], expected_collection)


class TestFileSystemHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.fs_handler = FileSystemHandler(test_repository_url())

    def test_can_handle(self):
        """Test can_handle function."""
        url = 'file:///home/akbar/dev'
        self.fs_handler.url = url
        self.assertTrue(self.fs_handler.can_handle())

        url = 'http:///home/akbar/dev'
        self.fs_handler.url = url
        self.assertFalse(self.fs_handler.can_handle())

    def test_fetch_metadata(self):
        """Test fetch_metadata function."""
        # TC1: Normal successful testcase
        self.assertIsNone(self.fs_handler.metadata)
        status, _ = self.fs_handler.fetch_metadata()
        self.assertTrue(status)
        self.assertIsNotNone(self.fs_handler.metadata)
        metadata_path = test_data_path('metadata.ini')
        with open(metadata_path, 'r') as metadata_file:
            expected_content = metadata_file.read()
        self.assertEqual(self.fs_handler.metadata, expected_content)


class TestRemoteGitHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.valid_github_https = 'https://github.com/anitagraser/QGIS-style-repo-dummy.git'
        self.valid_bitbucket_https = 'https://akbargumbira@bitbucket.org/akbargumbira/qgis-style-repo-dummy.git'
        self.valid_gitosgeo_https = 'https://git.osgeo.org/gogs/qgisitalia/QGIS-Italia-Risorse.git'

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

        # Test git.osgeo.org/gogs
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_platform = 'gogs'
        self.assertEqual(remote_repo.git_platform, expected_platform)
        expected_host = 'git.osgeo.org/gogs'
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = 'qgisitalia'
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = 'QGIS-Italia-Risorse'
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

        # GitOsgeo.org Repo
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_metadata_url = 'https://git.osgeo.org/gogs/qgisitalia/QGIS-Italia-Risorse/raw/master/metadata.ini'
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

if __name__ == '__main__':
    unittest.main()

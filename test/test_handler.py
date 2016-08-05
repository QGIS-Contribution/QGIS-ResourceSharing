# coding=utf-8
from qgis.testing import start_app, unittest
import nose2

from resource_sharing.repository_handler import (
    BaseRepositoryHandler,
    GithubHandler,
    BitBucketHandler)
from utilities import test_data_path


class TestBaseHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def test_parse_metadata(self):
        """Testing parsing the metadata."""
        url
        handler = BaseRepositoryHandler()


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

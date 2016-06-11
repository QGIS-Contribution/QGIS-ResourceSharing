# coding=utf-8
import unittest

from symbology_sharing.remote_repository import RemoteRepository


class TestRemoteRepository(unittest.TestCase):
    def setUp(self):
        self.valid_https = 'https://github.com/anitagraser/QGIS-style-repo-dummy.git'

    def test_set_url(self):
        """Testing setting url of a remote repository"""
        remote_repo = RemoteRepository(self.valid_https)

        expected_host = 'github.com'
        self.assertEqual(remote_repo.git_host, expected_host)

        expected_owner = 'anitagraser'
        self.assertEqual(remote_repo.git_owner, expected_owner)

        expected_repository = 'QGIS-style-repo-dummy'
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_get_metadata_url(self):
        """Testing metadata url is set correctly."""
        remote_repo = RemoteRepository(self.valid_https)

        expected_metadata_url = 'https://raw.githubusercontent.com/anitagraser/QGIS-style-repo-dummy/master/metadata.ini'
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

#! python3  # noqa E265

"""
Test repository handler for Git remote.

From unittest: `python -m unittest tests.qgis.test_handler_remote_git`
"""

# PyQGIS
from qgis.testing import unittest

from qgis_resource_sharing.repository_handler import (
    BitBucketHandler,
    GithubHandler,
    GogsHandler,
)


class TestRemoteGitHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.valid_github_https = (
            "https://github.com/anitagraser/QGIS-style-repo-dummy.git"
        )
        self.valid_bitbucket_https = (
            "https://akbargumbira@bitbucket.org/akbargumbira/qgis-style-repo-dummy.git"
        )
        self.valid_gitosgeo_https = (
            "https://git.osgeo.org/gitea/qgisitalia/QGIS-Italia-Risorse.git"
        )

    def test_set_url_github(self):
        """Testing setting url of a GitHub remote repository"""
        # Test Github
        remote_repo = GithubHandler(self.valid_github_https)
        expected_host = "github.com"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = "anitagraser"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "QGIS-style-repo-dummy"
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_set_url_bitbucket(self):
        """Testing setting url of a Bitbucket remote repository"""
        # Test Bitbucket
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_host = "bitbucket.org"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = "akbargumbira"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "qgis-style-repo-dummy"
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_set_url_osgeo(self):
        """Testing setting url of a remote repository hosted on git.osgeo.org"""
        # Test git.osgeo.org/gitea
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_platform = "gogs"
        self.assertEqual(remote_repo.git_platform, expected_platform)
        expected_host = "git.osgeo.org"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_service = "gitea"
        self.assertEqual(remote_repo.git_service, expected_service)
        expected_owner = "qgisitalia"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "QGIS-Italia-Risorse"
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_get_metadata_url_github(self):
        """Testing metadata url is set correctly."""
        # Github Repo
        remote_repo = GithubHandler(self.valid_github_https)
        expected_metadata_url = "https://raw.githubusercontent.com/anitagraser/QGIS-style-repo-dummy/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

    def test_get_metadata_url_bitbucket(self):
        """Testing metadata url is set correctly."""
        # Bitbucket Repo
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_metadata_url = "https://bitbucket.org/akbargumbira/qgis-style-repo-dummy/raw/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

    def test_get_metadata_url_osgeo(self):
        """Testing metadata url is set correctly."""
        # GitOsgeo.org Repo
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_metadata_url = "https://git.osgeo.org/gitea/qgisitalia/QGIS-Italia-Risorse/raw/branch/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)


if __name__ == "__main__":
    unittest.main()

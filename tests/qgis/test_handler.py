from qgis.testing import start_app, unittest

from qgis_resource_sharing.repository_handler import (
    BitBucketHandler,
    GithubHandler,
    GogsHandler,
)


class TestRemoteGitHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def setUp(self):
        self.valid_github_https = (
            "https://github.com/anitagraser/QGIS-style-repo-dummy.git"
        )
        self.valid_bitbucket_https = (
            "https://akbargumbira@bitbucket.org/akbargumbira/qgis-style-repo-dummy.git"
        )
        self.valid_gitosgeo_https = (
            "https://git.osgeo.org/gogs/qgisitalia/QGIS-Italia-Risorse.git"
        )

    def test_set_url(self):
        """Testing setting url of a remote repository"""
        # Test Github
        remote_repo = GithubHandler(self.valid_github_https)
        expected_host = "github.com"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = "anitagraser"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "QGIS-style-repo-dummy"
        self.assertEqual(remote_repo.git_repository, expected_repository)

        # Test Bitbucket
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_host = "bitbucket.org"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = "akbargumbira"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "qgis-style-repo-dummy"
        self.assertEqual(remote_repo.git_repository, expected_repository)

        # Test git.osgeo.org/gogs
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_platform = "gogs"
        self.assertEqual(remote_repo.git_platform, expected_platform)
        expected_host = "git.osgeo.org/gogs"
        self.assertEqual(remote_repo.git_host, expected_host)
        expected_owner = "qgisitalia"
        self.assertEqual(remote_repo.git_owner, expected_owner)
        expected_repository = "QGIS-Italia-Risorse"
        self.assertEqual(remote_repo.git_repository, expected_repository)

    def test_get_metadata_url(self):
        """Testing metadata url is set correctly."""
        # Github Repo
        remote_repo = GithubHandler(self.valid_github_https)
        expected_metadata_url = "https://raw.githubusercontent.com/anitagraser/QGIS-style-repo-dummy/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

        # Bitbucket Repo
        remote_repo = BitBucketHandler(self.valid_bitbucket_https)
        expected_metadata_url = "https://bitbucket.org/akbargumbira/qgis-style-repo-dummy/raw/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)

        # GitOsgeo.org Repo
        remote_repo = GogsHandler(self.valid_gitosgeo_https)
        expected_metadata_url = "https://git.osgeo.org/gogs/qgisitalia/QGIS-Italia-Risorse/raw/master/metadata.ini"
        self.assertEqual(remote_repo.metadata_url, expected_metadata_url)


if __name__ == "__main__":
    unittest.main()

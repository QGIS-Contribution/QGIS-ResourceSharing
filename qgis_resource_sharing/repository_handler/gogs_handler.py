#! python3  # noqa E265

# standard library
from urllib.parse import ParseResult, urlparse

# Plugin
from qgis_resource_sharing.repository_handler.remote_git_handler import RemoteGitHandler


class GogsHandler(RemoteGitHandler):
    """Handler class for Gogs Repository."""

    IS_DISABLED = False

    def __init__(self, url):
        RemoteGitHandler.__init__(self, url)
        self.url = url

    @property
    def url_parsed(self) -> ParseResult:
        return urlparse(self.url)

    @property
    def git_host(self):
        return "git.osgeo.org"

    @property
    def git_owner(self):
        return self.url_parsed.path.split("/")[2]

    @property
    def git_platform(self):
        return "gogs"

    @property
    def git_service(self):
        return "gitea"

    def can_handle(self):
        if self.git_platform == "gogs":
            return True
        return False

    def file_url(self, relative_path):
        return f"https://{self.git_host}/{self.git_service}/{self.git_owner}/{self.git_repository}/raw/branch/master/{relative_path}"

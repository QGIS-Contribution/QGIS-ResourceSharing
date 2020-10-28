from resource_sharing.repository_handler.remote_git_handler import RemoteGitHandler


class GogsHandler(RemoteGitHandler):
    """Handler class for Gogs Repository."""

    IS_DISABLED = False

    def __init__(self, url):
        RemoteGitHandler.__init__(self, url)

    def can_handle(self):
        if self.git_platform == "gogs":
            return True
        return False

    def file_url(self, relative_path):
        return "https://%s/%s/%s/raw/master/%s" % (
            self.git_host,
            self.git_owner,
            self.git_repository,
            relative_path,
        )

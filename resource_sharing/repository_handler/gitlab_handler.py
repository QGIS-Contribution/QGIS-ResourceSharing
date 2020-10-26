from resource_sharing.repository_handler.remote_git_handler import RemoteGitHandler


class GitlabHandler(RemoteGitHandler):
    """Handler class for Gitlab Repository."""

    IS_DISABLED = False

    def __init__(self, url):
        RemoteGitHandler.__init__(self, url)

    def can_handle(self):
        if self.git_platform == "gitlab":
            return True
        return False

    def file_url(self, relative_path):
        return "https://gitlab.com/%s/%s/raw/master/%s" % (
            self.git_owner,
            self.git_repository,
            relative_path,
        )

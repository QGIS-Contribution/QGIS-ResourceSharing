# coding=utf-8
from remote_git_handler import RemoteGitHandler


class GithubHandler(RemoteGitHandler):
    """Handler class for Github Repository."""
    IS_DISABLED = False

    def __init__(self, url=None):
        RemoteGitHandler.__init__(self, url)

    def can_handle(self):
        if self.git_platform == 'github':
            return True
        return False

    @property
    def metadata_url(self):
        return 'https://raw.githubusercontent.com/%s/%s/master/%s' % (
            self.git_owner,
            self.git_repository,
            self.METADATA_FILE)

# coding=utf-8
from base import BaseRepositoryHandler


class GithubHandler(BaseRepositoryHandler):
    """Handler class for Github Repository."""
    def __init__(self, url=None):
        BaseRepositoryHandler.__init__(self, url)

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

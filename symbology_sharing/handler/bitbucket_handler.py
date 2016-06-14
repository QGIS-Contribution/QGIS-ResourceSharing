# coding=utf-8
from base import BaseRepositoryHandler


class BitBucketHandler(BaseRepositoryHandler):
    """Handler class for Bitbucket Repository."""
    def __init__(self, url=None):
        BaseRepositoryHandler.__init__(self, url)

    def can_handle(self):
        if self.git_platform == 'bitbucket':
            return True
        return False

    @property
    def metadata_url(self):
        return 'https://bitbucket.org/%s/%s/raw/master/%s' % (
            self.git_owner,
            self.git_repository,
            self.METADATA_FILE)

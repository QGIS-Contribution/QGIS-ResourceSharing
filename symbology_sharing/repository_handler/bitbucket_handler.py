# coding=utf-8
from symbology_sharing.repository_handler.remote_git_handler import (
    RemoteGitHandler)


class BitBucketHandler(RemoteGitHandler):
    """Handler class for Bitbucket Repository."""
    IS_DISABLED = False

    def __init__(self, url=None):
        RemoteGitHandler.__init__(self, url)

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

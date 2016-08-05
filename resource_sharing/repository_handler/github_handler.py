# coding=utf-8
from resource_sharing.repository_handler.remote_git_handler import (
    RemoteGitHandler)


class GithubHandler(RemoteGitHandler):
    """Handler class for Github Repository."""
    IS_DISABLED = False

    def __init__(self, url):
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

    def preview_url(self, collection_name, file_path):
        return 'https://raw.githubusercontent.com/%s/%s/master/collections/%s/%s' % (
            self.git_owner,
            self.git_repository,
            collection_name,
            file_path)

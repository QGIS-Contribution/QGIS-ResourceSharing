# coding=utf-8
import os
from contextlib import closing

from qgis.core import QgsApplication

from ext_libs.giturlparse import parse, validate
from ext_libs.dulwich import porcelain
from symbology_sharing.handler.base import BaseHandler
from symbology_sharing.network_manager import NetworkManager


class RemoteGitHandler(BaseHandler):
    """Class to handle generic git remote repository."""
    IS_DISABLED = True

    def __init__(self, url=None):
        """Constructor."""
        BaseHandler.__init__(self, url)
        self._git_platform = None
        self._git_host = None
        self._git_owner = None
        self._git_repository = None

        # Call proper setters here
        self.url = url

    def can_handle(self):
        return False

    @BaseHandler.url.setter
    def url(self, url):
        """Setter to the repository's URL."""
        if validate(url):
            self._url = url
            git_parse = parse(url)
            self._git_platform = git_parse.platform
            self._git_host = git_parse.host
            self._git_owner = git_parse.owner
            self._git_repository = git_parse.repo

    @property
    def git_platform(self):
        return self._git_platform

    @property
    def git_host(self):
        return self._git_host

    @property
    def git_owner(self):
        return self._git_owner

    @property
    def git_repository(self):
        return self._git_repository

    def fetch_metadata(self):
        """Fetch metadata file from the repository."""
        # Fetch the metadata
        network_manager = NetworkManager(self.metadata_url)
        status, description = network_manager.fetch()
        if status:
            self.metadata = network_manager.content
        return status, description

    def download_collection(self, id, errstream=None):
        """Download a collection given its ID.

        :param id: The ID of the collection.
        :type id: str
        """
        local_repo_dir = os.path.join(
            QgsApplication.qgisSettingsDirPath(),
            'symbology_sharing',
            'repositories',
            self.git_host, self.git_owner, self.git_repository)
        if not os.path.exists(local_repo_dir):
            os.makedirs(local_repo_dir)
            with closing(
                    porcelain.clone(
                        self.url.encode('utf-8'), local_repo_dir)) as repo:
                return repo.path == local_repo_dir
        else:
            porcelain.pull(
                local_repo_dir, self.url.encode('utf-8'), b'refs/heads/master')
            # TODO: User should know if it's pulling out update again or just
            # using the current local repo to download the collection. For
            # now just return True
            return True
        return False

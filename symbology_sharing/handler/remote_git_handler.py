# coding=utf-8
import os
import shutil

from qgis.core import QgsApplication

from ext_libs.giturlparse import parse, validate
from ext_libs.dulwich import porcelain
from symbology_sharing.handler.base import BaseHandler
from symbology_sharing.network_manager import NetworkManager
from symbology_sharing.utilities import local_collection_path


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

    def download_collection(self, id, register_name):
        """Download a collection given its ID.

        For remote git repositories, we will clone the repository first (or pull
        if the repo is already cloned before) and copy the collection to
        collections dir.

        :param id: The ID of the collection.
        :type id: str
        """
        # Clone or pull the repositories first
        download_status = True
        local_repo_dir = os.path.join(
            QgsApplication.qgisSettingsDirPath(),
            'symbology_sharing',
            'repositories',
            self.git_host, self.git_owner, self.git_repository)
        if not os.path.exists(local_repo_dir):
            os.makedirs(local_repo_dir)
            repo = porcelain.clone(self.url.encode('utf-8'), local_repo_dir)
            download_status = repo.path == local_repo_dir
        else:
            porcelain.pull(
                local_repo_dir, self.url.encode('utf-8'), b'refs/heads/master')

        # Copy the specific downloaded collection to collections dir
        src_dir = os.path.join(local_repo_dir, 'collections', register_name)
        dest_dir = local_collection_path(id)
        if download_status:
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(src_dir, dest_dir)

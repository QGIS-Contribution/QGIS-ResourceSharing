# coding=utf-8
import os

from PyQt4.QtCore import QCoreApplication, QUrl
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import QgsNetworkAccessManager, QgsApplication

from ext_libs.giturlparse import parse, validate
from ext_libs.dulwich import porcelain

from base import BaseHandler


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
        self._network_manager = QgsNetworkAccessManager.instance()
        self._reply = None
        self._network_finished = False
        self._network_timeout = False

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
        request = QNetworkRequest(QUrl(self.metadata_url))
        request.setAttribute(
            QNetworkRequest.CacheLoadControlAttribute,
            QNetworkRequest.AlwaysNetwork)
        self._reply = self._network_manager.get(request)
        self._reply.finished.connect(self.fetch_metadata_finished)
        self._network_manager.requestTimedOut.connect(self.request_timeout)

        while not self._reply.isFinished():
            # noinspection PyArgumentList
            QCoreApplication.processEvents()

        # Finished
        description = None
        if self._reply.error() != QNetworkReply.NoError:
            status = False
            description = self._reply.errorString()
        else:
            status = True
            self.metadata = self._reply.readAll()

        self._reply.deleteLater()

        return status, description

    def fetch_metadata_finished(self):
        """Slot for when fetching metadata finished."""
        self._network_finished = True

    def request_timeout(self):
        self._network_timeout = True

    def download_collection(self, id, errstream):
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
            porcelain.clone(self.url.encode('utf-8'), local_repo_dir, errstream)
        else:
            # Pull for updates
            porcelain.pull(
                local_repo_dir, self.url.encode('utf-8'),
                b'refs/heads/master', errstream)

# coding=utf-8
from PyQt4.QtCore import QCoreApplication, QUrl, QTemporaryFile
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply

from qgis.core import QgsNetworkAccessManager

from ext_libs.giturlparse import parse, validate
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
        self._reply = self._network_manager.get(request)
        self._reply.finished.connect(self.fetch_metadata_finished)
        self._network_manager.requestTimedOut.connect(self.request_timeout)

        while not self._reply.isFinished():
            # noinspection PyArgumentList
            QCoreApplication.processEvents()

        # Finished
        if self._reply.error() != QNetworkReply.NoError:
            status = False
            description = self._reply.errorString()
        else:
            status = True
            self.metadata = self._reply.readAll()
            description = self.metadata

        self._reply.deleteLater()

        return status, description

    def fetch_metadata_finished(self):
        """Slot for when fetching metadata finished."""
        self._network_finished = True

    def request_timeout(self):
        self._network_timeout = True


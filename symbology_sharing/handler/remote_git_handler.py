# coding=utf-8
from PyQt4.QtCore import QObject, QCoreApplication, QUrl
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply

from qgis.core import QgsNetworkAccessManager

from ext_libs.giturlparse import parse, validate
from base import BaseHandler


class RemoteGitHandler(BaseHandler):
    """Class to handle generic git remote repository."""
    IS_DISABLED = True

    def __init__(self, url=None):
        """Constructor."""
        BaseHandler.__init__(self)
        self._url = None
        self._metadata = None
        self._git_platform = None
        self._git_host = None
        self._git_owner = None
        self._git_repository = None
        self._network_manager = QgsNetworkAccessManager.instance()
        self._reply = None
        self._progress_dialog = None
        self._handler_class = None

        # Call proper setters here
        self.url = url

    def can_handle(self):
        """Checking if handler can handle this URL.

        :param url: The URL of the repositoy.
        :type url: str
        """
        return False

    @property
    def metadata(self):
        return self._metadata

    @property
    def url(self):
        """The URL to the repository from QSettings.

        Example:
        - https://github.com/anitagraser/QGIS-style-repo-dummy.git
        """
        return self._url

    @url.setter
    def url(self, url):
        """Setter to the repository's URL."""
        if validate(url):
            self._url = url
        else:
            message = 'Error: URL is not a valid GIT URL.'
            raise Exception(message)

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

    def fetch_metadata(self, progress_dialog=None):
        """Fetch metadata file from the repository.

        :param progress_dialog: Progress dialog (optional)
        :type progress_dialog: QProgressDialog
        """
        if progress_dialog is not None:
            self._progress_dialog = progress_dialog
            # Set up progress dialog
            self._progress_dialog.show()
            # Just use infinite progress bar here
            self._progress_dialog.setMaximum(0)
            self._progress_dialog.setMinimum(0)
            self._progress_dialog.setValue(0)
            self._progress_dialog.setLabelText("Fetching repository's metadata")

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
            self._metadata = self._reply.readAll().data()
            description = self.metadata

        self._reply.deleteLater()

        return status, description

    def fetch_metadata_finished(self):
        """Slot for when fetching metadata finished."""
        if self._progress_dialog:
            self._progress_dialog.hide()

    def request_timeout(self):
        if self._progress_dialog:
            self._progress_dialog.hide()


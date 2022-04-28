import logging

from qgis.core import QgsAuthManager, QgsNetworkAccessManager
from qgis.PyQt.QtCore import QCoreApplication, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

from resource_sharing.utilities import qgis_version

LOGGER = logging.getLogger("QGIS Resource Sharing")


class NetworkManager(object):
    """Class to get the content of a file with a given URL."""

    def __init__(self, url, auth_cfg=None):
        self._network_manager = QgsNetworkAccessManager.instance()
        self._network_finished = False
        self._network_timeout = False
        self._url = url
        self._auth_cfg = auth_cfg
        self._content = None

    @property
    def content(self):
        return self._content

    @property
    def network_finished(self):
        return self._network_finished

    @property
    def network_timeout(self):
        return self._network_timeout

    def fetch(self):
        """Fetch the content (in the background).
        :return: (status, error message)
        :rtype: (boolean, string)
        """
        # Initialize some properties again
        self._content = None
        self._network_finished = False
        self._network_timeout = False

        request = QNetworkRequest(QUrl(self._url))
        request.setAttribute(
            QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.AlwaysNetwork
        )

        if self._auth_cfg and qgis_version() >= 21200:
            LOGGER.debug("Update request with auth_cfg %s" % self._auth_cfg)
            QgsAuthManager.instance().updateNetworkRequest(request, self._auth_cfg)

        self._reply = self._network_manager.get(request)
        self._reply.finished.connect(self.fetch_finished)
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
            self._content = self._reply.readAll()

        self._reply.deleteLater()

        return status, description

    def fetch_finished(self):
        """Called when fetching metadata has finished."""
        self._network_finished = True

    def request_timeout(self):
        """Called when a request timeout signal is emitted."""
        self._network_timeout = True

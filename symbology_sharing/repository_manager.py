# coding=utf-8
from PyQt4.QtCore import QObject, QSettings

from .utilities import repo_settings_group
from .handler import BaseHandler


class RepositoryManager(QObject):
    """Class to handle collection repositories."""
    OFFICIAL_REPO = (
        'QGIS Official Repository',
        'https://github.com/anitagraser/QGIS-style-repo-dummy.git')

    def __init__(self):
        """Constructor."""
        QObject.__init__(self)
        self._repositories = {}
        self.load()

    @property
    def repositories(self):
        """Property for repositories registered in settings.

        :returns: Dictionary of repositories registered
        :rtype: dict
        """
        return self._repositories

    def load(self):
        """Load repositories registered in settings."""
        self._repositories = {}
        settings = QSettings()
        settings.beginGroup(repo_settings_group())

        # Write Official Repository first to QSettings if needed
        official_repo_present = False
        for repo_name in settings.childGroups():
            url = settings.value(repo_name + '/url', '', type=unicode)
            if url == self.OFFICIAL_REPO[1]:
                official_repo_present = True
                break
        if not official_repo_present:
            settings.setValue(
                self.OFFICIAL_REPO[0] + '/url', self.OFFICIAL_REPO[1])

        for repo_name in settings.childGroups():
            self._repositories[repo_name] = {}
            self._repositories[repo_name]['url'] = settings.value(
                repo_name + '/url', '', type=unicode)
        settings.endGroup()

    def fetch_metadata(self, url):
        """Fetch metadata given the URL.

        :param url: The URL of the repository
        :type url: str
        """
        # Get the right handler for the given URL
        repo_handler = None
        for handler in BaseHandler.registry.values():
            handler_instance = handler(url)
            if handler_instance.can_handle():
                repo_handler = handler_instance
                break
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')
        status, description = repo_handler.fetch_metadata()
        return status, description

    def add_collections(self):
        """Add parsed collections."""
        pass

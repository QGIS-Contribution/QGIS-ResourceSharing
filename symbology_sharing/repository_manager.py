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
        self._collections = {}
        self.load()

    @property
    def repositories(self):
        """Property for repositories registered in settings.

        :returns: Dictionary of repositories registered
        :rtype: dict
        """
        return self._repositories

    @property
    def collections(self):
        return self._collections

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

    def add_repository(self, repo_name, url):
        """Add repository to settings and add the collections.

        :param url: The URL of the repository
        :type url: str
        """
        repo_handler = self.get_handler(url)
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')

        # Fetch metadata
        status, description = repo_handler.fetch_metadata()
        if status:
            # Parse metadata
            collections = repo_handler.parse_metadata()
            self.collections[repo_name] = collections
            # Add to QSettings
            settings = QSettings()
            settings.beginGroup(repo_settings_group())
            settings.setValue(repo_name + '/url', url)
            settings.endGroup()
        return status, description

    def edit_repository(self, old_repo_name, new_repo_name, new_url):
        """Edit repository and update the collections."""
        # Fetch the metadata from the new url
        repo_handler = self.get_handler(new_url)
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')
        status, description = repo_handler.fetch_metadata()

        if status:
            # Parse metadata
            collections = repo_handler.parse_metadata()
            # Remove old repo collections
            self.collections.pop(old_repo_name, None)
            # Add collections with the new repo name
            self.collections[new_repo_name] = collections
            # Update QSettings
            settings = QSettings()
            settings.beginGroup(repo_settings_group())
            settings.remove(old_repo_name)
            settings.setValue(new_repo_name + '/url', new_url)
            settings.endGroup()
        return status, description

    def remove_repository(self, old_repo_name):
        """Remove repository and all the collections of that repository."""
        # Remove collections
        self.collections.pop(old_repo_name, None)
        # Remove repo from QSettings
        settings = QSettings()
        settings.beginGroup(repo_settings_group())
        settings.remove(old_repo_name)
        settings.endGroup()

    def get_handler(self, url):
        """Get the right handler instance for given URL.

        :param url: The url of the repository
        :type url: str

        :return: The handler instance. None if no handler found.
        :rtype: BaseHandler, None
        """
        repo_handler = None
        for handler in BaseHandler.registry.values():
            handler_instance = handler(url)
            if handler_instance.can_handle():
                repo_handler = handler_instance
                break
        return repo_handler

# coding=utf-8
from PyQt4.QtCore import QObject, QSettings

from .utilities import repo_settings_group


class RepositoryManager(QObject):
    """Class to handle collection repositories."""
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
        for repo_name in settings.childGroups():
            self._repositories[repo_name] = {}
            self._repositories[repo_name]['url'] = settings.value(
                repo_name + '/url', '', type=unicode)
        settings.endGroup()
        print 'test'

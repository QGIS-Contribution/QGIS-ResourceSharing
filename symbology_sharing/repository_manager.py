# coding=utf-8
import csv

from PyQt4.QtCore import QObject, QSettings, QTemporaryFile

from .utilities import repo_settings_group
from .handler import BaseHandler
from .file_downloader import FileDownloader
from collections_manager import CollectionsManager


class RepositoryManager(QObject):
    """Class to handle collection repositories."""

    DIRECTORY_URL = 'https://raw.githubusercontent.com/anitagraser/QGIS-style-repo-dummy/master/directory.csv'

    def __init__(self):
        """Constructor.

        ..note:
        - Repositories is a list of repository that are registered in user's
        QGIS. Data structure of repositories:
        self._repositories = {
            'QGIS Official Repository': 'git@github.com:anitagraser/QGIS-style-repo-dummy.git',
            'Akbar's Github Repository': 'git@github.com:akbargumbira/QGIS-style-repo-dummy.git',
            'Akbar's Bitbucket Repository': 'git@bitbucket.org:akbargumbira/qgis-style-repo-dummy.git'
        }
        """
        QObject.__init__(self)
        self._online_directory = {}
        self._repositories = {}
        self._collections_manager = CollectionsManager()
        # Fetch online dir
        self.fetch_directory()
        # Load repositories from settings
        self.load()
        # Load collections from settings
        self._collections_manager.load()

    @property
    def repositories(self):
        """Property for repositories registered in settings.

        :returns: Dictionary of repositories registered
        :rtype: dict
        """
        return self._repositories

    @property
    def collections_manager(self):
        return self._collections_manager

    @property
    def collections(self):
        """Get all the collections registered."""
        return self._collections_manager.collections

    def fetch_directory(self):
        downloader = FileDownloader(self.DIRECTORY_URL)
        status, _ = downloader.fetch()
        if status:
            directory_file = QTemporaryFile()
            if directory_file.open():
                directory_file.write(downloader.content)
                directory_file.close()

            with open(directory_file.fileName()) as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=('name', 'url'))
                for row in reader:
                    self._online_directory[row['name']] = row['url'].strip()

    def load(self):
        """Load repositories registered in settings."""
        # import pydevd
        # pydevd.settrace('localhost', port=8080, stdoutToServer=True,
        #                 stderrToServer=True)
        self._repositories = {}
        settings = QSettings()
        settings.beginGroup(repo_settings_group())

        # Write online directory first to QSettings if needed
        for online_dir_name in self._online_directory:
            repo_present = False
            for repo_name in settings.childGroups():
                url = settings.value(repo_name + '/url', '', type=unicode)
                if url == self._online_directory[online_dir_name]:
                    repo_present = True
                    break
            if not repo_present:
                self.add_repository(
                    online_dir_name, self._online_directory[online_dir_name])

        for repo_name in settings.childGroups():
            self._repositories[repo_name] = {}
            url = settings.value(
                repo_name + '/url', '', type=unicode)
            self._repositories[repo_name]['url'] = url
        settings.endGroup()

    def add_repository(self, repo_name, url):
        """Add repository to settings and add the collections from that repo.

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
            self._collections_manager.add_repo_collection(
                repo_name, collections)
            # Add to QSettings
            settings = QSettings()
            settings.beginGroup(repo_settings_group())
            settings.setValue(repo_name + '/url', url)
            settings.endGroup()
            # Serialize collections every time we sucessfully added repo
            self._collections_manager.serialize()

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
            self._collections_manager.remove_repo_collection(old_repo_name)
            # Add collections with the new repo name
            self._collections_manager.add_repo_collection(
                new_repo_name, collections)
            # Update QSettings
            settings = QSettings()
            settings.beginGroup(repo_settings_group())
            settings.remove(old_repo_name)
            settings.setValue(new_repo_name + '/url', new_url)
            settings.endGroup()
            # Serialize collections every time we sucessfully edited repo
            self._collections_manager.serialize()
        return status, description

    def remove_repository(self, old_repo_name):
        """Remove repository and all the collections of that repository."""
        # Remove collections
        self._collections_manager.remove_repo_collection(old_repo_name)
        # Remove repo from QSettings
        settings = QSettings()
        settings.beginGroup(repo_settings_group())
        settings.remove(old_repo_name)
        settings.endGroup()
        # Serialize collections every time sucessfully remove a repo
        self._collections_manager.serialize()

    def reload_repository(self, repo_name, url):
        """Re-fetch the repository and update the collections registry."""
        status, description = self.edit_repository(repo_name, repo_name, url)
        return status, description

    def download_collection(self, id, errstream):
        """Download collection given the id."""
        repo_url = self.collections[id]['repository_url']
        repo_handler = self.get_handler(repo_url)
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')
        repo_handler.download_collection(id, errstream)


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

# coding=utf-8
import hashlib
# Use pathlib instead of os.path
from pathlib import Path
import shutil
import logging
import traceback

from qgis.PyQt.QtCore import (
    pyqtSignal, QObject)

from resource_sharing import config
from resource_sharing.config import (
    COLLECTION_INSTALLED_STATUS, COLLECTION_NOT_INSTALLED_STATUS)
from resource_sharing.utilities import (
    local_collection_path,
    render_template,
    resources_path)
from resource_sharing.repository_handler import BaseRepositoryHandler
from resource_sharing.resource_handler import BaseResourceHandler

LOGGER = logging.getLogger('QGIS Resource Sharing')


class CollectionInstaller(QObject):
    finished = pyqtSignal()
    aborted = pyqtSignal()
    progress = pyqtSignal(basestring)

    def __init__(self, collection_manager, collection_id):
        QObject.__init__(self)
        self._collection_manager = collection_manager
        self._collection_id = collection_id
        self.install_status = False
        self.error_message = None
        self.killed = False

    def run(self):
        self.progress.emit('Downloading the collection...')

        # We can't kill the process here, so let us finish it even if
        # the user cancels the download process
        download_status, error_message = self._collection_manager.download(
            self._collection_id)

        # If at this point it is killed, so abort and tell the main thread
        if self.killed:
            self.aborted.emit()
            return

        # If download fails
        if not download_status:
            self.install_status = False
            self.error_message = error_message
            self.finished.emit()
            return

        # Downloading is fine, It is not killed, let us install it
        if not self.killed:
            self.progress.emit('Installing the collection...')
            try:
                self._collection_manager.install(self._collection_id)
            except Exception as e:
                self.error_message = e
                LOGGER.exception(traceback.format_exc())
        else:
            # Downloaded but killed
            self.aborted.emit()
            return

        # If finished installing but killed here? just emit finished
        self.install_status = True
        self.finished.emit()

    def abort(self):
        self.killed = True


class CollectionManager(object):
    def __init__(self):
        """"Utilities class related to collection."""

    def get_collection_id(self, register_name, repo_url):
        """Generate the collection ID."""
        hash_object = hashlib.sha1((register_name + repo_url).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def get_html(self, collection_id):
        """Return the details of a collection as HTML, given its id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        html = ''
        resource_types = 0
        if 'svg' in config.COLLECTIONS[collection_id].keys():
            html = html + str(config.COLLECTIONS[collection_id]['svg']) + ' SVG'
            if config.COLLECTIONS[collection_id]['svg'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'style' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['style']) + ' Layer style (QML) file'
            if config.COLLECTIONS[collection_id]['style'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'symbol' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['symbol']) + ' Symbol (XML) file'
            if config.COLLECTIONS[collection_id]['symbol'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'models' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['models']) + ' Processing model'
            if config.COLLECTIONS[collection_id]['models'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'expressions' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['expressions']) + ' Expression (JSON) file'
            if config.COLLECTIONS[collection_id]['expressions'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'processing' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['processing']) + ' Processing script'
            if config.COLLECTIONS[collection_id]['processing'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        if 'rscripts' in config.COLLECTIONS[collection_id].keys():
            if resource_types > 0:
                html = html + ', '
            html = html + str(config.COLLECTIONS[collection_id]['rscripts']) + ' R script'
            if config.COLLECTIONS[collection_id]['rscripts'] > 1:
                html = html + 's'
            resource_types = resource_types + 1
        html = html + '.<br><i>Reinstall</i> to update'
        if resource_types == 0:
            html = '<i>No standard resources found</i>.'
        if config.COLLECTIONS[collection_id]['status'] != COLLECTION_INSTALLED_STATUS:
            html = '<i>Unknown before installation</i>'

        config.COLLECTIONS[collection_id]['resources_html'] = html
        context = {
            'resources_path': str(resources_path()),
            'collection': config.COLLECTIONS[collection_id]
        }
        return render_template('collection_details.html', context)

    def get_installed_collections(self, repo_url=None):
        """Get all installed collections for a given repository URL.

        If a URL is not specified, all the installed collections
        will be returned.

        :param repo_url: The repository URL.
        :type repo_url: str

        :return: Subset of config.COLLECTIONS that meet the requirement
        :rtype: dict
        """
        installed_collections = {}
        for id, collection in config.COLLECTIONS.items():
            if collection['status'] != COLLECTION_INSTALLED_STATUS:
                continue

            if repo_url:
                if collection['repository_url'] != repo_url:
                    continue

            installed_collections[id] = collection

        return installed_collections

    def download(self, collection_id):
        """Download a collection given its ID.

        :param collection_id: The ID of the collection to be downloaded.
        :type collection_id: str
        :return: status (True or False), information from the repo handler
        :rtype: (boolean, string)
        """
        repo_url = config.COLLECTIONS[collection_id]['repository_url']
        repo_handler = BaseRepositoryHandler.get_handler(repo_url)
        if repo_handler is None:
            message = 'There is no handler available for ' + str(repo_url)
            LOGGER.error(message)
            return False, message
        register_name = config.COLLECTIONS[collection_id]['register_name']
        status, information = repo_handler.download_collection(
            collection_id, register_name)
        return status, information

    def install(self, collection_id):
        """Install the collection.

        :param collection_id: The id of the collection about to be installed.
        :type collection_id: str
        """
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.install()

        config.COLLECTIONS[collection_id]['status'] = \
            COLLECTION_INSTALLED_STATUS

    def uninstall(self, collection_id):
        """Uninstall the collection.

        :param collection_id: The id of the collection about to be uninstalled.
        :type collection_id: str
        """
        # Uninstall all types of resources
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.uninstall()

        # Remove the collection directory
        collection_dir = local_collection_path(collection_id)
        if collection_dir.exists():
            shutil.rmtree(str(collection_dir))

        config.COLLECTIONS[collection_id]['status'] = \
            COLLECTION_NOT_INSTALLED_STATUS

        # Should items from other installed collections be reinstalled
        # "automatically"?
        # Relevant if an item in another installed collection has the same
        # file name as one of the files that have been removed (and is
        # installed in the same directory).
        # for coll_id in config.COLLECTIONS:
        #     install(self, coll_id)

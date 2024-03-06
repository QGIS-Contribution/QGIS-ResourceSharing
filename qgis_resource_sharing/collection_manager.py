import hashlib
import logging
import shutil
import traceback
from typing import Dict

from qgis.PyQt.QtCore import QObject, pyqtSignal

from qgis_resource_sharing import config
from qgis_resource_sharing.__about__ import __title__
from qgis_resource_sharing.config import (
    COLLECTION_INSTALLED_STATUS,
    COLLECTION_NOT_INSTALLED_STATUS,
)
from qgis_resource_sharing.repository_handler import BaseRepositoryHandler
from qgis_resource_sharing.resource_handler import BaseResourceHandler
from qgis_resource_sharing.utilities import (
    SUPPORTED_RESOURCES_MAP,
    local_collection_path,
)

LOGGER = logging.getLogger(__title__)


class CollectionInstaller(QObject):
    finished = pyqtSignal()
    aborted = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, collection_manager, collection_id):
        QObject.__init__(self)
        self._collection_manager = collection_manager
        self._collection_id = collection_id
        self.install_status = False
        self.error_message = None
        self.killed = False

    def run(self):
        self.progress.emit(self.tr("Downloading the collection..."))

        # We can't kill the process here, so let us finish it even if
        # the user cancels the download process
        download_status, error_message = self._collection_manager.download(
            self._collection_id
        )

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
            self.progress.emit(self.tr("Installing the collection..."))
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
        """Utilities class related to collection."""

    def get_collection_id(self, register_name, repo_url):
        """Generate the collection ID."""
        hash_object = hashlib.sha1((register_name + repo_url).encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def get_resource_status(self, collection_id: str) -> str:
        """Return the status (installed, not installed) of a collection
        as HTML, given its id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        html = ""
        resource_types = 0
        for type_, desc in SUPPORTED_RESOURCES_MAP.items():
            if type_ in config.COLLECTIONS[collection_id].keys():
                if resource_types > 0:
                    html += ", "
                html += f"{config.COLLECTIONS[collection_id][type_]} {desc}"
                if config.COLLECTIONS[collection_id][type_] > 1:
                    html += "s"
                resource_types += 1
        html = html + ".<br><i>Reinstall</i> to update"
        if resource_types == 0:
            html = "<i>No standard resources found</i>."
        if config.COLLECTIONS[collection_id]["status"] != COLLECTION_INSTALLED_STATUS:
            html = "<i>Unknown before installation</i>"

        return html

    def get_collection(self, collection_id: str) -> Dict[str, str]:
        """Return the details of a collection, given its id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        resource_html = self.get_resource_status(collection_id)
        config.COLLECTIONS[collection_id]["resources_html"] = resource_html
        return config.COLLECTIONS[collection_id]

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
        for collection_id, collection in config.COLLECTIONS.items():
            if collection["status"] != COLLECTION_INSTALLED_STATUS:
                continue

            if repo_url:
                if collection["repository_url"] != repo_url:
                    continue

            installed_collections[collection_id] = collection

        return installed_collections

    def download(self, collection_id):
        """Download a collection given its ID.

        :param collection_id: The ID of the collection to be downloaded.
        :type collection_id: str
        :return: status (True or False), information from the repo handler
        :rtype: (boolean, string)
        """
        repo_url = config.COLLECTIONS[collection_id]["repository_url"]
        repo_handler = BaseRepositoryHandler.get_handler(repo_url)
        if repo_handler is None:
            message = "There is no handler available for " + str(repo_url)
            LOGGER.error(message)
            return False, message
        register_name = config.COLLECTIONS[collection_id]["register_name"]
        status, information = repo_handler.download_collection(
            collection_id, register_name
        )
        return status, information

    def install(self, collection_id):
        """Install the collection.

        :param collection_id: The id of the collection about to be installed.
        :type collection_id: str
        """
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.install()

        config.COLLECTIONS[collection_id]["status"] = COLLECTION_INSTALLED_STATUS

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

        config.COLLECTIONS[collection_id]["status"] = COLLECTION_NOT_INSTALLED_STATUS

        # Should items from other installed collections be reinstalled
        # "automatically"?
        # Relevant if an item in another installed collection has the same
        # file name as one of the files that have been removed (and is
        # installed in the same directory).
        # for coll_id in config.COLLECTIONS:
        #     install(self, coll_id)

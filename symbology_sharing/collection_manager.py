# coding=utf-8
import hashlib
import os
import shutil

from symbology_sharing import config
from symbology_sharing.config import (
    COLLECTION_INSTALLED_STATUS, COLLECTION_NOT_INSTALLED_STATUS)
from symbology_sharing.utilities import (
    local_collection_path,
    render_template,
    resources_path)
from symbology_sharing.repository_handler import BaseRepositoryHandler
from symbology_sharing.resource_handler import BaseResourceHandler


class CollectionManager(object):
    def __init__(self):
        """"Utilities class related to collection."""

    def get_collection_id(self, register_name, repo_url):
        """Generate id of a collection."""
        hash_object = hashlib.sha1((register_name + repo_url).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def get_html(self, collection_id):
        """Return the detail of a collection in HTML form given the id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        context = {
            'resources_path': resources_path(),
            'collection': config.COLLECTIONS[collection_id]
        }
        return render_template('collection_details.html', context)

    def download(self, collection_id):
        """Download a collection given the id.

        :param collection_id: The id of the collection about to be downloaded.
        :type collection_id: str
        """
        repo_url = config.COLLECTIONS[collection_id]['repository_url']
        repo_handler = BaseRepositoryHandler.get_handler(repo_url)
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')
        register_name = config.COLLECTIONS[collection_id]['register_name']
        status, information = repo_handler.download_collection(
            collection_id, register_name)
        return status, information

    def install(self, collection_id):
        """Install a collection into QGIS.

        :param collection_id: The id of the collection about to be installed.
        :type collection_id: str
        """
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.install()
        config.COLLECTIONS[collection_id]['status'] = COLLECTION_INSTALLED_STATUS

    def uninstall(self, collection_id):
        """Uninstall the collection from QGIS.

        :param collection_id: The id of the collection about to be uninstalled.
        :type collection_id: str
        """
        # Uninstall all type of resources from QGIS
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.uninstall()
        # Remove the collection directory
        collection_dir = local_collection_path(collection_id)
        if os.path.exists(collection_dir):
            shutil.rmtree(collection_dir)
        config.COLLECTIONS[collection_id]['status'] = COLLECTION_NOT_INSTALLED_STATUS

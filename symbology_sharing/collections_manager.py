# coding=utf-8
import hashlib
import os
import shutil

from symbology_sharing.collection import (
    COLLECTION_INSTALLED_STATUS, COLLECTION_NOT_INSTALLED_STATUS)
from symbology_sharing.utilities import local_collection_path
from symbology_sharing.repository_handler import BaseRepositoryHandler
from symbology_sharing.resource_handler import BaseResourceHandler


class CollectionsManager(object):
    def __init__(self):
        """"Constructor for Collection class.

        self.collections is a dict of collection with this structure:
        self.collections = {
            collection_id (computed): {
                'register_name': collection,
                'author': author,
                'author_email': email,
                'repository_url': self.url,
                'status': COLLECTION_NOT_INSTALLED_STATUS,
                'name': parser.get(collection, 'name'),
                'tags': parser.get(collection, 'tags'),
                'description': parser.get(collection, 'description'),
                'qgis_min_version': parser.get(collection, 'qgis_minimum_version'),
                'qgis_max_version': parser.get(collection, 'qgis_maximum_version')
            },
            ....
        }
        """
        self._collections = {}

    @property
    def collections(self):
        return self._collections

    @collections.setter
    def collections(self, collections):
        self._collections = collections

    def get_collection_id(self, register_name, repo_url):
        """Generate id of a collection."""
        hash_object = hashlib.sha1((register_name + repo_url).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def html(self, collection_id):
        """Return the detail of a collection in HTML form given the id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        html = ''
        html += "<style>" \
                "   body, table {" \
                "   padding:0px;" \
                "   margin:0px;" \
                "   font-family:verdana;" \
                "   font-size: 12px;" \
                "  }" \
                "</style>"
        html += "<body>"
        html += "<table cellspacing=\"4\" width=\"100%\"><tr><td>"
        html += "<h1>%s</h1>" % self.collections[collection_id]['name']
        html += "<h3>%s</h3><br/>" % self.collections[collection_id]['description']
        html += "URL: %s <br/></br>" % self.collections[collection_id]['repository_url']
        html += "Tags: %s <br/></br>" % self.collections[collection_id]['tags']
        html += "Author: %s <br/></br>" % self.collections[collection_id]['author']
        html += "E-mail: %s" % self.collections[collection_id]['author_email']
        html += "</td></tr></table>"
        html += "</body>"
        return html

    def download_collection(self, collection_id):
        """Download a collection given the id.

        :param collection_id: The id of the collection about to be downloaded.
        :type collection_id: str
        """
        repo_url = self.collections[collection_id]['repository_url']
        repo_handler = BaseRepositoryHandler.get_handler(repo_url)
        if repo_handler is None:
            raise Exception('There is no handler available for the given URL!')
        register_name = self.collections[collection_id]['register_name']
        status, information = repo_handler.download_collection(
            collection_id, register_name)
        return status, information

    def install_collection(self, collection_id):
        """Install a collection into QGIS.

        :param collection_id: The id of the collection about to be installed.
        :type collection_id: str
        """
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.install()
        self.collections[collection_id]['status'] = COLLECTION_INSTALLED_STATUS

    def uninstall_collection(self, collection_id):
        """Uninstall the collection from QGIS.

        :param collection_id: The id of the collection about to be uninstalled.
        :type collection_id: str
        """
        # Remove the collection directory
        collection_dir = local_collection_path(collection_id)
        if os.path.exists(collection_dir):
            shutil.rmtree(collection_dir)
        # Uninstall all type of resources from QGIS
        for resource_handler in BaseResourceHandler.registry.values():
            resource_handler_instance = resource_handler(collection_id)
            resource_handler_instance.uninstall()
        self.collections[collection_id][
            'status'] = COLLECTION_NOT_INSTALLED_STATUS

# coding=utf-8
import hashlib
import pickle
import os

from symbology_sharing.collection import COLLECTION_NOT_INSTALLED_STATUS
from symbology_sharing.utilities import (
    collection_cache_path, local_collection_path)


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

        self.repo_collections is a list dict of collection with this structure:
        self.repo_collection = {
            repo_name: [{
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

        They are separated for different operation. self.collections is to
        deal with each collection (downloading, browsing, searching,
        etc). Self.repo_collection is to deal with adding, updating, removing repository.
        """
        self._collections = {}
        self._repo_collections = {}

    @property
    def collections(self):
        return self._collections

    @property
    def repo_collections(self):
        return self._repo_collections

    def add_repo_collection(self, name, collections):
        """Add repo collections.

        :param name: The name of the repository.
        :type name: str

        :param collections: The list of collections.
        :type collections: list
        """
        self.repo_collections[name] = collections
        self.rebuild_collections()

    def remove_repo_collection(self, name):
        """Remove a repo collection by name from repo collections."""
        self.repo_collections.pop(name, None)
        self.rebuild_collections()

    def rebuild_collections(self):
        """Rebuild collections from repo collections."""
        self._collections = {}
        for repo in self._repo_collections.keys():
            repo_collections = self.repo_collections[repo]
            for collection in repo_collections:
                collection_id = self.get_collection_id(
                    collection['register_name'], collection['repository_url'])
                self._collections[collection_id] = collection
                # Check in the file system if the collection exists
                if not os.path.exists(local_collection_path(collection_id)):
                    self._collections[collection_id]['status'] = COLLECTION_NOT_INSTALLED_STATUS

    def get_collection_id(self, register_name, repo_url):
        """Generate id of a collection."""
        hash_object = hashlib.sha1((register_name + repo_url).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def serialize(self):
        """Save repo collections to cache."""
        if not os.path.exists(os.path.dirname(collection_cache_path())):
            os.makedirs(os.path.dirname(collection_cache_path()))

        with open(collection_cache_path(), 'wb') as f:
            pickle.dump(self.repo_collections, f)

    def load(self):
        """Load repo collections from cache and rebuild collections."""
        repo_collections = {}
        if os.path.exists(collection_cache_path()):
            with open(collection_cache_path(), 'r') as f:
                repo_collections = pickle.load(f)
        self._repo_collections = repo_collections
        self.rebuild_collections()

    def html(self, id):
        """Return html of the metadata given the id.

        :param id: The id of the collection
        :type id: str
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
        html += "<h1>%s</h1>" % self.collections[id]['name']
        html += "<h3>%s</h3><br/>" % self.collections[id]['description']
        html += "URL: %s <br/></br>" % self.collections[id]['repository_url']
        html += "Tags: %s <br/></br>" % self.collections[id]['tags']
        html += "Author: %s <br/></br>" % self.collections[id]['author']
        html += "E-mail: %s" % self.collections[id]['author_email']
        html += "</td></tr></table>"
        html += "</body>"
        return html

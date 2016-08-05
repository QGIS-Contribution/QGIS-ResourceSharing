# coding=utf-8
import logging
import urlparse
from zipfile import ZipFile

from PyQt4.QtCore import QTemporaryFile

from resource_sharing.repository_handler.base import BaseRepositoryHandler
from resource_sharing.utilities import local_collection_path
from resource_sharing.network_manager import NetworkManager


LOGGER = logging.getLogger('QGIS Resources Sharing')


class RemoteZipHandler(BaseRepositoryHandler):
    """Class to handle remote zip repository."""
    IS_DISABLED = False

    def __init__(self, url=None):
        """Constructor."""
        BaseRepositoryHandler.__init__(self, url)

    def can_handle(self):
        if not self.is_git_repository:
            if self._parsed_url.scheme in ['http', 'https']:
                return True
        return False

    def fetch_metadata(self):
        """Fetch metadata file from the url."""
        # Download the metadata
        metadata_url = urlparse.urljoin(self.url, self.METADATA_FILE)
        network_manager = NetworkManager(metadata_url, self.auth_cfg)
        status, description = network_manager.fetch()
        if status:
            self.metadata = network_manager.content
        return status, description

    def download_collection(self, id, register_name):
        """Download a collection given its ID.

        For zip collection, we will download the zip, and extract the
        collection to collections dir.

        :param id: The ID of the collection.
        :type id: str

        :param register_name: The register name of the collection (the
            section name of the collection)
        :type register_name: unicode
        """
        # Download the zip first
        collection_path = 'collections/%s.zip' % register_name
        zip_collection_url = urlparse.urljoin(self.url, collection_path)
        network_manager = NetworkManager(zip_collection_url)
        status, description = network_manager.fetch()

        if not status:
            return False, description

        # Create the zip file
        zip_file = QTemporaryFile()
        if zip_file.open():
            zip_file.write(network_manager.content)
            zip_file.close()

        zf = ZipFile(zip_file.fileName())
        zf.extractall(path=local_collection_path(id))
        return True, None

    def preview_url(self, collection_name, file_path):
        image_path = 'collections/%s/%s' % (collection_name, file_path)
        image_url = urlparse.urljoin(self.url, image_path)
        return image_url

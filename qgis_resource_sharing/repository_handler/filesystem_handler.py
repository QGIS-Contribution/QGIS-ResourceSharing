import logging
import shutil
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import pathname2url

from qgis_resource_sharing.repository_handler.base import BaseRepositoryHandler
from qgis_resource_sharing.utilities import local_collection_path

LOGGER = logging.getLogger("QGIS Resource Sharing")


class FileSystemHandler(BaseRepositoryHandler):
    """Handler for file system repositories."""

    IS_DISABLED = False

    def __init__(self, url):
        """Constructor."""
        BaseRepositoryHandler.__init__(self, url)

        self._path = self._parsed_url.path

    def can_handle(self):
        if not self.is_git_repository:
            if self._parsed_url.scheme == "file":
                return True

    def fetch_metadata(self):
        """Fetch the metadata file from the repository."""
        # Check if the metadata exists
        metadata_path = Path(self._path) / self.METADATA_FILE
        if not metadata_path.exists():
            message = "The metadata file could not be found in the repository"
            return False, message

        # Read the metadata file:
        with open(str(metadata_path), "r") as metadata_file:
            metadata_content = metadata_file.read()
        self.metadata = metadata_content
        message = "Metadata successfully fetched"

        return True, message

    def download_collection(self, collection_id, register_name):
        """Download a collection given its ID.

        :param collection_id: The ID of the collection.
        :type collection_id: str

        :param register_name: The register name of the collection (the
            section name of the collection)
        :type register_name: unicode
        """
        # Copy the specific downloaded collection to collections dir
        src_dir = Path(self._path) / "collections" / register_name
        if not src_dir.exists():
            error_message = "Error: The collection does not exist in the " "repository."
            return False, error_message

        dest_dir = local_collection_path(collection_id)
        if dest_dir.exists():
            shutil.rmtree(str(dest_dir))
        shutil.copytree(str(src_dir), str(dest_dir))

        return True, None

    def file_url(self, relative_path):
        file_path = Path(self._path, relative_path)
        return urljoin("file:", pathname2url(str(file_path)))

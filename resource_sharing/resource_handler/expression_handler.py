# coding=utf-8
from pathlib import Path
import logging

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.utilities import qgis_version

LOGGER = logging.getLogger('QGIS Resource Sharing')
EXPRESSIONS = 'expressions'

class ExpressionHandler(BaseResourceHandler):
    """Concrete class of the Expression handler."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        # Initialize with the QGIS settings????

    @classmethod
    def dir_name(self):
        return EXPRESSIONS

    def install(self):
        """Add the expressions from this collection to QGIS settings.
        """
        # Skip installation if the directory does not exist
        if not Path(self.resource_dir).exists():
            return

        # Uninstall first (in case it is a reinstall)
        self.uninstall()

        # Get all the expressions in the collection
        json_files = []
        valid = 0
        for item in Path(self.resource_dir).glob('*.json'):
            file_path = Path(self.resource_dir, item)
            json_files.append(file_path)
            valid += 1

        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return

        for json_file in json_files:
            file_name = json_file.stem
            LOGGER.info("Installing expressions from " + file_name)
            valid += 1
        if valid >= 0:
            self.collection[EXPRESSIONS] = valid

    def uninstall(self):
        """Remove the expressions of this collection from QGIS settings.
        """

        # Remove from settings
        LOGGER.info("Removing expressions")
        # Remove files - nothing to remove


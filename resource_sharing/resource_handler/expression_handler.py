# coding=utf-8
from pathlib import Path
import json
import logging

from qgis.core import QgsSettings
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis
#try:
#    from qgis.core import QgsExpressions

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

        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())

        # Get all the expressions in the collection
        json_files = []
        valid = 0
        for item in Path(self.resource_dir).glob('*'):
            if item.suffix.lower().endswith("json"):
                file_path = Path(self.resource_dir, item)
                json_files.append(file_path)
                valid += 1

        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return

        for json_file in json_files:
            #file_name = json_file.stem
            LOGGER.info("Installing expressions from " + json_file)

            with open(json_file, 'rb') as expr_file:
                expr_json = expr_file.read()
            jsontext = json.loads(expr_json)
            expressions = jsontext['expressions']
            for expr in expressions:
                settings.setValue(expr['name'] + '\expression', expr['expression'])
                settings.setValue(expr['name'] + '\helpText', expr['description'])
            valid += 1
        settings.endGroup()
        if valid >= 0:
            self.collection[EXPRESSIONS] = valid

    def uninstall(self):
        """Remove the expressions of this collection from QGIS settings.
        """

        # Remove from settings
        LOGGER.info("Removing expressions")
        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())
        settings.endGroup()
        # Remove files - nothing to remove


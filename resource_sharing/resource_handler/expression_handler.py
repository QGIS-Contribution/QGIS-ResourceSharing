# coding=utf-8
from pathlib import Path
import json
import logging

from qgis.core import QgsSettings
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.utilities import (user_expressions_group, repo_settings_group, qgis_version)

hasExprBuilder = False
#try:
#    from qgis.core import QgsExpressions

try:
    from qgis.gui import QgsExpressionBuilderWidget
except:
    hasExprBuilder = False
else:
    hasExprBuilder = True

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
        LOGGER.info("Installing expressions")
        #return
        # Skip installation if the directory does not exist
        if not Path(self.resource_dir).exists():
            return

        # Uninstall first (in case it is a reinstall)
        #self.uninstall()

        # Get all the expressions in the collection
        json_files = []
        valid = 0
        for item in Path(self.resource_dir).glob('*'):
            if item.suffix.lower().endswith("json"):
                file_path = Path(self.resource_dir, item)
                json_files.append(file_path)
        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return
        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())
        for json_file in json_files:
            namePrefix = json_file.stem + '_'
            LOGGER.info("Installing expressions from " + str(json_file))

            with open(json_file, 'rb') as expr_file:
                expr_json = expr_file.read()
            jsontext = json.loads(expr_json)

            #QgsExpressionBuilderWidget loadExpressionsFromJson

            expressions = jsontext['expressions']
            for expr in expressions:
                expr_name = namePrefix + expr['name']
                LOGGER.info("Expr. name: " + expr_name)
                expr_value =expr['expression']
                LOGGER.info("Expr. expression: " + expr_value)
                expr_help = expr['description']
                LOGGER.info("Expr. description: " + expr_help)

                settings.setValue(expr_name + '/expression', expr_value)
                settings.setValue(expr_name + '/helpText', expr_help)
                aftervalue = settings.value(expr_name + '/expression', '', type=unicode).strip()
                LOGGER.info("after - expr: " + aftervalue)
            valid += 1
        settings.endGroup()
        if valid >= 0:
            self.collection[EXPRESSIONS] = valid

    def uninstall(self):
        """Remove the expressions in this collection from QGIS settings.
        """

        # Remove from settings
        LOGGER.info("Removing expressions")
        # Skip removal if the directory does not exist
        if not Path(self.resource_dir).exists():
            return
        # Get all the expressions in the collection
        json_files = []
        for item in Path(self.resource_dir).glob('*'):
            if item.suffix.lower().endswith("json"):
                file_path = Path(self.resource_dir, item)
                json_files.append(file_path)
        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return
        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())
        for json_file in json_files:
            namePrefix = json_file.stem + '_'
            LOGGER.info("Removing expressions from " + str(json_file))
            with open(json_file, 'rb') as expr_file:
                expr_json = expr_file.read()
            jsontext = json.loads(expr_json)
            expressions = jsontext['expressions']
            for expr in expressions:
                expr_name = namePrefix + expr['name']
                LOGGER.info("Expr. name: " + expr_name)
                if settings.contains(expr_name + '/expression'):
                   LOGGER.info("Exists - removing")
                   settings.remove(expr_name)
        settings.endGroup()
        # Remove files - nothing to remove


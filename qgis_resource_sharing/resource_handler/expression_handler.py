import json
import logging
from pathlib import Path

from qgis.core import QgsSettings

from qgis_resource_sharing.__about__ import __title__
from qgis_resource_sharing.resource_handler.base import BaseResourceHandler
from qgis_resource_sharing.utilities import user_expressions_group

hasExprBuilder = False


LOGGER = logging.getLogger(__title__)
EXPRESSIONS = "expressions"


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
        """Add the expressions from this collection to QGIS settings."""
        # Skip installation if the directory does not exist
        if not Path(self.resource_dir).exists():
            return

        # Uninstall first (in case it is a reinstall)
        # self.uninstall()

        # Get all the expressions in the collection
        json_files = []
        valid = 0
        for item in Path(self.resource_dir).glob("*"):
            if item.suffix.lower().endswith("json"):
                file_path = Path(self.resource_dir, item)
                json_files.append(file_path)
        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return
        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())
        for json_file in json_files:
            namePrefix = json_file.stem + "_"
            with open(json_file, "rb") as expr_file:
                expr_json = expr_file.read()
            jsontext = json.loads(expr_json)
            # QgsExpressionBuilderWidget loadExpressionsFromJson

            expressions = jsontext["expressions"]
            for expr in expressions:
                expr_name = namePrefix + expr["name"]
                expr_value = expr["expression"]
                expr_help = expr["description"]
                settings.setValue(expr_name + "/expression", expr_value)
                settings.setValue(expr_name + "/helpText", expr_help)
                # aftervalue = settings.value(
                #     expr_name + "/expression", "", type=unicode
                # ).strip()
            valid += 1
        settings.endGroup()
        if valid >= 0:
            self.collection[EXPRESSIONS] = valid

    def uninstall(self):
        """Remove the expressions in this collection from QGIS settings."""
        # Remove from settings
        # Skip removal if the directory does not exist
        if not Path(self.resource_dir).exists():
            return
        # Get all the expressions in the collection
        json_files = []
        for item in Path(self.resource_dir).glob("*"):
            if item.suffix.lower().endswith("json"):
                file_path = Path(self.resource_dir, item)
                json_files.append(file_path)
        # If there are no json files, there is nothing to do
        if len(json_files) == 0:
            return
        settings = QgsSettings()
        settings.beginGroup(user_expressions_group())
        for json_file in json_files:
            namePrefix = json_file.stem + "_"
            with open(json_file, "rb") as expr_file:
                expr_json = expr_file.read()
            jsontext = json.loads(expr_json)
            expressions = jsontext["expressions"]
            for expr in expressions:
                expr_name = namePrefix + expr["name"]
                if settings.contains(expr_name + "/expression"):
                    settings.remove(expr_name)
        settings.endGroup()
        # Remove files - nothing to remove

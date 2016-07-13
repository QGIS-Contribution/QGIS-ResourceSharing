# coding=utf-8
import os
import fnmatch

from PyQt4.QtCore import QSettings
from qgis.core import QgsStyleV2

from symbology_sharing.resource_handler.base import BaseResourceHandler
from symbology_sharing.utilities import local_collection_path
from symbology_sharing.symbol_xml_extractor import SymbolXMLExtractor


class SymbolResourceHandler(BaseResourceHandler):
    """Abstract class of the Symbol handler."""
    IS_DISABLED = False

    def __init__(self, collection_id=None):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        # Init the default style
        self.style = QgsStyleV2.defaultStyle()

    @property
    def dir_name(self):
        return 'symbol'

    def install(self):
        """Install the symbol from this collection into QGIS.

        We create a group with the name of the collection, a child group for
        each xml file and save all the symbols defined that xml file into
        that child group.
        """
        # Call parent method first
        super(SymbolResourceHandler, self).install()

        # Uninstall first in case of reinstalling
        self.uninstall()

        # Create group for this collection
        parent_group_name = '%s (%s)' % (
            self.collection['name'], self.collection_id)
        group_id = self.style.addGroup(parent_group_name)
        # Get all the symbol xml files under resource dirs
        symbol_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.xml'):
                symbol_files.append(file_path)

        for symbol_file in symbol_files:
            file_name = os.path.splitext(os.path.basename(symbol_file))[0]
            child_id = self.style.addGroup(file_name, group_id)
            # Add all symbols and group it
            symbol_xml_extractor = SymbolXMLExtractor(symbol_file)
            for symbol in symbol_xml_extractor.symbols:
                symbol_name = '%s (%s)' % (symbol['name'], self.collection_id)
                if self.style.addSymbol(symbol_name, symbol['symbol'], True):
                    self.style.group(
                        QgsStyleV2.SymbolEntity, symbol_name, child_id)

    def uninstall(self):
        """Uninstall the symbols from QGIS."""
        # Get the parent group id
        parent_group_name = '%s (%s)' % (
            self.collection['name'], self.collection_id)
        parent_group_id = self.style.groupId(parent_group_name)
        child_groups = self.style.childGroupNames(parent_group_name)
        for child_group_id in child_groups:
            # Get all the symbol from this child group and remove them
            symbols = self.style.symbolsOfGroup(
                QgsStyleV2.SymbolEntity, child_group_id)
            for symbol in symbols:
                self.style.removeSymbol(symbol)
            # Remove this child group
            self.style.remove(QgsStyleV2.GroupEntity, child_group_id)
        # Remove parent group:
        self.style.remove(QgsStyleV2.GroupEntity, parent_group_id)


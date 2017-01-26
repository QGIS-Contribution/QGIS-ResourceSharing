# coding=utf-8
import os
import fnmatch

try:
    from qgis.core import QgsStyleV2 as QgsStyle
except ImportError:
    from qgis.core import QgsStyle

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.symbol_xml_extractor import SymbolXMLExtractor
from resource_sharing.resource_handler.symbol_resolver_mixin import \
    SymbolResolverMixin


class SymbolResourceHandler(BaseResourceHandler, SymbolResolverMixin):
    """Concrete class of the Symbol handler."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        # Init the default style
        self.style = QgsStyle.defaultStyle()

    @classmethod
    def dir_name(self):
        return 'symbol'

    def install(self):
        """Install the symbol and collection from this collection into QGIS.

        We create a group with the name of the collection, a child group for
        each xml file and save all the symbols and colorramp defined that xml
        file into that child group.
        """
        # Check if the dir exists, pass installing silently if it doesn't exist
        if not os.path.exists(self.resource_dir):
            return

        # Uninstall first in case of reinstalling
        self.uninstall()

        # Get all the symbol xml files under resource dirs
        symbol_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.xml'):
                symbol_files.append(file_path)

        # If there's no symbol files don't do anything
        if len(symbol_files) == 0:
            return

        parent_group_name = '%s (%s)' % (
            self.collection['name'], self.collection_id)
        group_id = self.style.addGroup(parent_group_name)

        for symbol_file in symbol_files:
            file_name = os.path.splitext(os.path.basename(symbol_file))[0]
            child_id = self.style.addGroup(file_name, group_id)
            # Modify the symbol file first
            self.resolve_dependency(symbol_file)
            # Add all symbols and colorramps and group it
            symbol_xml_extractor = SymbolXMLExtractor(symbol_file)

            for symbol in symbol_xml_extractor.symbols:
                symbol_name = '%s (%s)' % (symbol['name'], self.collection_id)
                # self.resolve_dependency(symbol['symbol'])
                if self.style.addSymbol(symbol_name, symbol['symbol'], True):
                    self.style.group(
                        QgsStyle.SymbolEntity, symbol_name, child_id)

            for colorramp in symbol_xml_extractor.colorramps:
                colorramp_name = '%s (%s)' % (
                    colorramp['name'], self.collection_id)
                if self.style.addColorRamp(
                        colorramp_name, colorramp['colorramp'], True):
                    self.style.group(
                        QgsStyle.ColorrampEntity, colorramp_name, child_id)

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
                QgsStyle.SymbolEntity, child_group_id)
            for symbol in symbols:
                self.style.removeSymbol(symbol)
            # Get all the colorramps and remove them
            colorramps = self.style.symbolsOfGroup(
                QgsStyle.ColorrampEntity, child_group_id)
            for colorramp in colorramps:
                self.style.removeColorRamp(colorramp)

            # Remove this child group
            self.style.remove(QgsStyle.GroupEntity, child_group_id)

        # Remove parent group:
        self.style.remove(QgsStyle.GroupEntity, parent_group_id)

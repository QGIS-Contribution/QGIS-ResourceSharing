# coding=utf-8
import os
import fnmatch

from qgis.core import (
    QgsStyleV2,
    QgsSvgMarkerSymbolLayerV2,
    QgsMarkerLineSymbolLayerV2,
    QgsRasterFillSymbolLayer,
    QgsSVGFillSymbolLayer)

from symbology_sharing.resource_handler.base import BaseResourceHandler
from symbology_sharing.resource_handler.svg_handler import SVGResourceHandler
from symbology_sharing.symbol_xml_extractor import SymbolXMLExtractor
from symbology_sharing.utilities import path_leaf, local_collection_path


class SymbolResourceHandler(BaseResourceHandler):
    """Abstract class of the Symbol handler."""
    IS_DISABLED = False

    def __init__(self, collection_id=None):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        # Init the default style
        self.style = QgsStyleV2.defaultStyle()

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
            # Add all symbols and colorramps and group it
            symbol_xml_extractor = SymbolXMLExtractor(symbol_file)

            for symbol in symbol_xml_extractor.symbols:
                symbol_name = '%s (%s)' % (symbol['name'], self.collection_id)
                self.resolve_dependency(symbol['symbol'])
                if self.style.addSymbol(symbol_name, symbol['symbol'], True):
                    self.style.group(
                        QgsStyleV2.SymbolEntity, symbol_name, child_id)

            for colorramp in symbol_xml_extractor.colorramps:
                colorramp_name = '%s (%s)' % (colorramp['name'], self.collection_id)
                if self.style.addColorRamp(
                        colorramp_name, colorramp['colorramp'], True):
                    self.style.group(
                        QgsStyleV2.ColorrampEntity, colorramp_name, child_id)

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
            # Get all the colorramps and remove them
            colorramps = self.style.symbolsOfGroup(
                QgsStyleV2.ColorrampEntity, child_group_id)
            for colorramp in colorramps:
                self.style.removeColorRamp(colorramp)

            # Remove this child group
            self.style.remove(QgsStyleV2.GroupEntity, child_group_id)

        # Remove parent group:
        self.style.remove(QgsStyleV2.GroupEntity, parent_group_id)

    def resolve_dependency(self, symbol):
        """Update dependency of the symbol.

        We need to update any path dependency of downloaded symbol so that
        the path points to the right path after it's installed.

        For now, we only update the svg/image path to the svg/ directory of
        the collection if the svg exists.

        :param symbol: The symbol
        :type symbol: QgsSymbolV2
        """
        symbol_layers = symbol.symbolLayers()
        for symbol_layer in symbol_layers:
            # SVG Marker
            if isinstance(symbol_layer, QgsSvgMarkerSymbolLayerV2):
                updated_path = self.update_svg_path(symbol_layer.path())
                symbol_layer.setPath(updated_path)
            # Raster fill
            elif isinstance(symbol_layer, QgsRasterFillSymbolLayer):
                updated_path = self.update_svg_path(symbol_layer.imageFilePath())
                symbol_layer.setImageFilePath(updated_path)
            # SVG fill
            elif isinstance(symbol_layer, QgsSVGFillSymbolLayer):
                updated_path = symbol_layer.svgFilePath()
                symbol_layer.setSvgFilePath(updated_path)
            # Marker Line
            elif isinstance(symbol_layer, QgsMarkerLineSymbolLayerV2):
                symbol = symbol_layer.subSymbol()
                self.resolve_dependency(symbol)

    def update_svg_path(self, path):
        """Update symbol's image path to point to the collection svg dir.

        QGIS will already handle intelligently the path. One case if user
        uses the svg from the directory when they create the repository.
        Since it hasn't added in the svg path, it will use abs path,
        so we need to recreate the path.

        :param path: The original path.
        :type path: str
        """
        if not os.path.exists(path):
            filename = path_leaf(path)

            svg_path = os.path.join(
                local_collection_path(self.collection_id),
                SVGResourceHandler.dir_name(),
                filename)
            if os.path.isfile(svg_path):
                return svg_path

            # If not exist either?? :(
            return path

        return path



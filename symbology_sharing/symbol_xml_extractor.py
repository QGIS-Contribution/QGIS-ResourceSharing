# coding=utf-8
import os
import xml.etree.ElementTree as ET

from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QFile, QIODevice, QFileInfo, QUrl, Qt
from qgis.core import QgsSymbolLayerV2Utils

from symbology_sharing.utilities import path_leaf


def fix_xml_node(xml, collection_path, search_paths):
    """
    Loop through the XML nodes to resolve the SVG and image paths
    """
    root = ET.fromstring(xml)
    path_svg_marker_nodes = root.findall(".//layer/prop[@k='name']")
    path_svg_fill_nodes = root.findall(".//layer/prop[@k='svgFile']")
    path_raster_fill_nodes = root.findall(".//layer/prop[@k='imageFile']")
    path_nodes = path_svg_marker_nodes + path_svg_fill_nodes + path_raster_fill_nodes
    for path_node in path_nodes:
        path = resolve_path(path_node.get('v'), collection_path, search_paths)
        path_node.set('v', path)

    return ET.tostring(root)


def resolve_path(path, collection_path, search_paths):
    """
    Try to resolve the SVG and image path
    """
    # It might be a full path
    if QFile(path).exists():
        return QFileInfo(path).canonicalFilePath()

    # It might be a url
    if '://'in path:
        url = QUrl(path)
        if url.isValid() and not url.scheme().isEmpty():
            if url.scheme().compare("file", Qt.CaseInsensitive) == 0:
                # It's a url to local file
                path = url.toLocalFile()
                if QFile(path).exists():
                    return QFileInfo(path).canonicalFilePath()
            else:
                # URL to pointing to online resource
                return path

    # Check in the svg collection path
    file_name = path_leaf(path)
    svg_collection_path = os.path.join(collection_path, 'svg', file_name)
    if QFile(svg_collection_path).exists():
        return QFileInfo(svg_collection_path).canonicalFilePath()

    # Check in the image collection path
    image_collection_path = os.path.join(collection_path, 'image', file_name)
    if QFile(image_collection_path).exists():
        return QFileInfo(image_collection_path).canonicalFilePath()

    # Still not found, check in the search_paths
    for search_path in search_paths:
        local_path = os.path.join(search_path, path)
        if QFile(local_path).exists():
            return QFileInfo(local_path).canonicalFilePath()

    # Can't find any, just return the original path
    return path


class SymbolXMLExtractor(object):
    """A class which parses the given file and returns the symbols and
    colorramps"""
    def __init__(self, xml_path):
        self._xml_path = xml_path
        self._symbols = []
        self._colorramps = []
        # Parse the xml to get the symbols and colorramps
        self.parse_xml()

    def parse_xml(self):
        """Parse the xml file. Returns false if there is failure."""
        xml_file = QFile(self._xml_path)
        if not xml_file.open(QIODevice.ReadOnly):
            return False

        document = QDomDocument()
        if not document.setContent(xml_file):
            return False

        xml_file.close()

        document_element = document.documentElement()
        if document_element.tagName() != 'qgis_style':
            return False

        # Get all the symbols
        self._symbols = []
        symbols_element = document_element.firstChildElement('symbols')
        symbol_element = symbols_element.firstChildElement()
        while not symbol_element.isNull():
            if symbol_element.tagName() == 'symbol':
                symbol = QgsSymbolLayerV2Utils.loadSymbol(symbol_element)
                if symbol:
                    self._symbols.append({
                        'name': symbol_element.attribute('name'),
                        'symbol': symbol
                    })
            symbol_element = symbol_element.nextSiblingElement()

        # Get all the colorramps
        self._colorramps = []
        ramps_element = document_element.firstChildElement('colorramps')
        ramp_element = ramps_element.firstChildElement()
        while not ramp_element.isNull():
            if ramp_element.tagName() == 'colorramp':
                colorramp = QgsSymbolLayerV2Utils.loadColorRamp(ramp_element)
                if colorramp:
                    self._colorramps.append({
                        'name': ramp_element.attribute('name'),
                        'colorramp': colorramp
                    })

            ramp_element = ramp_element.nextSiblingElement()

        return True

    @property
    def symbols(self):
        """Return list of symbols in the xml.

        The structure of the property:
        symbols = [
            {
                'name': str
                'symbol': QgsSymbolV2
            }
        ]
        """
        return self._symbols

    @property
    def colorramps(self):
        """Return list of colorramps in the xml.

        The structure of the property:
        colorramps = [
            {
                'name': str
                'colorramp': QgsVectorColorRampV2
            }
        ]
        """
        return self._colorramps

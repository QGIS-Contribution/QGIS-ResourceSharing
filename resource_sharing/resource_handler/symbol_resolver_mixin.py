# coding=utf-8
import os
import xml.etree.ElementTree as ET

from PyQt4.QtCore import QFileInfo, QUrl, Qt, QFile
from qgis.core import QgsApplication

from resource_sharing.utilities import path_leaf


class SymbolResolverMixin(object):
    """Mixin for Resources Handler that need to resolve image symbol path."""

    def resolve_dependency(self, xml_path):
        """Modify the xml and resolve the resources dependency.

        We need to update any path dependency of downloaded symbol so that
        the path points to the right path after it's installed.

        For now, we only update the svg/image path to the svg/ directory of
        the collection if the svg exists.

        :param xml_path: The path to the style xml file.
        :type xml_path: str
        """
        with open(xml_path, 'r') as xml_file:
            symbol_xml = xml_file.read()

        updated_xml = fix_xml_node(
            symbol_xml, self.collection_path, QgsApplication.svgPaths())

        with open(xml_path, 'w') as xml_file:
            xml_file.write(updated_xml)


def fix_xml_node(xml, collection_path, search_paths):
    """
    Loop through the XML nodes to resolve the SVG and image paths
    """
    root = ET.fromstring(xml)
    svg_marker_nodes = root.findall(".//layer/prop[@k='name']")
    svg_fill_nodes = root.findall(".//layer/prop[@k='svgFile']")
    raster_fill_nodes = root.findall(".//layer/prop[@k='imageFile']")
    path_nodes = svg_marker_nodes + svg_fill_nodes + raster_fill_nodes
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

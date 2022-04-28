import xml.etree.ElementTree as ET
from pathlib import Path

from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QFile, QFileInfo, QUrl

from qgis_resource_sharing.utilities import path_leaf


class SymbolResolverMixin(object):
    """Mixin for Resources Handlers that need to resolve SVG
    and image symbol paths."""

    def resolve_dependency(self, xml_path):
        """Modify the XML and resolve dependencies.

        Update paths to downloaded symbol so that the paths
        point to the right location.

        For now, we only update the svg/image paths to the
        svg directory of the collection if the SVG file exists
        there.

        :param xml_path: The path to the XML style file.
        :type xml_path: str
        """
        with open(xml_path, "rb") as xml_file:
            symbol_xml = xml_file.read()

        updated_xml = fix_xml_node(
            symbol_xml, str(self.collection_path), QgsApplication.svgPaths()
        )

        with open(xml_path, "wb") as xml_file:
            xml_file.write(updated_xml)


def fix_xml_node(xml, collection_path, search_paths):
    """Loop through the XML nodes to resolve the SVG and image paths.

    :param xml: The XML string of the symbol (or full XML symbol definition)
    :type xml: str

    :param collection_path: The downloaded collection's local file
        system path, where we can look for images/SVGs.
    :type collection_path: str

    :param search_paths: List of paths to search for images/SVGs.
    :type search_paths: str
    """
    root = ET.fromstring(xml)
    svg_marker_nodes = root.findall(".//layer/prop[@k='name']")
    svg_fill_nodes = root.findall(".//layer/prop[@k='svgFile']")
    raster_fill_nodes = root.findall(".//layer/prop[@k='imageFile']")
    path_nodes = svg_marker_nodes + svg_fill_nodes + raster_fill_nodes
    for path_node in path_nodes:
        path = resolve_path(path_node.get("v"), collection_path, search_paths)
        path_node.set("v", path)

    return ET.tostring(root)


def resolve_path(path, collection_path, search_paths):
    """Try to resolve the SVG and image paths.

    This is the procedure:
        * It might be a complete local file system path, check if it exists
        * It might be a URL (either local file system or http(s))
        * Check in the 'svg' directory of the collection
        * Check in the 'image' directory of the collection
        * Check in the search_paths

    :param path: The original path.
    :type path: str

    :param collection_path: The local file system path for the collection.
    :type collection_path: str

    :param search_paths: List of paths to search for images/SVGs.
    :type search_paths: str
    """
    # It might be a complete local file system path
    if QFile(path).exists():
        return QFileInfo(path).canonicalFilePath()

    # It might be a URL
    if "://" in path:
        url = QUrl(path)
        if url.isValid() and url.scheme() != "":
            if url.scheme().lower() == "file":
                # It's a url to local file
                path = url.toLocalFile()
                if QFile(path).exists():
                    return QFileInfo(path).canonicalFilePath()
            else:
                # URL pointing to online resource
                return path

    # Check in the 'svg' directory of the collection
    file_name = path_leaf(path)
    svg_collection_path = Path(collection_path, "svg", file_name)
    if QFile(str(svg_collection_path)).exists():
        return QFileInfo(str(svg_collection_path)).canonicalFilePath()

    # Check in the 'image' directory of the collection
    image_collection_path = Path(collection_path, "image", file_name)
    if QFile(str(image_collection_path)).exists():
        return QFileInfo(str(image_collection_path)).canonicalFilePath()

    # Still not found, check the search_paths
    for search_path in search_paths:
        local_path = Path(search_path, path)
        if QFile(str(local_path)).exists():
            return QFileInfo(str(local_path)).canonicalFilePath()

    # Can't find any, just return the original path
    return path

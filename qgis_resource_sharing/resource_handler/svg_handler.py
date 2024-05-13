import logging
import shutil
from pathlib import Path

from qgis.core import Qgis, QgsSettings

from qgis_resource_sharing.__about__ import __title__
from qgis_resource_sharing.resource_handler.base import BaseResourceHandler
from qgis_resource_sharing.utilities import local_collection_path

SVG = "svg"
LOGGER = logging.getLogger(__title__)


class SVGResourceHandler(BaseResourceHandler):
    """The SVG resource handler class."""

    IS_DISABLED = False

    def __init__(self, collection_id):
        """Base class constructor."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def svg_search_paths(cls):
        """Read the SVG paths from settings

        Return the SVG search path as a list"""
        settings = QgsSettings()
        search_paths_settings = settings.value("svg/searchPathsForSVG")
        if not search_paths_settings:
            search_paths = []
        else:
            if Qgis.QGIS_VERSION_INT < 29900:
                # QGIS 2
                search_paths = search_paths_settings.split("|")
            else:
                # QGIS 3
                # Check if it is a string (single directory)
                if isinstance(search_paths_settings, str):
                    search_paths = [search_paths_settings]
                else:
                    # It is a list
                    search_paths = search_paths_settings
        return search_paths

    @classmethod
    def set_svg_search_paths(cls, paths):
        """Write the list of SVG paths to settings"""
        settings = QgsSettings()
        if Qgis.QGIS_VERSION_INT < 29900:
            settings.setValue("svg/searchPathsForSVG", "|".join(paths))
        else:
            if len(paths) == 0:
                settings.remove("svg/searchPathsForSVG")
            else:
                if len(paths) == 1:
                    svgpaths = str(paths[0])
                else:
                    svgpaths = paths
                settings.setValue("svg/searchPathsForSVG", svgpaths)

    @classmethod
    def dir_name(cls):
        return SVG

    def install(self):
        """Install the SVGs from this collection.

        Add the collection root directory path to the SVG search path.
        """
        # Check if the dir exists, pass silently if it doesn't
        if not Path(self.resource_dir).exists():
            return
        # Add to the SVG search paths
        search_paths = self.svg_search_paths()
        if str(local_collection_path()) not in search_paths:
            search_paths.append(str(local_collection_path()))
        self.set_svg_search_paths(search_paths)

        # Count the SVGs
        valid = 0
        for filename in Path(self.resource_dir).rglob("*"):
            if filename.suffix.lower().endswith("svg"):
                valid += 1
        if valid >= 0:
            self.collection[SVG] = valid

    def uninstall(self):
        """Uninstall the SVGs."""
        if not Path(self.resource_dir).exists():
            return
        # Remove from the SVG search paths if there are no SVGs left
        # under local_collection_path.
        # Have to remove now, to be able to update the SVG search path
        shutil.rmtree(self.resource_dir)
        # Check if there are no SVG files in the collections directory
        svgCount = 0
        for filename in local_collection_path().rglob("*"):
            if filename.suffix.lower() == "svg":
                svgCount += 1
                break
        search_paths = self.svg_search_paths()
        if svgCount == 0:
            if str(local_collection_path()) in search_paths:
                search_paths.remove(str(local_collection_path()))
        self.set_svg_search_paths(search_paths)

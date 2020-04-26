# coding=utf-8
#import os
# Use pathlib instead of os.path?
from pathlib import Path
#import fnmatch
import shutil
import logging

from qgis.PyQt.QtCore import QSettings
from qgis.core import QgsSettings
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.utilities import local_collection_path

SVG = 'svg'
LOGGER = logging.getLogger('QGIS Resource Sharing')

class SVGResourceHandler(BaseResourceHandler):
    """The SVG resource handler class."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Base class constructor."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def svg_search_paths(cls):
        """Read the SVG paths from settings"""
        settings = QgsSettings()
        search_paths_str = settings.value('svg/searchPathsForSVG')
        if not search_paths_str:
            search_paths = []
        else:
            if Qgis.QGIS_VERSION_INT < 29900:
                search_paths = search_paths_str.split('|')
            else:
                search_paths = search_paths_str
        return search_paths

    @classmethod
    def set_svg_search_paths(cls, paths):
        """Write the list of SVG paths to settings"""
        # settings = QSettings()
        settings = QgsSettings()
        if Qgis.QGIS_VERSION_INT < 29900:
            settings.setValue('svg/searchPathsForSVG', '|'.join(paths))
        else:
            settings.setValue('svg/searchPathsForSVG', paths)

    @classmethod
    def dir_name(cls):
        return SVG

    def install(self):
        """Install the SVGs from this collection.

        Add the collection root directory path to the SVG search path.
        """
        # Check if the dir exists, pass silently if it doesn't
        #if not os.path.exists(self.resource_dir):
        if not Path(self.resource_dir).exists():
            return
        # Add to the SVG search paths
        search_paths = self.svg_search_paths()

        #if local_collection_path() not in search_paths:
        if str(local_collection_path()) not in search_paths:
            search_paths.append(str(local_collection_path()))
        LOGGER.info('set svg search_paths: ' + search_paths)
        self.set_svg_search_paths(search_paths)

        # Count the SVGs
        valid = 0
        #for dirpath, dirnames, filenames in os.walk(self.resource_dir):
        for filename in Path(self.resource_dir).rglob('*'):
            LOGGER.info('filename: ' + str(filename))
            #for filename in [f for f in filenames if f.lower().endswith(".svg")]:
            if filename.suffix.lower().endswith("svg"):
                valid += 1
        if valid >= 0:
            self.collection[SVG] = valid

    def uninstall(self):
        """Uninstall the SVGs."""
        #if not os.path.exists(self.resource_dir):
        if not Path(self.resource_dir).exists():
            return
        # Remove from the SVG search paths if there are no SVGs left
        # in any collection
        # Have to remove now, to be able to update the SVG search path
        shutil.rmtree(self.resource_dir)
        svgCount = 0
        #for dirpath, dirnames, filenames in os.walk(local_collection_path()):
        #for filename in Path(local_collection_path()).rglob('*'):
        for filename in local_collection_path().rglob('*'):
            #for filename in [f for f in filenames if f.lower().endswith(".svg")]:
            if filename.suffix.lower() == "svg":
                svgCount += 1
                break
        search_paths = self.svg_search_paths()
        if svgCount == 0:
            if str(local_collection_path()) in search_paths:
                search_paths.remove(str(local_collection_path()))
        self.set_svg_search_paths(search_paths)

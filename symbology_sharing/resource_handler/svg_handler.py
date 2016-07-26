# coding=utf-8
import os

from PyQt4.QtCore import QSettings

from symbology_sharing.resource_handler.base import BaseResourceHandler
from symbology_sharing.utilities import local_collection_path


class SVGResourceHandler(BaseResourceHandler):
    """Concrete class of the SVG resource handler."""
    IS_DISABLED = False

    def __init__(self, collection_id=None):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return 'svg'

    def install(self):
        """Install the SVGs from this collection in to QGIS.

        We simply just add the path to the collection root directory to search
        path in QGIS.
        """
        # Check if the dir exists, pass installing silently if it doesn't exist
        if not os.path.exists(self.resource_dir):
            return

        # Add to the search paths for SVG
        settings = QSettings()
        search_paths_str = settings.value('svg/searchPathsForSVG')
        if not search_paths_str:
            search_paths = []
        else:
            search_paths = search_paths_str.split('|')

        if local_collection_path() not in search_paths:
            search_paths.append(local_collection_path())

        settings.setValue('svg/searchPathsForSVG', '|'.join(search_paths))

    def uninstall(self):
        """Uninstall the SVGs from QGIS."""
        # Remove from the searchPaths if the dir empty of collection
        settings = QSettings()
        search_paths_str = settings.value('svg/searchPathsForSVG')
        if not search_paths_str:
            search_paths = []
        else:
            search_paths = search_paths_str.split('|')

        collection_directories = os.listdir(local_collection_path())
        if len(collection_directories) == 0:
            search_paths.remove(local_collection_path())

        settings.setValue('svg/searchPathsForSVG', '|'.join(search_paths))

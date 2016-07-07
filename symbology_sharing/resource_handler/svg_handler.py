# coding=utf-8
from PyQt4.QtCore import QSettings
from qgis.core import QgsApplication

from symbology_sharing.resource_handler.base import BaseResourceHandler


class SVGResourceHandler(BaseResourceHandler):
    """Abstract class of the SVG resource handler."""
    IS_DISABLED = False

    def __init__(self, collection_id=None):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @property
    def dir_name(self):
        return 'svg'

    def install(self):
        """Install the SVGs from this collection in to QGIS.

        We simply just add the path to the SVG of this collection to the SVG
        search path in QGIS.
        """
        # Call parent method first
        super(SVGResourceHandler, self).install()
        # Add to the search paths for SVG
        settings = QSettings()
        search_paths_str = settings.value('svg/searchPathsForSVG')
        if not search_paths_str:
            search_paths = []
        else:
            search_paths = search_paths_str.split('|')
        if self.resource_dir not in search_paths:
            search_paths.append(self.resource_dir)
        settings.setValue('svg/searchPathsForSVG', '|'.join(search_paths))

    def uninstall(self):
        """Uninstall the SVGs from QGIS."""
        # Remove from the searchPaths for SVG
        settings = QSettings()
        search_paths_str = settings.value('svg/searchPathsForSVG')
        if not search_paths_str:
            search_paths = []
        else:
            search_paths = search_paths_str.split('|')
        if self.resource_dir in search_paths:
            search_paths.remove(self.resource_dir)
        settings.setValue('svg/searchPathsForSVG', '|'.join(search_paths))

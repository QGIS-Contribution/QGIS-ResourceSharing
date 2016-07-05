# coding=utf-8
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

        # Add to the default  path
        search_paths = QgsApplication.svgPaths()
        if self.resource_dir not in search_paths:
            search_paths.append(self.resource_dir)
        QgsApplication.setDefaultSvgPaths(search_paths)

    def uninstall(self):
        """Uninstall the SVGs from QGIS."""
        # Remove from the default path
        search_paths = QgsApplication.svgPaths()
        unique_search_paths = list(set(search_paths))
        unique_search_paths.remove(self.resource_dir)
        QgsApplication.setDefaultSvgPaths(unique_search_paths)

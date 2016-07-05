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

        # 1. Add to the default  path
        search_paths = QgsApplication.svgPaths()
        search_paths.append(self.resource_dir)
        QgsApplication.setDefaultSvgPaths(search_paths)

        # # 2. Add to the searchPath
        # setting = QSettings()
        # search_paths = setting.value('svg/searchPathsForSVG').split('|')
        # search_paths.append(self.resource_dir)
        # setting.setValue('svg/searchPathsForSVG', '|'.join(search_paths))

    def uninstall(self):
        """Uninstall the SVGs from QGIS."""
        search_paths = QgsApplication.svgPaths()
        search_paths.remove(self.resource_dir)
        QgsApplication.setDefaultSvgPaths(search_paths)
        # setting = QSettings()
        # setting.setValue('svg/searchPathsForSVG', new_search_paths)


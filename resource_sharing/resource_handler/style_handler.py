# coding=utf-8
import os
import fnmatch
import logging

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.resource_handler.symbol_resolver_mixin import \
    SymbolResolverMixin

LOGGER = logging.getLogger('QGIS Resource Sharing')
STYLE = 'style'

class StyleResourceHandler(BaseResourceHandler, SymbolResolverMixin):
    """Style handler class."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return STYLE

    def install(self):
        """Install the style.

        We just resolve the symbol SVG/image path in the QML file
        """
        # Check if the dir exists, pass installing silently if it doesn't exist
        if not os.path.exists(self.resource_dir):
            return

        # Get all the style xml files under resource dirs
        style_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.qml'):
                style_files.append(file_path)

        # Nothing to do if there are no symbol files
        if len(style_files) == 0:
            return

        valid = 0
        for style_file in style_files:
            # Try to fix image and PNG paths in the QML file
            self.resolve_dependency(style_file)
            valid += 1
        if valid >= 0:
            self.collection[STYLE] = valid

    def uninstall(self):
        """Uninstall the style."""
        # The style is not installed, so do nothing.
        pass

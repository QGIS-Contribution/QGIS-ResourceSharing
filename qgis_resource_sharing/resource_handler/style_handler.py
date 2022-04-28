import logging
from pathlib import Path

from qgis_resource_sharing.resource_handler.base import BaseResourceHandler
from qgis_resource_sharing.resource_handler.symbol_resolver_mixin import (
    SymbolResolverMixin,
)

LOGGER = logging.getLogger("QGIS Resource Sharing")
STYLE = "style"


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
        Resolve the symbol SVG/image paths in the QML files
        """
        # Check if the dir exists, pass silently if it doesn't
        if not Path(self.resource_dir).exists():
            return
        # Get all the collection's layer style QML files located in
        # self.resource_dir
        style_files = []
        for item in Path(self.resource_dir).glob("*.qml"):
            style_files.append(item)
        # Nothing to do if there are no symbol files
        if len(style_files) == 0:
            return
        valid = 0
        for style_file in style_files:
            # Try to fix image and SVG paths in the QML file
            try:
                self.resolve_dependency(str(style_file))
            except Exception as e:
                LOGGER.error(
                    "Could not handle style (QML) file '"
                    + str(style_file)
                    + "':\n"
                    + str(e)
                )
            else:
                valid += 1
        if valid >= 0:
            self.collection[STYLE] = valid

    def uninstall(self):
        """Uninstall the style."""
        # Styles are not installed, so do nothing.
        pass

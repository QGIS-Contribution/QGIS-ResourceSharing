# coding=utf-8
import logging
from pathlib import Path
import shutil
import typing

from qgis.core import (
    QgsApplication,
    QgsMessageLog,
)

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.utilities import get_profile_base_path


CHECKLISTS_FOLDER = 'checklists'
CHECKLISTS = 'checklists'  # Resource Sharing collection subdirectory name
LOGGER = logging.getLogger('QGIS Resource Sharing')


class ChecklistHandler(BaseResourceHandler):
    """Handler for checklists."""
    IS_DISABLED = False
    _GLOB_PATTERN = '*.json'

    @property
    def checklists_directory(self) -> Path:
        return get_profile_base_path() / 'checklists'

    @classmethod
    def dir_name(cls):
        return CHECKLISTS

    def install(self):
        """Install checklists from the collection.

        Copy the checklists in the checklists directory of the Resource
        Sharing collection to the user's checklists directory.

        """

        valid = 0
        for item in self.resource_dir.glob(self._GLOB_PATTERN):
            QgsMessageLog.logMessage(f'Processing file {item!r}...')
            try:
                shutil.copy(item, self.checklists_directory)
                valid += 1
            except OSError as exc:
                LOGGER.error(f"Could not copy checklist {item!r}:\n{str(exc)}")
        if valid > 0:
            self.collection[CHECKLISTS] = valid

    def uninstall(self):
        """Uninstall the collection's checklists."""
        for item in self.resource_dir.glob(self._GLOB_PATTERN):
            checklist_path = Path(self.checklists_directory, item.name)
            if checklist_path.exists():
                checklist_path.unlink()
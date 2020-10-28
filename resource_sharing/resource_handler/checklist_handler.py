import logging
import shutil
from pathlib import Path

from qgis.core import QgsApplication

from resource_sharing.resource_handler.base import BaseResourceHandler

CHECKLISTS_FOLDER = "checklists"
CHECKLISTS = "checklists"  # Resource Sharing collection subdirectory name
LOGGER = logging.getLogger("QGIS Resource Sharing")


class ChecklistHandler(BaseResourceHandler):
    """Handler for checklists."""

    IS_DISABLED = False
    _GLOB_PATTERN = "*.json"

    @property
    def checklists_directory(self) -> Path:
        chkl_path = Path(QgsApplication.qgisSettingsDirPath()) / "checklists/"
        return Path(chkl_path)

    @classmethod
    def dir_name(cls):
        return CHECKLISTS

    def install(self):
        """Install checklists from the collection.

        Copy the checklists in the checklists directory of the Resource
        Sharing collection to the user's checklists directory.
        """

        valid = 0
        self.checklists_directory.mkdir(parents=False, exist_ok=True)
        for item in self.resource_dir.glob(self._GLOB_PATTERN):
            try:
                shutil.copy(item, self.checklists_directory / Path(item).name)
                valid += 1
            except OSError as exc:
                LOGGER.error(f"Could not copy checklist {item!r}:\n{str(exc)}")
        if valid > 0:
            self.collection[CHECKLISTS] = valid

    def uninstall(self):
        """Uninstall the collection's checklists."""
        if self.checklists_directory.exists():
            for item in self.resource_dir.glob(self._GLOB_PATTERN):
                chkl_file = Path(self.checklists_directory, item.name)
                if chkl_file.exists():
                    chkl_file.unlink()
                else:
                    LOGGER.info("Item already removed: " + str(chkl_file))
            # Remove the user's checklist directory, if empty
            # (unlink will not remove a non-empty directory, but raises
            # an exception)
            if not any(self.checklists_directory.iterdir()):
                self.checklists_directory.rmdir()
        else:
            LOGGER.info("No checklist directory")

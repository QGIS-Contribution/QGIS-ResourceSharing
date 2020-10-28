from pathlib import Path
import shutil
import logging

from qgis.core import QgsApplication

# Worth a try? Should probably be present if the Processing R
# Provider plugin is installed.
# from processing_r.processing.utils import RUtils
from processing.tools.system import userFolder, mkdir
from resource_sharing.resource_handler.base import BaseResourceHandler

RSCRIPTS_PROCESSING_FOLDER = "rscripts"  # Processing folder for R scripts
RSCRIPTS_FOLDER = "rscripts"  # Collection subfolder name
LOGGER = logging.getLogger("QGIS Resource Sharing")


class RScriptHandler(BaseResourceHandler):
    """Handler for R script resources."""

    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return RSCRIPTS_FOLDER

    def install(self):
        """Install the R scripts of the collection.

        Copy the collection's R scripts (*.rsx and *.rsx.help) from
        its rscripts directory to the user's R script directory and
        refresh the provider.
        """
        # Check if the dir exists, return silently if it doesn't
        if not Path(self.resource_dir).exists():
            return

        # Handle the R script files located in self.resource_dir
        R_files = []
        for item in Path(self.resource_dir).glob("*"):
            file_path = Path(self.resource_dir, item)
            if file_path.suffix.lower().endswith("rsx"):
                R_files.append(file_path)
            if "".join(file_path.suffixes).lower().endswith("rsx.help"):
                R_files.append(file_path)
        valid = 0
        for R_file in R_files:
            # Install the R script file silently
            try:
                shutil.copy(str(R_file), self.RScripts_folder())
                if R_file.suffix.lower().endswith("rsx"):
                    valid += 1
            except OSError as e:
                LOGGER.error("Could not copy script '" + str(R_file) + "'\n" + str(e))
        if valid > 0:
            self.refresh_Rscript_provider()
            self.collection[RSCRIPTS_FOLDER] = valid

    def uninstall(self):
        """Uninstall the collection's R scripts from the processing toolbox."""
        if not Path(self.resource_dir).exists():
            return
        # Remove the collection's R script files
        for item in Path(self.resource_dir).glob("*"):
            rscript_path = Path(self.RScripts_folder(), item.name)
            if rscript_path.exists():
                rscript_path.unlink()
        self.refresh_Rscript_provider()

    def refresh_Rscript_provider(self):
        """Refresh the R script provider."""
        r_provider = QgsApplication.processingRegistry().providerById("r")
        if r_provider is not None:
            try:
                r_provider.refreshAlgorithms()
            except Exception as err:
                LOGGER.error(
                    "Exception when refreshing after adding" " R scripts:\n" + str(err)
                )

    def default_rscripts_folder(self):
        """Return the default user R scripts folder."""
        # Perphaps better to use RUtils.default_scripts_folder()?
        # return RUtils.default_scripts_folder()
        folder = Path(userFolder(), RSCRIPTS_PROCESSING_FOLDER)
        mkdir(str(folder))
        return str(folder)

    def RScripts_folder(self):
        """Return the default R scripts folder."""
        return self.default_rscripts_folder()

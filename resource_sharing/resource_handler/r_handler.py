# coding=utf-8
import os
import fnmatch
import shutil
from processing.tools.system import userFolder, mkdir

# Worth a try?
#from processing_r.processing.utils import RUtils

from resource_sharing.resource_handler.base import BaseResourceHandler

from qgis.core import QgsApplication, QgsMessageLog, Qgis

R_SCRIPTS_FOLDER = 'R_SCRIPTS_FOLDER'
RSCRIPTS = 'rscripts'

class RScriptHandler(BaseResourceHandler):
    """Handler for R script resources."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return 'rscripts'

    def install(self):
        """Install the R scripts of the collection.

        We copy the R scripts (*.rsx and *.rsx.help) that exist in
        the rscripts dir to the user's R script directory and refresh
        the provider.
        """
        # Check if the dir exists, return silently if it doesn't
        if not os.path.exists(self.resource_dir):
            return

        # Get all the R script files under self.resource_dir
        R_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.rsx'):
                R_files.append(file_path)
            if fnmatch.fnmatch(file_path, '*.rsx.help'):
                R_files.append(file_path)

        valid = 0
        for R_file in R_files:
            # Install the processing file silently
            try:
                shutil.copy(R_file, self.RScripts_folder())
                valid += 1
            except OSError as e:
                QgsMessageLog.logMessage("Could not copy script '{}'\n{}".format(processing_file, str(e)),
                                             "Processing",
                                             Qgis.Warning)

        if valid > 0:
            self.refresh_Rscript_provider()

    def uninstall(self):
        """Uninstall the r scripts from processing toolbox."""
        if not os.path.exists(self.resource_dir):
            return
        # Remove the R script files that are present in this collection
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*%s*' % self.collection_id):
                script_path = os.path.join(self.RScripts_folder(), item)
                if os.path.exists(script_path):
                    os.remove(script_path)

        self.refresh_Rscript_provider()

    def refresh_Rscript_provider(self):
        """Refresh the processing script provider."""
        if QgsApplication.processingRegistry().providerById("r") is not None:
            QgsApplication.processingRegistry().providerById("r").refreshAlgorithms()

    def default_rscripts_folder(self):
        """Return the default R scripts folder."""
        folder = str(os.path.join(userFolder(), RSCRIPTS))
        mkdir(folder)
        return os.path.abspath(folder)

    def RScripts_folder(self):
        """Return the default R scripts folder."""
        # Perphaps better to use RUtils.default_scripts_folder()?
        #return RUtils.default_scripts_folder()
        # Local:
        return self.default_rscripts_folder()


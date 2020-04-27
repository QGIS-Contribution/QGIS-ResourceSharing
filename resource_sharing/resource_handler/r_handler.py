# coding=utf-8
#import os
# Use pathlib instead of os.path?
from pathlib import Path
import fnmatch
import shutil
import logging

from qgis.core import QgsApplication, Qgis
# Worth a try? Should probably be present if the Processing R
# Provider plugin is installed.
# from processing_r.processing.utils import RUtils
from processing.tools.system import userFolder, mkdir
from resource_sharing.resource_handler.base import BaseResourceHandler

RSCRIPTS_PROCESSING_FOLDER = 'rscripts'  # Processing folder for R scripts
RSCRIPTS_FOLDER = 'rscripts'  # Collection subfolder name
LOGGER = logging.getLogger('QGIS Resource Sharing')


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

        We copy the R scripts (*.rsx and *.rsx.help) that exist in
        the rscripts dir to the user's R script directory and refresh
        the provider.
        """
        # Check if the dir exists, return silently if it doesn't
        #if not os.path.exists(self.resource_dir):
        if not Path(self.resource_dir).exists():
            return

        # Get all the R script files under self.resource_dir
        R_files = []
        #for item in os.listdir(self.resource_dir):
        for item in Path(self.resource_dir).glob('*'):
            #file_path = os.path.join(self.resource_dir, item)
            file_path = Path(self.resource_dir, item)
            #if fnmatch.fnmatch(file_path, '*.rsx'):
            if file_path.suffix.lower() == 'rsx':
                R_files.append(file_path)
            #if fnmatch.fnmatch(file_path, '*.rsx.help'):
            if ''.join(file_path.suffixes).lower().endswith('rsx.help'):
                R_files.append(file_path)

        valid = 0
        for R_file in R_files:
            # Install the R script file silently
            try:
                shutil.copy(str(R_file), self.RScripts_folder())
                valid += 1
            except OSError as e:
                LOGGER.error("Could not copy script '" + str(R_file) +
                             "'\n" + str(e))
        if valid > 0:
            self.refresh_Rscript_provider()
            self.collection[RSCRIPTS_FOLDER] = valid

    def uninstall(self):
        """Uninstall the R scripts from processing toolbox."""
        #if not os.path.exists(self.resource_dir):
        if not Path(self.resource_dir).exists():
            return
        # Remove the R script files that are present in this collection
        #for item in os.listdir(self.resource_dir):
        for item in Path(self.resource_dir).glob('*'):
            #file_path = os.path.join(self.resource_dir, item)
            file_path = Path(self.resource_dir, item)
            if fnmatch.fnmatch(str(file_path), '*%s*' % self.collection_id):
                #script_path = os.path.join(self.RScripts_folder(), item)
                script_path = Path(self.RScripts_folder(), item)
                #if os.path.exists(script_path):
                if script_path.exists():
                    #os.remove(script_path)
                    script_path.unlink()
        self.refresh_Rscript_provider()

    def refresh_Rscript_provider(self):
        """Refresh the R script provider."""
        r_provider = QgsApplication.processingRegistry().providerById("r")
        if r_provider is not None:
            r_provider.refreshAlgorithms()

    def default_rscripts_folder(self):
        """Return the default R scripts folder."""
        # Perphaps better to use RUtils.default_scripts_folder()?
        # return RUtils.default_scripts_folder()
        # folder = userFolder() / RSCRIPTS_PROCESSING_FOLDER
        #folder = str(os.path.join(userFolder(), RSCRIPTS_PROCESSING_FOLDER))
        folder = Path(userFolder(), RSCRIPTS_PROCESSING_FOLDER)
        mkdir(str(folder))
        #return os.path.abspath(folder)
        return str(folder)

    def RScripts_folder(self):
        """Return the default R scripts folder."""
        return self.default_rscripts_folder()

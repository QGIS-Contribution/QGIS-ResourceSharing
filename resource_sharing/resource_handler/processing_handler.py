# coding=utf-8
import os
import fnmatch
import shutil
import logging

from processing.script import ScriptUtils
from resource_sharing.resource_handler.base import BaseResourceHandler

from qgis.core import QgsApplication
# from qgis.core import QgsMessageLog, Qgis
LOGGER = logging.getLogger('QGIS Resource Sharing')


class ProcessingScriptHandler(BaseResourceHandler):
    """Concrete class handler for processing script resource."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return 'processing'

    def install(self):
        """Install the processing scripts in the collection.

        We copy the processing scripts exist in the processing dir to the
        user's processing scripts directory and refresh the provider.
        """
        # Check if the dir exists, pass installing silently if it doesn't exist
        if not os.path.exists(self.resource_dir):
            return

        # Get all the script files under self.resource_dir
        processing_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.py'):
                processing_files.append(file_path)

        valid = 0
        for processing_file in processing_files:
            # Install silently the processing file
                try:
                    shutil.copy(processing_file, self.scripts_folder())
                    valid += 1
                except OSError as e:
                    LOGGER.error("Could not copy script '" +
                                 str(processing_file) + "'\n" + str(e))
                    # QgsMessageLog.logMessage("Could not copy script '" +
                    #                          str(processing_file) + "'\n" +
                    #                          str(e), "QGIS Resource Sharing",
                    #                          Qgis.Warning)
        if valid > 0:
            self.refresh_script_provider()

    def uninstall(self):
        """Uninstall the processing scripts from processing toolbox."""
        # Remove the script files containing substring collection_id
        for item in os.listdir(self.scripts_folder()):
            if fnmatch.fnmatch(item, '*%s*' % self.collection_id):
                script_path = os.path.join(self.scripts_folder(), item)
                if os.path.exists(script_path):
                    os.remove(script_path)

        self.refresh_script_provider()

    def refresh_script_provider(self):
        """Refresh the processing script provider."""
        script_pr = QgsApplication.processingRegistry().providerById("script")
        if script_pr is not None:
            script_pr.refreshAlgorithms()

    def scripts_folder(self):
        """Return the default processing scripts folder."""
        return ScriptUtils.defaultScriptsFolder()

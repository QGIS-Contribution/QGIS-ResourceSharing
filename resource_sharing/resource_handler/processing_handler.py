# coding=utf-8
import os
import fnmatch
import shutil
import logging

from processing.script import ScriptUtils
from resource_sharing.resource_handler.base import BaseResourceHandler

from qgis.core import QgsApplication
LOGGER = logging.getLogger('QGIS Resource Sharing')
PROCESSING = 'processing'


class ProcessingScriptHandler(BaseResourceHandler):
    """Concrete class handler for processing script resource."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return PROCESSING

    def install(self):
        """Install the processing scripts of the collection.

        We copy the processing scripts to the user's processing
        scripts directory, and refresh the provider.
        """
        # Pass silently if the directory does not exist
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
            # Install the processing file silently
            try:
                shutil.copy(processing_file, self.scripts_folder())
                valid += 1
            except OSError as e:
                LOGGER.error("Could not copy script '" +
                                 str(processing_file) + "'\n" + str(e))
        if valid > 0:
            self.refresh_script_provider()
            self.collection[PROCESSING] = valid

    def uninstall(self):
        """Uninstall the processing scripts from processing toolbox."""
        # if not Path(self.resource_dir).exists():
        if not os.path.exists(self.resource_dir):
            return
        # Remove the processing script files that are present in this
        # collection
        for item in os.listdir(self.resource_dir):
            # file_path = self.resource_dir / item)
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*%s*' % self.collection_id):
                script_path = os.path.join(self.scripts_folder(), item)
                if os.path.exists(script_path):
                    os.remove(script_path)

        #for item in os.listdir(self.scripts_folder()):
        #    if fnmatch.fnmatch(item, '*%s*' % self.collection_id):
        #        script_path = os.path.join(self.scripts_folder(), item)
        #        if os.path.exists(script_path):
        #            os.remove(script_path)

        self.refresh_script_provider()

    def refresh_script_provider(self):
        """Refresh the processing script provider."""
        script_pr = QgsApplication.processingRegistry().providerById("script")
        if script_pr is not None:
            script_pr.refreshAlgorithms()

    def scripts_folder(self):
        """Return the default processing scripts folder."""
        return ScriptUtils.defaultScriptsFolder()

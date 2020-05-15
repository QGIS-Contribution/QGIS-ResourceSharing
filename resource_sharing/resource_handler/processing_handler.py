# coding=utf-8
# Use pathlib instead of os.path
from pathlib import Path
import shutil
import logging

from processing.script import ScriptUtils
from resource_sharing.resource_handler.base import BaseResourceHandler

from qgis.core import QgsApplication
LOGGER = logging.getLogger('QGIS Resource Sharing')
PROCESSING = 'processing'


class ProcessingScriptHandler(BaseResourceHandler):
    """Handler for processing scripts."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return PROCESSING

    def install(self):
        """Install the collection's processing scripts.

        We copy the processing scripts to the user's processing
        scripts directory, and refresh the provider.
        """
        # Pass silently if the directory does not exist
        if not Path(self.resource_dir).exists():
            return
        # Handle the script files located in self.resource_dir
        processing_files = []
        for item in Path(self.resource_dir).glob('*.py'):
            processing_files.append(item)
        valid = 0
        for processing_file in processing_files:
            # Install the processing file silently
            try:
                shutil.copy(processing_file, self.scripts_folder())
                if processing_file.suffix.lower().endswith('py'):
                    valid += 1
            except OSError as e:
                LOGGER.error("Could not copy script '" +
                                 str(processing_file) + "'\n" + str(e))
        if valid > 0:
            self.refresh_script_provider()
            self.collection[PROCESSING] = valid

    def uninstall(self):
        """Uninstall the processing scripts from the processing toolbox."""
        if not Path(self.resource_dir).exists():
            return
        # Remove the collection's processing script files
        for item in Path(self.resource_dir).glob('*.py'):
            script_path = Path(self.scripts_folder(), item.name)
            if script_path.exists():
                script_path.unlink()
        self.refresh_script_provider()

    def refresh_script_provider(self):
        """Refresh the processing script provider."""
        script_pr = QgsApplication.processingRegistry().providerById("script")
        if script_pr is not None:
            try:
                script_pr.refreshAlgorithms()
            except Error as e:
                LOGGER.error("Exception refreshing algorithms:\n" +
                             str(e))
 
    def scripts_folder(self):
        """Return the default processing scripts folder."""
        return ScriptUtils.defaultScriptsFolder()


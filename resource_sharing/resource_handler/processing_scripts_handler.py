# coding=utf-8
import os
import fnmatch
import shutil

from processing.script import ScriptUtils import

from resource_sharing.resource_handler.base import BaseResourceHandler


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
        user's processing scripts directory (~/.qgis2/processing/scripts) and
        refresh the provider.
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

        for processing_file in processing_files:
            script_file_name = os.path.basename(processing_file)
            script_name = '{} ({}).{}'.format(
                os.path.splitext(script_file_name)[0],
                self.collection_id,
                os.path.splitext(script_file_name)[1],)
            dest_path = os.path.join(self.scripts_folder(), script_name)
            shutil.copy(processing_file, dest_path)

        self.refresh_script_provider()

    def uninstall(self):
        """Uninstall the processing scripts from processing toolbox."""
        # Remove the script files containing substring collection_id
        for item in os.listdir(self.scripts_folder()):
            if fnmatch.fnmatch(item, '*{}*'.format(self.collection_id)):
                script_path = os.path.join(self.scripts_folder(), item)
                if os.path.exists(script_path):
                    os.remove(script_path)

        self.refresh_script_provider()

    def refresh_script_provider(self):
        """Refresh the processing script provider."""
        QgsApplication.processingRegistry().providerById("script")
        provider.refreshAlgorithms()

    def scripts_folder(self):
        """Return the default processing scripts folder."""
        # Copy the script
        return ScriptUtils.defaultScriptsFolder()

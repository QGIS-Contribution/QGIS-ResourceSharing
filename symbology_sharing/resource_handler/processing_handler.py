# coding=utf-8
import os
import fnmatch

from PyQt4.QtCore import QSettings

from processing.script.ScriptAlgorithm import ScriptAlgorithm
from processing.script.WrongScriptException import WrongScriptException
from processing.script.ScriptUtils import ScriptUtils
from processing.core.alglist import algList

from symbology_sharing.resource_handler.base import BaseResourceHandler
from symbology_sharing.utilities import local_collection_path


class ProcessingScriptHandler(BaseResourceHandler):
    """Abstract class handler for processing script resource."""
    IS_DISABLED = False

    def __init__(self, collection_id=None):
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
            # Install silently the processing file
            try:
                script = ScriptAlgorithm(processing_file)
            except WrongScriptException:
                break

            # Copy the script
            dest_path = os.path.join(
                ScriptUtils.scriptsFolder(), os.path.basename(processing_file))
            with open(dest_path, 'w') as f:
                f.write(script.script)
        algList.reloadProvider('script')

    def uninstall(self):
        """Uninstall the processing scripts from processing toolbox."""
        # Get all the script files under self.resource_dir
        processing_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.py'):
                processing_files.append(file_path)

        # Remove them from user's scripts dir
        for processing_file in processing_files:
            script_path = os.path.join(
                ScriptUtils.scriptsFolder(), os.path.basename(processing_file))
            os.remove(script_path)
        algList.reloadProvider('script')

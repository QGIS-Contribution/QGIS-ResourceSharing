# coding=utf-8
import os
# Use pathlib instead of os.path?
# from pathlib import Path
import fnmatch
import shutil
import logging
from processing.tools.system import userFolder, mkdir

from resource_sharing.resource_handler.base import BaseResourceHandler

from qgis.core import QgsApplication

MODELS_PROCESSING_FOLDER = 'models'
MODELS = 'models'  # Resource Sharing collection subdirectory name
LOGGER = logging.getLogger('QGIS Resource Sharing')


class ModelHandler(BaseResourceHandler):
    """Handler for model resources."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return MODELS

    def install(self):
        """Install the models from the collection.

        Copy the models (*.model3) in the models directory of the
        Resource Sharing collection to the user's processing
        model directory and refresh the provider.
        """
        # Check if the dir exists, return silently if it doesn't
        # if Path(self.resource_dir).exists():
        if not os.path.exists(self.resource_dir):
            return

        # Get all the model files under self.resource_dir
        model_files = []
        for item in os.listdir(self.resource_dir):
            # file_path = self.resource_dir / item)
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.model3'):
                model_files.append(file_path)
        valid = 0
        for model_file in model_files:
            # Install the model file silently
            try:
                shutil.copy(model_file, self.Models_folder())
                valid += 1
            except OSError as e:
                LOGGER.error("Could not copy model '" +
                             str(model_file) + "':\n" + str(e))
        if valid > 0:
            self.refresh_Model_provider()

    def uninstall(self):
        """Uninstall the models from processing toolbox."""
        # if not Path(self.resource_dir).exists():
        if not os.path.exists(self.resource_dir):
            return
        # Remove the model files that are present in this collection
        for item in os.listdir(self.resource_dir):
            # file_path = self.resource_dir / item)
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*%s*' % self.collection_id):
                model_path = os.path.join(self.Models_folder(), item)
                if os.path.exists(model_path):
                    os.remove(model_path)

        self.refresh_Model_provider()

    def refresh_Model_provider(self):
        """Refresh the processing model provider."""
        mod_prov = QgsApplication.processingRegistry().providerById("model")
        if (mod_prov is not None):
            mod_prov.refreshAlgorithms()

    def default_models_folder(self):
        """Return the default location of the processing models folder."""
        # folder = userFolder() / MODELS_PROCESSING_FOLDER
        folder = str(os.path.join(userFolder(), MODELS_PROCESSING_FOLDER))
        mkdir(folder)
        # return folder.absolute()
        return os.path.abspath(folder)

    def Models_folder(self):
        """Return the folder where processing expects to find models."""
        # Use the default location
        return self.default_models_folder()

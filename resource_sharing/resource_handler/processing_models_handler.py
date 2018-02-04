# coding=utf-8
import os
import fnmatch
import shutil

from processing.modeler.ModelerUtils import ModelerUtils

from resource_sharing.resource_handler.base import BaseResourceHandler


class ProcessingModelsHandler(BaseResourceHandler):
    """Concrete class handler for processing models resource."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)

    @classmethod
    def dir_name(cls):
        return 'processing'

    def install(self):
        """Install the processing models in the collection.

        We copy the processing models exist in the processing dir to the
        user's processing models directory (~/.qgis2/processing/models) and
        refresh the provider.
        """
        # Check if the dir exists, pass installing silently if it doesn't exist
        if not os.path.exists(self.resource_dir):
            return

        # Get all the models files under self.resource_dir
        processing_files = []
        for item in os.listdir(self.resource_dir):
            file_path = os.path.join(self.resource_dir, item)
            if fnmatch.fnmatch(file_path, '*.model'):
                processing_files.append(file_path)

        for processing_file in processing_files:
            model_file_name = os.path.basename(processing_file)
            model_name = '{} ({}).{}'.format(
                os.path.splitext(model_file_name)[0],
                self.collection_id,
                os.path.splitext(model_file_name)[1],)
            dest_path = os.path.join(self.models_folder(), model_name)
            shutil.copy(processing_file, dest_path)

        self.refresh_models_provider()

    def uninstall(self):
        """Uninstall the processing models from processing toolbox."""
        # Remove the models files containing substring collection_id
        for item in os.listdir(self.models_folder()):
            if fnmatch.fnmatch(item, '*{}*'.format(self.collection_id)):
                model_path = os.path.join(self.models_folder(), item)
                if os.path.exists(model_path):
                    os.remove(model_path)

        self.refresh_model_provider()

    def refresh_model_provider(self):
        """Refresh the processing models provider."""
        QgsApplication.processingRegistry().providerById("model")
        provider.refreshAlgorithms()

    def models_folder(self):
        """Return the default processing models folder."""
        return ModelerUtils.defaultModelsFolder()

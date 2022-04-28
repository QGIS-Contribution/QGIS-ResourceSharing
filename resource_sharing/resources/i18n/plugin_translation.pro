FORMS = ../../gui/ui/download_dialog.ui \
        ../../gui/ui/manage_repository.ui \
        ../../gui/ui/resource_sharing_dialog_base.ui \

SOURCES=\
    # root
    ../../collection_manager.py \
    ../../config.py \
    ../../custom_logging.py \
    ../../exception.py \
    ../../network_manager.py \
    ../../plugin.py \
    ../../repository_manager.py \
    ../../symbol_xml_extractor.py \
    ../../utilities.py \
    ../../version_compare.py \
    # gui
    ../../gui/custom_sort_filter_proxy.py \
    ../../gui/manage_dialog.py \
    ../../gui/resource_sharing_dialog.py \
    # repository handler
    ../../repository_handler/base.py \
    ../../repository_handler/bitbucket_handler.py \
    ../../repository_handler/filesystem_handler.py \
    ../../repository_handler/github_handler.py \
    ../../repository_handler/gitlab_handler.py \
    ../../repository_handler/gogs_handler.py \
    ../../repository_handler/remote_git_handler.py \
    ../../repository_handler/remote_zip_handler.py \
    # resource handler
    ../../resource_handler/base.py \
    ../../resource_handler/checklist_handler.py \
    ../../resource_handler/expression_handler.py \
    ../../resource_handler/model_handler.py \
    ../../resource_handler/processing_handler.py \
    ../../resource_handler/r_handler.py \
    ../../resource_handler/style_handler.py \
    ../../resource_handler/symbol_handler.py \
    ../../resource_handler/symbol_resolver_mixin.py

TRANSLATIONS = qgis_resource_sharing_fr.ts

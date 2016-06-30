# coding=utf-8
import os

from qgis.core import QgsApplication


def resources_path(*args):
    """Get the absolute path to resources in the resources dir.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: list

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(path, 'resources'))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


def ui_path(*args):
    """Get the absolute path to the ui file from the UI dir.

    :param args List of path elements e.g. ['manage_repository.ui]
    :type args: list

    :return: Absolute path to the ui file.
    :rtype: str
    """
    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, 'gui', 'ui'))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


def repo_settings_group():
    """Get the settings group for Symbology Sharing Dialog."""
    return '/SymbologySharing/repository'


def collection_cache_path():
    """Get the path to the collection cache."""
    return os.path.join(
        QgsApplication.qgisSettingsDirPath(),
        'symbology_sharing',
        'collections_cache')


def local_collection_path(id=None):
    """Get the path to the local collection dir.

    If id is not passed, it will just return the root dir of the collections.
    """
    path = os.path.join(
        QgsApplication.qgisSettingsDirPath(),
        'symbology_sharing',
        'collections')
    if id:
        path = os.path.join(path, id)
    return path

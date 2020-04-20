# coding=utf-8
import os
# Use pathlib instead of os.path?
# from pathlib import Path
import logging

import ntpath
from ext_libs.pathvalidate import sanitize_filename

from qgis.PyQt.QtCore import QDir, QSettings
from qgis.core import QgsSettings
try:
    from qgis.core import QgsApplication, QGis as Qgis
except ImportError:
    from qgis.core import QgsApplication, Qgis

from resource_sharing import config
import jinja2

LOGGER = logging.getLogger('QGIS Resource Sharing')


def resources_path(*args):
    """Get the absolute path to resources in the resources dir.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: list

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    # path = Path(os.path.dirname(__file__))
    path = os.path.dirname(os.path.dirname(__file__))
    # path = (path / 'resources').absolute
    path = os.path.abspath(os.path.join(path, 'resources'))
    for item in args:
        # path = (path / item).absolute
        path = os.path.abspath(os.path.join(path, item))

    return path


def ui_path(*args):
    """Get the absolute path to the ui file from the UI dir.

    :param args List of path elements e.g. ['manage_repository.ui]
    :type args: list

    :return: Absolute path to the ui file.
    :rtype: str
    """
    # path = Path(os.path.dirname(__file__))
    path = os.path.dirname(__file__)
    # path = (path / 'gui' / 'ui').absolute
    path = os.path.abspath(os.path.join(path, 'gui', 'ui'))
    for item in args:
        # path = (path / item).absolute
        path = os.path.abspath(os.path.join(path, item))

    return path


def repo_settings_group():
    """Get the settings group for Resource Sharing Dialog."""
    return '/ResourceSharing/repository'


def resource_sharing_group():
    """Get the settings group for the local collection directories."""
    return '/ResourceSharing'


def repositories_cache_path():
    """Get the path to the repositories cache."""
    # return Path(QgsApplication.qgisSettingsDirPath()) /
    #             'resource_sharing' / 'repositories_cache'
    return os.path.join(
        QgsApplication.qgisSettingsDirPath(),
        'resource_sharing',
        'repositories_cache')


def local_collection_root_dir_key():
    """The QSettings key for the local collections root dir."""
    return 'localCollectionDir'


def default_local_collection_root_dir():
    return os.path.join(QgsApplication.qgisSettingsDirPath(),
                        'resource_sharing',
                        'collections')


def local_collection_path(id=None):
    """Get the path to the local collection dir.

    If id is not passed, it will just return the root dir of the
    collections.
    """
    settings = QgsSettings()
    settings.beginGroup(resource_sharing_group())
    if settings.contains(local_collection_root_dir_key()):
        # The path is defined in the settings - use it
        path = settings.value(local_collection_root_dir_key())
    else:
        # The path is not defined in the settings
        if os.path.exists(old_local_collection_path()):
            # The pre-version 0.10 directory exists - so use it
            path = old_local_collection_path()
        else:
            # Use the new default directory
            path = default_local_collection_root_dir()
        LOGGER.info('Setting the collection path to ' + path)
        settings.setValue(local_collection_root_dir_key(),
                          path)
    settings.endGroup()
    # If the directory does not exist, create it!
    if not os.path.exists(path):
        LOGGER.debug('coll_mgr - creating local collection dir: ' +
                     str(path))
        os.makedirs(path)

    # # path = Path(QDir.homePath()) / 'QGIS' / 'Resource Sharing')
    # path = os.path.join(
    #     QDir.toNativeSeparators(QDir.homePath()),
    #     'QGIS',
    #     'Resource Sharing')
    if id:
        collection_name = config.COLLECTIONS[id]['name']
        sane_name = sanitize_filename(collection_name)

        dir_name = '%s-%s' % (sane_name, id)
        # dir_name = '%s (%s)' % (collection_name, id)
        # dir_name = '%s' % (id)
        # path = path / dir_name
        path = os.path.join(path, dir_name)
        # Check if the "old" directory name exists
        old_dir_name = '%s' % (id)
        old_path = os.path.join(path, old_dir_name)
        if os.path.exists(old_path):
            try:
                os.rename(old_path, path)
            except:
                #
    return path


def old_local_collection_path(id=None):
    """Get the path to the old local collection dir.
    (in case we would like to help the users migrate)
    If id is not passed, it will just return the root dir of the
    collections.
    """
    path = os.path.join(
        QDir.homePath(),
        'QGIS',
        'Resource Sharing')
    if id:
        collection_name = config.COLLECTIONS[id]['name']
        dir_name = '%s (%s)' % (collection_name, id)
        path = os.path.join(path, dir_name)
    return path


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def qgis_version():
    """Get the version of QGIS.

    :returns: QGIS Version where 30400 represents QGIS 3.4 etc.
    :rtype: int
    """
    version = unicode(Qgis.QGIS_VERSION_INT)
    version = int(version)
    return version


def render_template(filename, context):
    """Render a template with the specified filename.
    :param filename: The filename (must be in the template directory)
    :type filename: str

    :param context: The context passed for the template
    :type context: dict
    """
    path = os.path.dirname(__file__)
    # path = path / os.pardir / 'resources' / 'template').absolute()
    path = os.path.abspath(
        os.path.join(path, os.pardir, 'resources', 'template'))
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)

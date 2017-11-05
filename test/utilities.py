# coding=utf-8
import os
import sys
import logging

from PyQt4.QtCore import QUrl

LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
IFACE = None
PARENT = None


def get_qgis_app():
    """ Start one QGIS application to test against.
    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)
    If QGIS is already running the handle to that app will be returned.
    """

    try:
        from PyQt4 import QtGui, QtCore
        from qgis.core import QgsApplication
        from qgis.gui import QgsMapCanvas
        from qgis_interface import QgisInterface
    except ImportError:
        return None, None, None, None

    global QGIS_APP  # pylint: disable=W0603

    if QGIS_APP is None:
        gui_flag = True  # All test will run qgis in gui mode
        # noinspection PyPep8Naming
        QGIS_APP = QgsApplication(sys.argv, gui_flag)
        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)

    global PARENT  # pylint: disable=W0603
    if PARENT is None:
        PARENT = QtGui.QWidget()

    global CANVAS  # pylint: disable=W0603
    if CANVAS is None:
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(800, 600))

    global IFACE  # pylint: disable=W0603
    if IFACE is None:
        # QgisInterface is a stub implementation of the QGIS plugin interface
        # noinspection PyPep8Naming
        IFACE = QgisInterface(CANVAS)

    return QGIS_APP, CANVAS, IFACE, PARENT

def test_data_path(*args):
    """Return the absolute path to the plugin test data or directory path.

    :param args: List of path e.g. ['control', 'files',
        'test-error-message.txt'] or ['control', 'scenarios'] to get the path
        to scenarios dir.
    :type args: list

    :return: Absolute path to the test data or dir path.
    :rtype: str

    """
    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, 'data'))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


def test_repository_url():
    """Return the test repository URL on file system.

    :return: The test repository URL string
    :rtype: str
    """
    return QUrl.fromLocalFile(test_data_path()).toString()

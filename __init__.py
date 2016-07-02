# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsSymbologySharing
                                 A QGIS plugin
 Download colllections shared by other users
                             -------------------
        begin                : 2016-05-29
        copyright            : (C) 2016 by Akbar Gumbira
        email                : akbargumbira@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

import sys
import copy
import os

from qgis.core import QgsApplication

# Dulwich tries to call sys.argv while in QGIS, argv module is missing
if not hasattr(sys, 'argv'):
    sys.argv = QgsApplication.instance().argv()

sys.path.append(os.path.dirname(__file__))

PLUGIN_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__)))
if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)

EXT_LIBS_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, 'ext_libs'))
if EXT_LIBS_DIR not in sys.path:
    sys.path.append(EXT_LIBS_DIR)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QgsSymbologySharing class from file QgsSymbologySharing.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from symbology_sharing.plugin import Plugin
    return Plugin(iface)

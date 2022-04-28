"""
/***************************************************************************
 QGIS Resource Sharing - A QGIS plugin
 Download collections shared by other users
                           -------------------
        begin              : 2016-05-29
        copyright          : (C) 2016 by Akbar Gumbira, 2020 by Håvard Tveite
        email              : havard.tveite@nmbu.no
        git sha            : $Format:%H$
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

import os
import sys

# Dulwich tries to call sys.argv, but the argv module is missing in QGIS
if not hasattr(sys, "argv"):
    sys.argv = []

sys.path.append(os.path.dirname(__file__))

PLUGIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)

EXT_LIBS_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, "ext_libs"))
if EXT_LIBS_DIR not in sys.path:
    sys.path.append(EXT_LIBS_DIR)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load the Plugin class from the plugin.py file.
       And set up the logger

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from resource_sharing.custom_logging import setup_logger

    setup_logger()

    from resource_sharing.plugin import ResourceSharingPlugin

    return ResourceSharingPlugin(iface)

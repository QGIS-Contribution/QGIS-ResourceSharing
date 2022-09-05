"""
    Test plugin initialization
"""

from qgis_resource_sharing import classFactory


def test_plugin_init(qgis_iface):
    """Just testing if clicking on the toolbar buttons does not crash

    :param qgis_iface:
    """
    plugin = classFactory(qgis_iface)
    plugin.initGui()

"""
/***************************************************************************
                                 A QGIS plugin
 Download collections shared by other users
                              -------------------
        begin                : 2016-05-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Akbar Gumbira
        email                : akbargumbira@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# standard
from pathlib import Path

# PyQGIS
from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# package
from resource_sharing.__about__ import DIR_PLUGIN_ROOT, __icon_path__
from resource_sharing.gui.resource_sharing_dialog import ResourceSharingDialog


class ResourceSharingPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to
            this class, providing the hook to manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save the reference to the QGIS interface
        self.iface = iface

        # initialize the locale
        locale: str = QgsSettings().value("locale/userLocale", QLocale().name())[0:2]
        locale_path: Path = (
            DIR_PLUGIN_ROOT / f"resources/i18n/qgis_resource_sharing_{locale}.qm"
        )

        if locale_path.exists():
            self.translator = QTranslator()
            self.translator.load(str(locale_path.resolve()))
            QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ResourceSharingDialog()

        # Declare instance attributes
        self.actions = []
        self.menuName = self.tr("&Resource Sharing")
        # TODO: We may let the user set this up
        self.toolbar = self.iface.addToolBar(self.menuName)
        self.toolbar.setObjectName("Resource Sharing")

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using the Qt translation
        API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("QgsResourceSharing", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            if hasattr(self.iface, "addPluginToWebMenu"):
                self.iface.addPluginToWebMenu("", action)
            # We'll also keep it in the Plugin menu for the time being...
            # else:
            #     self.iface.addPluginToMenu(self.menuName, action)
            self.iface.addPluginToMenu(self.menuName, action)
        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.add_action(
            icon_path=str(__icon_path__.resolve()),
            text=self.tr("Resource Sharing"),
            callback=self.run,
            parent=self.iface.mainWindow(),
            add_to_toolbar=True,
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            if hasattr(self.iface, "removePluginWebMenu"):
                self.iface.removePluginWebMenu("", action)
            # We'll also keep it in the Plugin menu for the time being...
            # else:
            #    self.iface.removePluginMenu(self.menuName, action)
            self.iface.removePluginMenu(self.menuName, action)

            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        self.toolbar.parentWidget().removeToolBar(self.toolbar)

    def run(self):
        """Performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

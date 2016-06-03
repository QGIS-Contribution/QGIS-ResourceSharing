# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsSymbologySharingDialog
                                 A QGIS plugin
 Download colllections shared by other users
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

from PyQt4 import QtGui, uic

from PyQt4.Qt import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QListWidgetItem

from manage_dialog import ManageRepositoryDialog
from ..utilities import resources_path, ui_path

FORM_CLASS, _ = uic.loadUiType(ui_path('qgs_symbology_sharing_dialog_base.ui'))


class QgsSymbologySharingDialog(QtGui.QDialog, FORM_CLASS):
    TAB_ALL = 0
    TAB_INSTALLED = 1
    TAB_SETTINGS = 2

    def __init__(self, parent=None, iface=None):
        """Constructor.

        :param parent: Optional widget to use as parent
        :type parent: QWidget

        :param iface: An instance of QGisInterface
        :type iface: QGisInterface
        """
        super(QgsSymbologySharingDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        # Mock plugin manager dialog
        self.resize(796, 594)
        self.setMinimumSize(QSize(790, 0))
        self.setModal(True)

        # Set QListWidgetItem
        # All
        icon_all = QIcon()
        icon_all.addFile(
            resources_path('img', 'plugin.svg'),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_all = QListWidgetItem()
        item_all.setIcon(icon_all)
        item_all.setText(self.tr('All'))

        # Installed
        icon_installed = QIcon()
        icon_installed.addFile(
            resources_path('img', 'plugin-installed.svg'),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_installed = QListWidgetItem()
        item_installed.setIcon(icon_installed)
        item_installed.setText(self.tr('Installed'))
        item_all.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # Settings
        icon_settings = QIcon()
        icon_settings.addFile(
            resources_path('img', 'settings.svg'),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_settings = QListWidgetItem()
        item_settings.setIcon(icon_settings)
        item_settings.setText(self.tr('Settings'))
        item_all.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # Add the list widget item to the widget
        self.menu_list_widget.addItem(item_all)
        self.menu_list_widget.addItem(item_installed)
        self.menu_list_widget.addItem(item_settings)

        # Connect list widget to stack widget
        self.menu_list_widget.currentRowChanged.connect(self.set_current_tab)

        # Slots
        self.button_add.clicked.connect(self.add_repository)
        self.button_edit.clicked.connect(self.edit_repository)

    def set_current_tab(self, index):
        """Set stacked widget based on active tab.

        :param index: The index of the active list widget item.
        :type index: int
        """
        if index == (self.menu_list_widget.count() - 1):
            # Switch to settings tab
            self.stacked_menu_widget.setCurrentIndex(1)
        else:
            # Switch to plugins tab
            self.stacked_menu_widget.setCurrentIndex(0)

    def add_repository(self):
        """Open add repository dialog."""
        dlg = ManageRepositoryDialog(self)
        if not dlg.exec_():
            return

    def edit_repository(self):
        """Open edit repository dialog."""
        dlg = ManageRepositoryDialog(self   )
        if not dlg.exec_():
            return



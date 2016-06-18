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
from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import (
    QIcon,
    QListWidgetItem,
    QTreeWidgetItem,
    QSizePolicy,
    QMessageBox,
    QProgressDialog
)
from qgis.gui import QgsMessageBar

from manage_dialog import ManageRepositoryDialog
from ..repository_manager import RepositoryManager
from ..utilities import resources_path, ui_path, repo_settings_group

FORM_CLASS, _ = uic.loadUiType(ui_path('qgs_symbology_sharing_dialog_base.ui'))


class SymbologySharingDialog(QtGui.QDialog, FORM_CLASS):
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
        super(SymbologySharingDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.repository_manager = RepositoryManager()

        # Init the message bar
        self.message_bar = QgsMessageBar(self)
        self.message_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vlayoutRightColumn.insertWidget(0, self.message_bar)

        # Mock plugin manager dialog
        self.resize(796, 594)
        self.setMinimumSize(QSize(790, 0))
        self.setModal(True)
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)

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

        # Slots
        self.button_add.clicked.connect(self.add_repository)
        self.button_edit.clicked.connect(self.edit_repository)
        self.button_delete.clicked.connect(self.delete_repository)
        self.menu_list_widget.currentRowChanged.connect(self.set_current_tab)

        # Creating progress dialog for downloading stuffs
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setAutoClose(False)
        title = self.tr('Symbology Sharing')
        self.progress_dialog.setWindowTitle(title)

        # Populate tree repositories with registered repositories
        self.populate_tree_repositories()

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

        for repo in self.repository_manager.repositories.values():
            if dlg.line_edit_url.text().strip() == repo['url']:
                self.message_bar.pushMessage(
                    self.tr(
                        'Unable to add another repository with the same URL!'),
                    QgsMessageBar.CRITICAL, 5)
                return

        repo_name = dlg.line_edit_name.text()
        repo_url = dlg.line_edit_url.text().strip()
        if repo_name in self.repository_manager.repositories:
            repo_name += '(2)'

        settings = QSettings()
        settings.beginGroup(repo_settings_group())

        # Fetch metadata
        if self.progress_dialog is not None:
            self.progress_dialog.show()
            # Just use infinite progress bar here
            self.progress_dialog.setMaximum(0)
            self.progress_dialog.setMinimum(0)
            self.progress_dialog.setValue(0)
            self.progress_dialog.setLabelText("Fetching repository's metadata")

        try:
            status, description = self.repository_manager.fetch_metadata(repo_url)
            if status:
                # TODO: Process this instead of showing it on message box :)
                # QMessageBox.information(
                #     self,
                #     self.tr("Test"),
                #     author)
                # Add the repo
                settings.setValue(repo_name + '/url', repo_url)
            else:
                self.message_bar.pushMessage(
                    self.tr(
                        'Unable to add repository: %s') % description,
                    QgsMessageBar.CRITICAL, 5)
        except Exception, e:
            self.message_bar.pushMessage(
                self.tr('%s') % e,
                QgsMessageBar.CRITICAL, 5)
        finally:
            self.progress_dialog.hide()

        # Refresh tree repository
        self.refresh_tree_repositories()
        self.set_enabled_edit_delete_button(False)

    def edit_repository(self):
        """Open edit repository dialog."""
        selected_item = self.tree_repositories.currentItem()
        if selected_item:
            repo_name = selected_item.text(0)

        if not repo_name:
            return

        dlg = ManageRepositoryDialog(self)
        dlg.line_edit_name.setText(repo_name)
        dlg.line_edit_url.setText(
            self.repository_manager.repositories[repo_name]['url'])

        if not dlg.exec_():
            return

        # Check if the changed URL is already there in the repo
        new_url = dlg.line_edit_url.text().strip()
        old_url = self.repository_manager.repositories[repo_name]['url']
        for repo in self.repository_manager.repositories.values():
            if new_url == repo['url'] and (old_url != new_url):
                self.message_bar.pushMessage(
                    self.tr(
                        'Unable to add another repository with the same URL!'),
                    QgsMessageBar.CRITICAL, 5)
                return

        # Delete old repo and create a new entry
        settings = QSettings()
        settings.beginGroup(repo_settings_group())
        settings.remove(repo_name)
        new_name = dlg.line_edit_name.text()
        if new_name in self.repository_manager.repositories and new_name != repo_name:
            new_name += '(2)'
        settings.setValue(new_name + '/url', new_url)

        # Refresh tree repository
        self.refresh_tree_repositories()
        self.set_enabled_edit_delete_button(False)

    def delete_repository(self):
        """Delete a repository in the tree widget."""
        selected_item = self.tree_repositories.currentItem()
        if selected_item:
            repo_name = selected_item.text(0)

        if not repo_name:
            return
        # Check if it's the official repository
        settings = QSettings()
        settings.beginGroup(repo_settings_group())
        if settings.value(repo_name + '/url') == self.repository_manager.OFFICIAL_REPO[1]:
            self.message_bar.pushMessage(
                self.tr(
                    'You can not remove the official repository!'),
                QgsMessageBar.WARNING, 5)
            return

        warning = self.tr('Are you sure you want to remove the following '
                          'repository?') + '\n' + repo_name
        if QMessageBox.warning(
                self,
                self.tr("QGIS Symbology Sharing"),
                warning,
                QMessageBox.Yes,
                QMessageBox.No) == QMessageBox.No:
            return

        settings.remove(repo_name)

        # Refresh tree repository
        self.refresh_tree_repositories()
        self.set_enabled_edit_delete_button(False)

    def refresh_tree_repositories(self):
        """Refresh tree repositories using new repositories data."""
        self.repository_manager.load()
        self.populate_tree_repositories()

    def populate_tree_repositories(self):
        """Populate dictionary repositories to the tree widget."""
        # Clear the current tree widget
        self.tree_repositories.clear()

        # Export the updated ones from the repository manager
        for repo_name in self.repository_manager.repositories:
            url = self.repository_manager.repositories[repo_name]['url']
            item = QTreeWidgetItem(self.tree_repositories)
            item.setText(0, repo_name)
            item.setText(1, url)
        self.tree_repositories.resizeColumnToContents(0)
        self.tree_repositories.resizeColumnToContents(1)
        self.tree_repositories.sortItems(1, Qt.AscendingOrder)

    def on_tree_repositories_itemSelectionChanged(self):
        """Slot for when the itemSelectionChanged signal emitted."""
        # Activate edit and delete button
        self.set_enabled_edit_delete_button(True)

    def set_enabled_edit_delete_button(self, is_enabled):
        """Disable edit and delete button.

        :param is_enabled: Boolean is enabled or not.
        :type is_enabled: bool
        """
        self.button_edit.setEnabled(is_enabled)
        self.button_delete.setEnabled(is_enabled)

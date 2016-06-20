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
    QProgressDialog,
    QStandardItemModel,
    QStandardItem
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

        # Creating progress dialog for downloading stuffs
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setAutoClose(False)
        title = self.tr('Symbology Sharing')
        self.progress_dialog.setWindowTitle(title)

        # Init repository manager
        self.repository_manager = RepositoryManager()
        # Collections list view
        self.collections_model = QStandardItemModel(0, 1)
        self.list_view_collections.setModel(self.collections_model)

        # Slots
        self.button_add.clicked.connect(self.add_repository)
        self.button_edit.clicked.connect(self.edit_repository)
        self.button_delete.clicked.connect(self.delete_repository)
        self.menu_list_widget.currentRowChanged.connect(self.set_current_tab)
        self.list_view_collections.selectionModel().currentChanged.connect(
            self.on_list_view_collections_clicked)

        # Populate repositories widget and collections list view
        self.populate_repositories_widget()
        self.reload_collections_model()

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

        # Show progress dialog
        self.show_progress_dialog("Fetching repository's metadata")

        # Add repository
        try:
            status, description = self.repository_manager.add_repository(
                repo_name, repo_url)
            if status:
                self.message_bar.pushMessage(
                    self.tr(
                        'Repository is sucessfully added'),
                    QgsMessageBar.SUCCESS, 5)
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

        # Reload data and widget
        self.reload_data_and_widget()

        # Deactivate edit and delete button
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)

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

        new_name = dlg.line_edit_name.text()
        if new_name in self.repository_manager.repositories and new_name != repo_name:
            new_name += '(2)'

        # Show progress dialog
        self.show_progress_dialog("Fetching repository's metadata")

        # Edit repository
        try:
            status, description = self.repository_manager.edit_repository(
                repo_name, new_name, new_url)
            if status:
                self.message_bar.pushMessage(
                    self.tr(
                        'Repository is sucessfully updated'),
                    QgsMessageBar.SUCCESS, 5)
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

        # Reload data and widget
        self.reload_data_and_widget()

        # Deactivate edit and delete button
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)

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

        # Remove repository
        self.repository_manager.remove_repository(repo_name)

        # Reload data and widget
        self.reload_data_and_widget()

        # Deactivate edit and delete button
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)

    def reload_data_and_widget(self):
        """Reload repositories and collections and update widgets related."""
        self.reload_repositories_widget()
        self.reload_collections_model()

    def reload_repositories_widget(self):
        """Refresh tree repositories using new repositories data."""
        self.repository_manager.load()
        self.populate_repositories_widget()

    def populate_repositories_widget(self):
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

    def reload_collections_model(self):
        """Reload collections model with new collections object."""
        self.collections_model.clear()
        for id in self.repository_manager.collections:
            collection_name = self.repository_manager.collections[id]['name']
            item = QStandardItem(collection_name)
            item.setEditable(False)
            item.setData(id)
            self.collections_model.appendRow(item)

    def on_tree_repositories_itemSelectionChanged(self):
        """Slot for when the itemSelectionChanged signal emitted."""
        # Activate edit and delete button
        self.button_edit.setEnabled(True)
        self.button_delete.setEnabled(True)

    def on_list_view_collections_clicked(self, index):
        collection_item = self.collections_model.itemFromIndex(index)
        self.show_collection_metadata(collection_item.data())

    def show_collection_metadata(self, id):
        """Show the collection metadata given the id."""
        html = self.repository_manager.collections_manager.html(id)
        self.web_view_details.setHtml(html)

    def reject(self):
        """Slot when the dialog is closed."""
        # Serialize collections to settings
        self.repository_manager.collections_manager.serialize()
        self.done(0)

    def show_progress_dialog(self, text):
        """Show infinite progress dialog with given text.

        :param text: Text as the label of the progress dialog
        :type text: str
        """
        if self.progress_dialog is not None:
            self.progress_dialog.show()
            # Just use infinite progress bar here
            self.progress_dialog.setMaximum(0)
            self.progress_dialog.setMinimum(0)
            self.progress_dialog.setValue(0)
            self.progress_dialog.setLabelText(text)

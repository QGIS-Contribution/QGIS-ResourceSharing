# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 Download collections shared by other users
                             -------------------
        begin                : 2016-05-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Akbar Gumbira
        copyright            : (C) 2020 by Håvard Tveite
        email                : havard.tveite@nmbu.no
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
import logging

from qgis.PyQt import uic
from qgis.PyQt.Qt import QSize, QFont, QBrush, QColor
from qgis.PyQt.QtCore import (
    Qt, QSettings, pyqtSlot, QRegExp, QUrl, QThread)

from qgis.PyQt.QtGui import (
    QIcon,
    QDesktopServices,
    QStandardItem,
    QStandardItemModel)
try:
    from qgis.PyQt.QtGui import (
        QListWidgetItem,
        QDialog,
        QTreeWidgetItem,
        QSizePolicy,
        QMessageBox,
        QProgressDialog,
        QDialogButtonBox)
except ImportError:
    from qgis.PyQt.QtWidgets import (
        QListWidgetItem,
        QDialog,
        QTreeWidgetItem,
        QSizePolicy,
        QMessageBox,
        QProgressDialog,
        QDialogButtonBox)


from qgis.gui import QgsMessageBar
from qgis.core import Qgis
from qgis.core import QgsSettings

from resource_sharing.gui.manage_dialog import ManageRepositoryDialog
from resource_sharing.repository_manager import RepositoryManager
from resource_sharing.collection_manager import (
    CollectionManager,
    CollectionInstaller)
from resource_sharing.utilities import (
    resources_path,
    ui_path,
    repo_settings_group,
    local_collection_path,
    render_template)
from resource_sharing.gui.custom_sort_filter_proxy import (
    CustomSortFilterProxyModel,
    COLLECTION_NAME_ROLE,
    COLLECTION_DESCRIPTION_ROLE,
    COLLECTION_AUTHOR_ROLE,
    COLLECTION_TAGS_ROLE,
    COLLECTION_ID_ROLE,
    COLLECTION_STATUS_ROLE)
from resource_sharing.config import (
    COLLECTION_ALL_STATUS,
    COLLECTION_INSTALLED_STATUS)
from resource_sharing import config

FORM_CLASS, _ = uic.loadUiType(str(ui_path('resource_sharing_dialog_base.ui')))
LOGGER = logging.getLogger('QGIS Resource Sharing')
REPOSITORY_ITEM = 1000
COLLECTION_ITEM = 2000

class ResourceSharingDialog(QDialog, FORM_CLASS):
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
        super(ResourceSharingDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        # Reconfigure UI
        self.setModal(True)
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)
        self.button_install.setEnabled(False)
        self.button_open.setEnabled(False)
        self.button_uninstall.setEnabled(False)

        # Set up the "main menu" - QListWidgetItem
        # All collections
        icon_all = QIcon()
        icon_all.addFile(
            str(resources_path('img', 'plugin.svg')),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_all = QListWidgetItem()
        item_all.setIcon(icon_all)
        item_all.setText(self.tr('All collections'))
        # Installed collections
        icon_installed = QIcon()
        icon_installed.addFile(
            str(resources_path('img', 'plugin-installed.svg')),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_installed = QListWidgetItem()
        item_installed.setIcon(icon_installed)
        item_installed.setText(self.tr('Installed collections'))
        item_all.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        # Settings / repositories
        icon_settings = QIcon()
        icon_settings.addFile(
            str(resources_path('img', 'settings.svg')),
            QSize(),
            QIcon.Normal,
            QIcon.Off)
        item_settings = QListWidgetItem()
        item_settings.setIcon(icon_settings)
        item_settings.setText(self.tr('Settings'))
        item_all.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # Add the items to the list widget
        self.menu_list_widget.addItem(item_all)
        self.menu_list_widget.addItem(item_installed)
        self.menu_list_widget.addItem(item_settings)

        # Init the message bar
        self.message_bar = QgsMessageBar(self)
        self.message_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vlayoutRightColumn.insertWidget(0, self.message_bar)

        # Progress dialog for long running processes
        self.progress_dialog = None

        # Init the repository manager dialog
        self.repository_manager = RepositoryManager()
        self.collection_manager = CollectionManager()
        # Collections list view
        self.collections_model = QStandardItemModel(0, 1)
        self.collections_model.sort(0, Qt.AscendingOrder)
        self.collection_proxy = CustomSortFilterProxyModel(self)
        self.collection_proxy.setSourceModel(self.collections_model)
        self.list_view_collections.setModel(self.collection_proxy)
        # Active selected collection
        self._selected_collection_id = None

        # Slots
        self.button_add.clicked.connect(self.add_repository)
        self.button_edit.clicked.connect(self.edit_repository)
        self.button_delete.clicked.connect(self.delete_repository)
        self.button_reload.clicked.connect(self.reload_repositories)
        self.menu_list_widget.currentRowChanged.connect(self.set_current_tab)
        self.list_view_collections.selectionModel().currentChanged.connect(
            self.on_list_view_collections_clicked)
        self.line_edit_filter.textChanged.connect(self.filter_collections)
        self.button_install.clicked.connect(self.install_collection)
        self.button_open.clicked.connect(self.open_collection)
        self.button_uninstall.clicked.connect(self.uninstall_collection)
        self.button_box.button(QDialogButtonBox.Help).clicked.connect(
            self.open_help)

        # Populate the repositories widget and collections list view
        self.populate_repositories_widget()
        self.reload_collections_model()

    def set_current_tab(self, index):
        """Set stacked widget based on the active tab.

        :param index: The index of the active widget (in the list widget).
        :type index: int
        """
        # Clear message bar
        self.message_bar.clearWidgets()
        if index == (self.menu_list_widget.count() - 1):
            # Last menu entry - Settings
            self.stacked_menu_widget.setCurrentIndex(1)
        else:
            # Not settings, must be Collections (all or installed)
            if index == 1:
                # Installed collections
                self.collection_proxy.accepted_status = \
                    COLLECTION_INSTALLED_STATUS
                # Set the web view
                title = self.tr('Installed Collections')
                description = self.tr(
                    'On the left you see the list of all the '
                    'installed collections.')
            else:
                # All collections (0)
                self.collection_proxy.accepted_status = COLLECTION_ALL_STATUS
                # Set the web view
                title = self.tr('All Collections')
                description = self.tr(
                    'On the left you see a list of all the collections '
                    'that are available from the registered repositories.<br> '
                    'Installed collections are emphasized (in <b>bold</b>).')

            context = {
                'resources_path': str(resources_path()),
                'title': title,
                'description': description
            }
            self.web_view_details.setHtml(
                render_template('tab_description.html', context))
            self.stacked_menu_widget.setCurrentIndex(0)

    def add_repository(self):
        """Open add repository dialog."""
        dlg = ManageRepositoryDialog(self)
        if not dlg.exec_():
            return

        for repoName, repo in self.repository_manager.directories.items():
            if dlg.line_edit_url.text().strip() == repo['url']:
                self.message_bar.pushMessage(
                    self.tr(
                        'Unable to add another repository with the same URL!'),
                    Qgis.Warning, 5)
                return
            if dlg.line_edit_name.text().strip() == repoName:
                self.message_bar.pushMessage(
                    self.tr(
                        'Repositories must have unique names!'),
                    Qgis.Warning, 5)
                return

        repo_name = dlg.line_edit_name.text()
        repo_url = dlg.line_edit_url.text().strip()
        repo_auth_cfg = dlg.line_edit_auth_id.text().strip()
        if repo_name in self.repository_manager.directories:
            repo_name += '(2)'

        # Show progress dialog
        self.show_progress_dialog("Fetching repository's metadata")

        # Add repository
        try:
            status, adderror = self.repository_manager.add_directory(
                repo_name, repo_url, repo_auth_cfg)
            if status:
                self.message_bar.pushMessage(
                    self.tr(
                        'Repository was successfully added'),
                    Qgis.Success, 5)
            else:
                self.message_bar.pushMessage(
                    self.tr(
                        'Unable to add repository: %s') % adderror,
                    Qgis.Warning, 5)
        except Exception as e:
            self.message_bar.pushMessage(
                self.tr('%s') % e,
                Qgis.Warning, 5)
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

        # Check if it is among the officially approved QGIS repositories
        settings = QgsSettings()
        settings.beginGroup(repo_settings_group())
        if settings.value(repo_name + '/url') in \
                self.repository_manager._online_directories.values():
            self.message_bar.pushMessage(
                self.tr(
                    'You can not edit the official repositories!'),
                Qgis.Warning, 5)
            return

        dlg = ManageRepositoryDialog(self)
        dlg.line_edit_name.setText(repo_name)
        dlg.line_edit_url.setText(
            self.repository_manager.directories[repo_name]['url'])
        dlg.line_edit_auth_id.setText(
            self.repository_manager.directories[repo_name]['auth_cfg'])

        if not dlg.exec_():
            return

        # Check if the changed URL is already present and that
        # the new repository name is unique
        new_url = dlg.line_edit_url.text().strip()
        old_url = self.repository_manager.directories[repo_name]['url']
        new_name = dlg.line_edit_name.text().strip()
        for repoName, repo in self.repository_manager.directories.items():
            if new_url == repo['url'] and (old_url != new_url):
                self.message_bar.pushMessage(
                    self.tr('Unable to add another repository with the same '
                            'URL!'),
                    Qgis.Warning, 5)
                return
            if new_name == repoName and (repo_name != new_name):
                self.message_bar.pushMessage(
                    self.tr(
                        'Repositories must have unique names!'),
                    Qgis.Warning, 5)
                return

        # Redundant
        if (new_name in self.repository_manager.directories) and (
                    new_name != repo_name):
            new_name += '(2)'

        new_auth_cfg = dlg.line_edit_auth_id.text()

        # Show progress dialog
        self.show_progress_dialog("Fetching repository's metadata")

        # Edit repository
        try:
            status, editerror = self.repository_manager.edit_directory(
                repo_name,
                new_name,
                old_url,
                new_url,
                new_auth_cfg
            )
            if status:
                self.message_bar.pushMessage(
                    self.tr('Repository is successfully updated'),
                    Qgis.Success, 5)
            else:
                self.message_bar.pushMessage(
                    self.tr('Unable to edit repository: %s') % editerror,
                    Qgis.Warning, 5)
        except Exception as e:
            self.message_bar.pushMessage(
                self.tr('%s') % e, Qgis.Warning, 5)
        finally:
            self.progress_dialog.hide()

        # Reload data and widget
        self.reload_data_and_widget()

        # Deactivate the edit and delete buttons
        self.button_edit.setEnabled(False)
        self.button_delete.setEnabled(False)

    def delete_repository(self):
        """Delete a repository in the tree widget."""
        selected_item = self.tree_repositories.currentItem()
        if selected_item:
            repo_name = selected_item.text(0)

        if not repo_name:
            return
        # Check if it is among the offical repositories
        repo_url = self.repository_manager.directories[repo_name]['url']
        if repo_url in self.repository_manager._online_directories.values():
            self.message_bar.pushMessage(
                self.tr(
                    'You can not remove official repositories!'),
                Qgis.Warning, 5)
            return

        warning = self.tr('Are you sure you want to remove the following '
                          'repository?') + '\n' + repo_name
        if QMessageBox.warning(
                self,
                self.tr('QGIS Resource Sharing'),
                warning,
                QMessageBox.Yes,
                QMessageBox.No) == QMessageBox.No:
            return

        # Remove repository
        installed_collections = \
            self.collection_manager.get_installed_collections(repo_url)
        if installed_collections:
            message = ('You have installed collections from this '
                       'repository. Please uninstall them first!')
            self.message_bar.pushMessage(message, Qgis.Warning, 5)
        else:
            self.repository_manager.remove_directory(repo_name)
            # Reload data and widget
            self.reload_data_and_widget()
            # Deactivate the edit and delete buttons
            self.button_edit.setEnabled(False)
            self.button_delete.setEnabled(False)

    def reload_repositories(self):
        """Slot for when user clicks reload repositories button."""
        # Show progress dialog
        self.show_progress_dialog('Reloading all repositories')

        for repo_name in self.repository_manager.directories:
            directory = self.repository_manager.directories[repo_name]
            url = directory['url']
            auth_cfg = directory['auth_cfg']
            try:
                status, reloaderror = self.repository_manager.reload_directory(
                    repo_name, url, auth_cfg)
                if status:
                    self.message_bar.pushMessage(
                        self.tr(
                            'Repository %s is successfully reloaded') %
                        repo_name, Qgis.Info, 5)
                else:
                    self.message_bar.pushMessage(
                        self.tr(
                            'Unable to reload %s: %s') % (
                            repo_name, reloaderror),
                        Qgis.Warning, 5)
            except Exception as e:
                self.message_bar.pushMessage(
                    self.tr('%s') % e,
                    Qgis.Warning, 5)

        self.progress_dialog.hide()
        # Reload data and widget
        self.reload_data_and_widget()

    def install_collection(self):
        """Slot for when the user clicks the install/reinstall button."""
        # Save the current index to enable selection after installation
        self.current_index = self.list_view_collections.currentIndex()
        self.show_progress_dialog('Starting installation...')
        self.progress_dialog.canceled.connect(self.install_canceled)

        self.installer_thread = QThread()
        self.installer_worker = CollectionInstaller(
            self.collection_manager, self._selected_collection_id)
        self.installer_worker.moveToThread(self.installer_thread)
        self.installer_worker.finished.connect(self.install_finished)
        self.installer_worker.aborted.connect(self.install_aborted)
        self.installer_worker.progress.connect(self.install_progress)
        self.installer_thread.started.connect(self.installer_worker.run)
        self.installer_thread.start()

    def install_finished(self):
        # Process the result
        self.progress_dialog.hide()
        installStatus = self.installer_worker.install_status
        if not installStatus:
            message = self.installer_worker.error_message
        # Clean up the worker and thread
        self.installer_worker.deleteLater()
        self.installer_thread.quit()
        self.installer_thread.wait()
        self.installer_thread.deleteLater()

        if installStatus:
            self.reload_collections_model()
            # Report what has been installed
            message = '<b>%s</b> was successfully installed, containing:\n<ul>' % (
                config.COLLECTIONS[self._selected_collection_id]['name'])
            number = 0
            if 'style' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['style']
                message = message + '\n<li> ' + str(number) + ' Layer style (QML) file'
                if number > 1:
                    message = message + 's'
            if 'symbol' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['symbol']
                message = message + '\n<li> ' + str(number) + ' XML symbol file'
                if number > 1:
                    message = message + 's'
            if 'svg' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['svg']
                message = message + '\n<li> ' + str(number) + ' SVG file'
                if number > 1:
                    message = message + 's'
            if 'models' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['models']
                message = message + '\n<li> ' + str(number) + ' model'
                if number > 1:
                    message = message + 's'
            if 'expressions' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['expressions']
                message = message + '\n<li> ' + str(number) + ' expression file'
                if number > 1:
                    message = message + 's'
            if 'processing' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['processing']
                message = message + '\n<li> ' + str(number) + ' processing script'
                if number > 1:
                    message = message + 's'
            if 'rscripts' in config.COLLECTIONS[self._selected_collection_id].keys():
                number = config.COLLECTIONS[self._selected_collection_id]['rscripts']
                message = message + '\n<li> ' + str(number) + ' R script'
                if number > 1:
                    message = message + 's'
            message = message + '\n</ul>'
        QMessageBox.information(self, 'Resource Sharing', message)
        self.populate_repositories_widget()
        # Set the selection
        oldRow = self.current_index.row()
        newIndex = self.collections_model.createIndex(oldRow, 0)
        selection_model = self.list_view_collections.selectionModel()
        selection_model.setCurrentIndex(newIndex, selection_model.ClearAndSelect)
        selection_model.select(newIndex, selection_model.ClearAndSelect)
        # Update the buttons
        self.button_install.setEnabled(True)
        self.button_install.setText('Reinstall')
        self.button_open.setEnabled(True)
        self.button_uninstall.setEnabled(True)

        self.show_collection_metadata(self._selected_collection_id)

    def install_canceled(self):
        self.progress_dialog.hide()
        self.show_progress_dialog('Cancelling installation...')
        self.installer_worker.abort()

    def install_aborted(self):
        if self.installer_thread.isRunning():
            self.installer_thread.quit()
        self.installer_thread.finished.connect(self.progress_dialog.hide)

    def install_progress(self, text):
        self.progress_dialog.setLabelText(text)

    def uninstall_collection(self):
        """Slot called when user clicks the uninstall button."""
        # get the QModelIndex for the item to be uninstalled
        uninstall_index = self.list_view_collections.currentIndex()
        coll_id = self._selected_collection_id
        try:
            self.collection_manager.uninstall(coll_id)
        except Exception as e:
            LOGGER.error('Could not uninstall collection ' +
                         config.COLLECTIONS[coll_id]['name'] + ':\n' + str(e))
        else:
            QMessageBox.information(
                self,
                'Resource Sharing',
                'The collection was successfully uninstalled!')
            self.reload_collections_model()
            # Fix the GUI
            currentMenuRow = self.menu_list_widget.currentRow()
            self.set_current_tab(currentMenuRow)
            self.populate_repositories_widget()

            rowCount = self.collection_proxy.rowCount()
            if rowCount > 0:
                # Set the current (and selected) row in the listview
                newRow = uninstall_index.row()
                # Check if this was the last element
                rowCount = self.collection_proxy.rowCount()
                if newRow == rowCount:
                   newRow = newRow - 1
                # Select the new current element
                newIndex = self.collections_model.createIndex(newRow, 0)
                selection_model = self.list_view_collections.selectionModel()
                selection_model.setCurrentIndex(newIndex, selection_model.ClearAndSelect)
                # Get the id of the current collection
                proxyModel = self.list_view_collections.model()
                proxyIndex = proxyModel.index(newRow,0)
                current_coll_id = proxyIndex.data(COLLECTION_ID_ROLE)
                self._selected_collection_id = current_coll_id
                # Update buttons
                status = config.COLLECTIONS[current_coll_id]['status']
                if status == COLLECTION_INSTALLED_STATUS:
                    self.button_install.setEnabled(True)
                    self.button_install.setText('Reinstall')
                    self.button_open.setEnabled(True)
                    self.button_uninstall.setEnabled(True)
                else:
                    self.button_install.setEnabled(True)
                    self.button_install.setText('Install')
                    self.button_open.setEnabled(False)
                    self.button_uninstall.setEnabled(False)
                # Update the web_view_details frame
                self.show_collection_metadata(current_coll_id)
            else:
                self.button_install.setEnabled(False)
                self.button_install.setText('Install')
                self.button_open.setEnabled(False)
                self.button_uninstall.setEnabled(False)

    def open_collection(self):
        """Slot for when user clicks 'Open' button."""
        collection_path = local_collection_path(self._selected_collection_id)
        directory_url = QUrl.fromLocalFile(str(collection_path))
        QDesktopServices.openUrl(directory_url)

    def reload_data_and_widget(self):
        """Reload repositories and collections and update widgets related."""
        self.reload_repositories_widget()
        self.reload_collections_model()

    def reload_repositories_widget(self):
        """Refresh tree repositories using new repositories data."""
        self.repository_manager.load_directories()
        self.populate_repositories_widget()

    def populate_repositories_widget(self):
        """Populate the current dictionary repositories to the tree widget."""
        # Clear the current tree widget
        self.tree_repositories.clear()
        installed_collections = \
            self.collection_manager.get_installed_collections()
        # Export the updated ones from the repository manager
        repo_Font = QFont()
        repo_with_installed_Font = QFont()
        repo_with_installed_Font.setWeight(60)
        collection_brush = QBrush(Qt.darkGray)
        installed_collection_brush = QBrush(QColor(60, 25, 10))
        for repo_name in self.repository_manager.directories:
            url = self.repository_manager.directories[repo_name]['url']
            item = QTreeWidgetItem(self.tree_repositories, REPOSITORY_ITEM)
            # Is the repository in the QGIS resource directory?
            if url in self.repository_manager._online_directories.values():
                repo_with_installed_Font.setUnderline(True)
                repo_Font.setUnderline(True)
            else:
                repo_with_installed_Font.setUnderline(False)
                repo_Font.setUnderline(False)
            item.setText(0, repo_name)
            item.setText(1, url)
            item.setFont(0,repo_Font)
            for coll_id in config.COLLECTIONS:
                if ('repository_name' in config.COLLECTIONS[coll_id].keys() and
                    config.COLLECTIONS[coll_id]['repository_name'] == repo_name):
                    coll_name = config.COLLECTIONS[coll_id]['name']
                    coll_tags = config.COLLECTIONS[coll_id]['tags']
                    collectionItem = QTreeWidgetItem(item, COLLECTION_ITEM)
                    brush = collection_brush
                    collectionFont = QFont()
                    collectionFont.setStyle(QFont.StyleItalic)
                    collitemtext = coll_name
                    if installed_collections and coll_id in installed_collections.keys():
                       collitemtext = coll_name + ' (installed)'
                       brush = installed_collection_brush
                       item.setFont(0,repo_with_installed_Font)
                       item.setForeground(0, brush)
                       item.setForeground(1, brush)
                    collectionItem.setFont(0, collectionFont)
                    collectionItem.setForeground(0, brush)
                    collectionItem.setText(0, collitemtext)
                    collectionItem.setFont(1, collectionFont)
                    collectionItem.setForeground(1, brush)
                    collectionItem.setText(1, coll_tags)
        self.tree_repositories.resizeColumnToContents(0)
        self.tree_repositories.resizeColumnToContents(1)
        self.tree_repositories.sortItems(1, Qt.AscendingOrder)

    def reload_collections_model(self):
        """Reload the collections model with the current collections."""
        self.collections_model.clear()
        installed_collections = \
            self.collection_manager.get_installed_collections()
        for id in config.COLLECTIONS:
            collection_name = config.COLLECTIONS[id]['name']
            collection_author = config.COLLECTIONS[id]['author']
            collection_tags = config.COLLECTIONS[id]['tags']
            collection_description = config.COLLECTIONS[id]['description']
            collection_status = config.COLLECTIONS[id]['status']
            repository_name = ''
            if 'repository_name' in config.COLLECTIONS[id].keys():
              repository_name = config.COLLECTIONS[id]['repository_name']
            item = QStandardItem(collection_name + ' (' + repository_name + ')')
            item.setEditable(False)
            item.setData(id, COLLECTION_ID_ROLE)
            item.setData(collection_name, COLLECTION_NAME_ROLE)
            item.setData(collection_description, COLLECTION_DESCRIPTION_ROLE)
            item.setData(collection_author, COLLECTION_AUTHOR_ROLE)
            item.setData(collection_tags, COLLECTION_TAGS_ROLE)
            item.setData(collection_status, COLLECTION_STATUS_ROLE)
            # Make installed collections stand out
            if installed_collections and id in installed_collections.keys():
                collectionFont = QFont()
                collectionFont.setWeight(60)
                item.setFont(collectionFont)
            self.collections_model.appendRow(item)
        self.collections_model.sort(0, Qt.AscendingOrder)

    def on_tree_repositories_itemSelectionChanged(self):
        """Slot for the itemSelectionChanged signal of tree_repositories."""
        selected_item = self.tree_repositories.currentItem()
        if selected_item and selected_item.type() == REPOSITORY_ITEM:
            if selected_item:
                repo_name = selected_item.text(0)
            if not repo_name:
                return
            if not repo_name in self.repository_manager.directories.keys():
                return
            repo_url = self.repository_manager.directories[repo_name]['url']
            # Disable the edit and delete buttons for "official" repositories
            if repo_url in self.repository_manager._online_directories.values():
                self.button_edit.setEnabled(False)
                self.button_delete.setEnabled(False)
            else:
                # Activate the edit and delete buttons
                self.button_edit.setEnabled(True)
                self.button_delete.setEnabled(True)
        elif selected_item and selected_item.type() == COLLECTION_ITEM:
            self.button_edit.setEnabled(False)
            self.button_delete.setEnabled(False)
        else:
            self.button_edit.setEnabled(False)
            self.button_delete.setEnabled(False)

    def on_list_view_collections_clicked(self, index):
        """Slot for when the list_view_collections is clicked."""
        real_index = self.collection_proxy.mapToSource(index)
        if real_index.row() != -1:
            collection_item = self.collections_model.itemFromIndex(real_index)
            collection_id = collection_item.data(COLLECTION_ID_ROLE)
            self._selected_collection_id = collection_id

            # Enable / disable buttons
            status = config.COLLECTIONS[self._selected_collection_id]['status']
            is_installed = status == COLLECTION_INSTALLED_STATUS
            if is_installed:
                self.button_install.setEnabled(True)
                self.button_install.setText('Reinstall')
                self.button_open.setEnabled(True)
                self.button_uninstall.setEnabled(True)
            else:
                self.button_install.setEnabled(True)
                self.button_install.setText('Install')
                self.button_open.setEnabled(False)
                self.button_uninstall.setEnabled(False)

            # Show  metadata
            self.show_collection_metadata(collection_id)

    @pyqtSlot(str)
    def filter_collections(self, text):
        search = QRegExp(
            text,
            Qt.CaseInsensitive,
            QRegExp.RegExp)
        self.collection_proxy.setFilterRegExp(search)

    def show_collection_metadata(self, id):
        """Show the collection metadata given the ID."""
        html = self.collection_manager.get_html(id)
        self.web_view_details.setHtml(html)

    def reject(self):
        """Slot when the dialog is closed."""
        # Serialize collections to settings
        self.repository_manager.serialize_repositories()
        self.done(0)

    def open_help(self):
        """Open help."""
        doc_url = QUrl('http://qgis-contribution.github.io/' +
                       'QGIS-ResourceSharing/')
        QDesktopServices.openUrl(doc_url)

    def show_progress_dialog(self, text):
        """Show infinite progress dialog with given text.

        :param text: Text as the label of the progress dialog
        :type text: str
        """
        if self.progress_dialog is None:
            self.progress_dialog = QProgressDialog(self)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setAutoClose(False)
            title = self.tr('Resource Sharing')
            self.progress_dialog.setWindowTitle(title)
            # Just use an infinite progress bar here
            self.progress_dialog.setMaximum(0)
            self.progress_dialog.setMinimum(0)
            self.progress_dialog.setValue(0)
            self.progress_dialog.setLabelText(text)

        self.progress_dialog.show()

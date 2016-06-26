# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DownloadDialog
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
import sys
from PyQt4 import QtGui, uic, QtCore

from ..utilities import ui_path
from ..repository_manager import RepositoryManager

FORM_CLASS, _ = uic.loadUiType(ui_path('download_dialog.ui'))


class DownloadDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None, collection_id=None):
        """Constructor."""
        super(DownloadDialog, self).__init__(parent)
        self.setupUi(self)
        self.repository_manager = RepositoryManager()
        self._collection_id = collection_id
        self.start_download()

    def start_download(self):
        err_stream = EmittingStream(text_written=self.normal_output_written)
        self.repository_manager.download_collection(self._collection_id,
                                                    err_stream)

    def normal_output_written(self, text):
        """Append text to the QTextEdit."""
        cursor = self.text_edit_log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.text_edit_log.setTextCursor(cursor)
        self.text_edit_log.ensureCursorVisible()


class EmittingStream(QtCore.QObject):
    text_written = QtCore.pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

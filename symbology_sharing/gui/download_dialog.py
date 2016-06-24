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
from PyQt4 import QtGui, uic

from ..utilities import ui_path
from ..repository_manager import RepositoryManager

FORM_CLASS, _ = uic.loadUiType(ui_path('download_dialog.ui'))


class DownloadDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None, collection_id=None):
        """Constructor."""
        super(DownloadDialog, self).__init__(parent)
        self.setupUi(self)
        self.repository_manager = RepositoryManager()

        out_log = OutLog(self.text_edit_log, sys.stderr)
        self.repository_manager.download_collection(collection_id, out_log)


class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)



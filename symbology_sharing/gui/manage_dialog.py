# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ManageRepositoryDialog
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

from ..utilities import ui_path
from ..repository_manager import RepositoryManager

FORM_CLASS, _ = uic.loadUiType(ui_path('manage_repository.ui'))


class ManageRepositoryDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ManageRepositoryDialog, self).__init__(parent)
        self.setupUi(self)
        self.line_edit_url.setText('http://')
        self.line_edit_name.textChanged.connect(self.form_changed)
        self.line_edit_url.textChanged.connect(self.form_changed)

    def form_changed(self):
        """Slot for when the form changed."""
        is_enabled = (len(self.line_edit_name.text()) > 0 and
                      len(self.line_edit_url.text()) > 0)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(is_enabled)





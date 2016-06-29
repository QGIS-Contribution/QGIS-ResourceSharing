# coding=utf-8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSortFilterProxyModel

COLLECTION_NAME_ROLE = Qt.UserRole + 1
COLLECTION_DESCRIPTION_ROLE = Qt.UserRole + 2
COLLECTION_AUTHOR_ROLE = Qt.UserRole + 3
COLLECTION_TAGS_ROLE = Qt.UserRole + 4
COLLECTION_ID_ROLE = Qt.UserRole + 5


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    """Custom QSortFilterProxyModel to be able to search on multiple data."""
    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)

    def filterAcceptsRow(self, row_num, source_parent):
        """Override this function."""
        index = self.sourceModel().index(row_num, 0, source_parent)
        name = self.filterRegExp().indexIn(
            self.sourceModel().data(index, COLLECTION_NAME_ROLE)) >= 0
        author = self.filterRegExp().indexIn(
            self.sourceModel().data(index, COLLECTION_AUTHOR_ROLE)) >= 0
        description = self.filterRegExp().indexIn(
            self.sourceModel().data(index, COLLECTION_DESCRIPTION_ROLE)) >= 0
        tags = self.filterRegExp().indexIn(
            self.sourceModel().data(index, COLLECTION_TAGS_ROLE)) >= 0

        return name or author or description or tags

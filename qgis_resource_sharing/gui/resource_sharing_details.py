"""
/***************************************************************************
                       QGIS Resource Sharing - a QGIS plugin
 Download collections shared by other users
                             -------------------
        begin                : 2024-03-05
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jean Felder
        email                : jean dot felder at oslandia dot com
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
from typing import List, Optional

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from qgis.PyQt.QtWidgets import QLabel, QWidget

from qgis_resource_sharing.collection_manager import CollectionManager
from qgis_resource_sharing.config import CollectionStatus
from qgis_resource_sharing.utilities import ui_path

# -- GLOBALS
FORM_CLASS, _ = uic.loadUiType(str(ui_path("resource_sharing_details_base.ui")))
LOGGER = logging.getLogger("QGIS Resource Sharing")


class QgsResourceSharingDetails(QWidget, FORM_CLASS):
    """Widget to display the details of a collection as a grid"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Constructor.

        :param parent: Optional widget to use as parent
        :type parent: QWidget
        """
        super(QgsResourceSharingDetails, self).__init__(parent)
        self.setupUi(self)

        self._collection_manager = CollectionManager()
        self._network_manager = QNetworkAccessManager(self)
        self._network_manager.finished.connect(self._on_request_response)
        self._network_replies: List[QNetworkReply] = []

    def set_content(self, collection_id: str) -> None:
        """Return the details of a collection as HTML, given its id.

        :param collection_id: The id of the collection
        :type collection_id: str
        """
        # reset
        self.setMinimumWidth(400)
        for reply in self._network_replies:
            reply.abort()

        # get collection information
        collection = self._collection_manager.get_collection(collection_id)

        # title
        self.titleLabel.setText(f'<h1>{collection["name"]}</h1>')
        LOGGER.debug(
            f"Set content of collection {collection['name']} with id {collection_id}"
        )

        # description and tags
        self.descriptionContent.setText(collection["description"])
        self.tagsContent.setText(collection["tags"])

        # resources
        show_resources_html = collection["status"] == CollectionStatus.INSTALLED
        self.resourcesLabel.setVisible(show_resources_html)
        self.resourcesContent.setVisible(show_resources_html)
        self.resourcesContent.setText(collection["resources_html"])
        self.resourcesLine.setVisible(show_resources_html)

        # preview images
        # remove the previous images
        for idx in reversed(range(self.verticalLayoutPreview.count())):
            self.verticalLayoutPreview.itemAt(idx).widget().setParent(None)

        # load the new images
        for preview_path in collection["preview"]:
            reply = self._network_manager.get(QNetworkRequest(QUrl(preview_path)))
            self._network_replies.append(reply)

        visible_preview = len(collection["preview"]) > 0
        self.previewsLabel.setVisible(visible_preview)
        self.previewsContent.setVisible(visible_preview)
        self.previewsLine.setVisible(visible_preview)

        preview_label_text = "Previews"
        if len(collection["preview"]) > 1:
            preview_label_text += f" ({len(collection['preview'])})"

        self.previewsLabel.setText(preview_label_text)

        # repository url
        res_url = collection["repository_url"]
        self.urlContent.setText(f'<a href="{res_url}">{res_url}</a>')

        # license
        # FIXME: a license may contain an image which is not visible
        # at the moment
        if collection["license"]:
            self.licenseLabel.setVisible(True)
            self.licenseContent.setVisible(True)
            self.licenseLine.setVisible(True)
            self.licenseLabel.setText("License")
            license_text = collection["license"]
            if collection["license_url"]:
                license_url = collection["license_url"]
                license_text += f' (read <a href="{license_url}">here</a>)'

            self.licenseContent.setText(license_text)
        elif collection["license_url"]:
            self.licenseLabel.setVisible(True)
            self.licenseContent.setVisible(True)
            self.licenseLine.setVisible(True)
            self.licenseLabel.setText("License File")
            license_url = collection["license_url"]
            license_text = f'Read the license <a href="{license_url}">here</a>'
            self.licenseContent.setText(license_text)
        else:
            self.licenseLabel.setVisible(False)
            self.licenseContent.setVisible(False)
            self.licenseLine.setVisible(False)

        # author and email
        self.authorContent.setText(collection["author"])
        email = collection["author_email"]
        self.emailContent.setText(f'<a href="mailto:{email}">{email}</a>')

    def _on_request_response(self, network_reply: QNetworkReply) -> None:
        """Load the content of a network request as an image.

        :param network_reply: a network reply wich contains image data
        :type collection_id: QNetworkReply
        """
        self._network_replies.remove(network_reply)
        if network_reply.error() != QNetworkReply.NetworkError.NoError:
            LOGGER.error(f"Unable to download image from {network_reply.url()}")
            return

        img_data = network_reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.verticalLayoutPreview.addWidget(label)

        LOGGER.debug(f"Image downloaded from {network_reply.url()}")

        # the min width of the container is the size of the widest image
        # + the size of the other labels
        new_width = pixmap.width() + 180
        if new_width > self.minimumWidth():
            self.setMinimumWidth(new_width)

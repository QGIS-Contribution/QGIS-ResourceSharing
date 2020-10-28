import logging

from qgis.core import (
    QgsPalLayerSettings,
    QgsProject,
    QgsReadWriteContext,
    QgsSymbolLayerUtils,
    QgsTextFormat,
)
from qgis.PyQt.QtCore import QFile, QIODevice
from qgis.PyQt.QtXml import QDomDocument

LOGGER = logging.getLogger("QGIS Resource Sharing")


class SymbolXMLExtractor(object):
    """Parses the given file and returns the symbols and colorramps"""

    def __init__(self, xml_path):
        """Constructor of the class.

        :param xml_path: The path to the symbol xml
        :type xml_path: str
        """
        self._xml_path = xml_path
        self._symbols = []
        self._colorramps = []
        # Parse the xml to get the symbols and colorramps
        self.parse_xml()

    def parse_xml(self):
        """Parse the xml file. Returns false if there is failure."""
        xml_file = QFile(self._xml_path)
        if not xml_file.open(QIODevice.ReadOnly):
            return False

        document = QDomDocument()
        if not document.setContent(xml_file):
            return False

        xml_file.close()

        document_element = document.documentElement()
        if document_element.tagName() != "qgis_style":
            return False

        # Get all the symbols
        self._symbols = []
        symbols_element = document_element.firstChildElement("symbols")
        symbol_element = symbols_element.firstChildElement()
        context = QgsReadWriteContext()
        context.setPathResolver(QgsProject.instance().pathResolver())
        while not symbol_element.isNull():
            if symbol_element.tagName() == "symbol":
                symbol = QgsSymbolLayerUtils.loadSymbol(symbol_element, context)
                if symbol:
                    self._symbols.append(
                        {"name": symbol_element.attribute("name"), "symbol": symbol}
                    )
            symbol_element = symbol_element.nextSiblingElement()

        # Get all the colorramps
        self._colorramps = []
        ramps_element = document_element.firstChildElement("colorramps")
        ramp_element = ramps_element.firstChildElement()
        while not ramp_element.isNull():
            if ramp_element.tagName() == "colorramp":
                colorramp = QgsSymbolLayerUtils.loadColorRamp(ramp_element)
                if colorramp:
                    self._colorramps.append(
                        {"name": ramp_element.attribute("name"), "colorramp": colorramp}
                    )

            ramp_element = ramp_element.nextSiblingElement()

        # Get all the TextFormats - textformats - textformat
        self._textformats = []
        textformats_element = document_element.firstChildElement("textformats")
        textformat_element = textformats_element.firstChildElement()
        while not textformat_element.isNull():
            if textformat_element.tagName() == "textformat":
                textformat = QgsTextFormat()
                textformat.readXml(textformat_element, QgsReadWriteContext())
                if textformat:
                    self._textformats.append(
                        {
                            "name": textformat_element.attribute("name"),
                            "textformat": textformat,
                        }
                    )
            textformat_element = textformat_element.nextSiblingElement()

        # Get all the LabelSettings - labelsettings - labelsetting -
        #  QgsPalLayerSettings.readXML?
        self._labelsettings = []
        labels_element = document_element.firstChildElement("labelsettings")
        label_element = labels_element.firstChildElement()

        while not label_element.isNull():
            if label_element.tagName() == "labelsetting":
                labelsettings = QgsPalLayerSettings()
                labelsettings.readXml(label_element, QgsReadWriteContext())
                if labelsettings:
                    self._labelsettings.append(
                        {
                            "name": label_element.attribute("name"),
                            "labelsettings": labelsettings,
                        }
                    )
            label_element = label_element.nextSiblingElement()
        return True

    @property
    def symbols(self):
        """Return a list of the symbols in the XML file.

        The structure of the property:
        symbols = [
            {
                'name': str
                'symbol': QgsSymbolV2
            }
        ]
        """
        return self._symbols

    @property
    def colorramps(self):
        """Return a list of the colorramps in the XML file.

        The structure of the property:
        colorramps = [
            {
                'name': str
                'colorramp': QgsVectorColorRampV2
            }
        ]
        """
        return self._colorramps

    @property
    def textformats(self):
        """Return a list of the textformats in the XML file.
        The structure of the property:
        textformats = [
            {
                'name': str
                'textformat': QgsTextFormat???
            }
        ]
        """
        return self._textformats

    @property
    def labelsettings(self):
        """Return a list of the labelsettings in the XML file.
        The structure of the property:
        labelsettings = [
            {
                'name': str
                'labelsettings': QgsPalLayerSettings???
            }
        ]
        """
        return self._labelsettings

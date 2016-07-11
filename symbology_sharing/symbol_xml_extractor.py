# coding=utf-8
from xml.dom.minidom import parse


class SymbolXMLExtractor():
    """A class which parses the given file and returns the symbols"""
    def __init__(self, xml_file):
        self._xml_dom = parse(xml_file)
        self._symbols = []
        self._colorramps = []

        # Parse the xml to get the symbols and colorramps
        self.parse_xml()

    def parse_xml(self):
        symbols_dom = self._xml_dom.getElementsByTagName("symbol")
        colorramps_dom = self._xml_dom.getElementsByTagName("colorramp")

        self._symbols = []
        for symbol_dom in symbols_dom:
            symbol = {
                'name': symbol_dom.getAttribute('name'),
                'xml': symbol_dom.toxml()
            }
            self._symbols.append(symbol)

        self._colorramps = []
        for colorramp_dom in colorramps_dom:
            colorramp = {
                'name': colorramp_dom.getAttribute('name'),
                'xml': colorramp_dom.toxml()
            }
            self._colorramps.append(colorramp)

    @property
    def symbols(self):
        return self._symbols

    @property
    def colorramps(self):
        return self._colorramps

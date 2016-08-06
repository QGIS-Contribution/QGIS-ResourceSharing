# coding=utf-8
from qgis.testing import start_app, unittest
import nose2

from qgis.core import (
    QgsVectorColorBrewerColorRampV2,
    QgsVectorGradientColorRampV2,
    QgsVectorRandomColorRampV2,
    QgsFillSymbolV2,
    QgsLineSymbolV2,
    QgsMarkerSymbolV2)

from resource_sharing.symbol_xml_extractor import SymbolXMLExtractor
from utilities import test_data_path


class TestSymbolXMLExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def test_parse_xml(self):
        """Test parsing the xml works correctly."""
        xml_path = test_data_path(
            'collections', 'test_collection', 'symbol', 'various_symbols.xml' )
        extractor = SymbolXMLExtractor(xml_path)
        # There are 9 symbols and 3 colorramps there
        expected_symbols = {
            'fill_raster': QgsFillSymbolV2,
            'fill_svg': QgsFillSymbolV2,
            'fill_svg_line': QgsFillSymbolV2,
            'line_arrow': QgsLineSymbolV2,
            'line_svg_marker': QgsLineSymbolV2,
            'marker_ellipse': QgsMarkerSymbolV2,
            'marker_font': QgsMarkerSymbolV2,
            'marker_simple': QgsMarkerSymbolV2,
            'marker_svg': QgsMarkerSymbolV2
        }
        self.assertEqual(len(extractor.symbols), len(expected_symbols))
        for symbol in extractor.symbols:
            self.assertTrue(
                isinstance(symbol['symbol'], expected_symbols[symbol['name']])
            )
        expected_colorramps = {
            'cr_colorbrewer': QgsVectorColorBrewerColorRampV2,
            'cr_gradient': QgsVectorGradientColorRampV2,
            'cr_random': QgsVectorRandomColorRampV2
        }
        self.assertEqual(len(extractor.colorramps), len(expected_colorramps))
        for colorramp in extractor.colorramps:
            self.assertTrue(
                isinstance(colorramp['colorramp'],
                           expected_colorramps[colorramp['name']])
            )


if __name__ == "__main__":
    nose2.main()

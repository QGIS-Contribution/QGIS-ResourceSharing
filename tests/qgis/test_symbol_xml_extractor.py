#! python3  # noqa E265

"""
    Test symbol collections extractor.

    From unittest: `python -m unittest tests.qgis.test_symbol_xml_extractor`
"""

from qgis.core import QgsColorBrewerColorRamp, QgsFillSymbol, QgsGradientColorRamp
from qgis.core import QgsLimitedRandomColorRamp as random_color_ramp  # <-- !!!!
from qgis.core import QgsLineSymbol, QgsMarkerSymbol
from qgis.testing import unittest

from qgis_resource_sharing.symbol_xml_extractor import SymbolXMLExtractor

try:
    from .utilities import test_data_path
except ImportError:
    from tests.qgis.utilities import test_data_path


class TestSymbolXMLExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        pass

    def test_parse_xml(self):
        """Test parsing the xml works correctly."""
        xml_path = test_data_path(
            "repository_dummy",
            "collections",
            "test_collection",
            "symbol",
            "various_symbols.xml",
        )
        extractor = SymbolXMLExtractor(xml_path)
        self.assertTrue(extractor.parse_xml())
        # There are 9 symbols and 3 colorramps there
        expected_symbols = {
            "fill_raster": QgsFillSymbol,
            "fill_svg": QgsFillSymbol,
            "fill_svg_line": QgsFillSymbol,
            "line_arrow": QgsLineSymbol,
            "line_svg_marker": QgsLineSymbol,
            "marker_ellipse": QgsMarkerSymbol,
            "marker_font": QgsMarkerSymbol,
            "marker_simple": QgsMarkerSymbol,
            "marker_svg": QgsMarkerSymbol,
        }
        self.assertEqual(len(extractor.symbols), len(expected_symbols))
        for symbol in extractor.symbols:
            self.assertTrue(
                isinstance(symbol["symbol"], expected_symbols[symbol["name"]])
            )
        expected_colorramps = {
            "cr_colorbrewer": QgsColorBrewerColorRamp,
            "cr_gradient": QgsGradientColorRamp,
            "cr_random": random_color_ramp,  # QGIS 2.x is QgsRandomColorRamp QGIS 3.x is QgsLimitedRandomColorRamp
        }
        self.assertEqual(len(extractor.colorramps), len(expected_colorramps))
        for colorramp in extractor.colorramps:
            self.assertTrue(
                isinstance(
                    colorramp["colorramp"], expected_colorramps[colorramp["name"]]
                )
            )


if __name__ == "__main__":
    unittest.main()

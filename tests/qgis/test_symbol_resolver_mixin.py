#! python3  # noqa E265

"""
    Test symbol collections extractor.

    From unittest: `python -m unittest tests.qgis.test_symbol_resolver_mixin`
"""

from qgis.PyQt.QtCore import QUrl
from qgis.testing import start_app, unittest

from qgis_resource_sharing.resource_handler.symbol_resolver_mixin import (
    fix_xml_node,
    resolve_path,
)
from tests.qgis.utilities import test_data_path


class TestSymbolResolverMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()
        cls.collection_path = test_data_path(
            "repository_dummy", "collections", "test_collection"
        )

    def _to_str(self, buffer):
        """For Py3 compat, this will transform a byte into string"""
        if type(buffer) == "str":
            return buffer
        return buffer.decode("utf-8")

    def test_fix_xml_node(self):
        """Test if fixing xml node works."""
        symbol_xml = """
            <symbol alpha="1" clip_to_extent="1" type="fill" name="fill_raster">
                <layer pass="0" class="RasterFill" locked="0">
                    <prop k="alpha" v="1"/>
                    <prop k="angle" v="0"/>
                    <prop k="coordinate_mode" v="0"/>
                    <prop k="imageFile" v="/you/will/not/find/pikachu.png"/>
                    <prop k="offset" v="0,0"/>
                    <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
                    <prop k="offset_unit" v="MM"/>
                    <prop k="width" v="0"/>
                    <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
                    <prop k="width_unit" v="Pixel"/>
                </layer>
            </symbol>
        """
        collection_path = test_data_path(
            "repository_dummy", "collections", "test_collection"
        )
        fixed_xml = self._to_str(fix_xml_node(symbol_xml, collection_path, []))
        expected_xml = """<symbol alpha="1" clip_to_extent="1" name="fill_raster" type="fill">
                <layer class="RasterFill" locked="0" pass="0">
                    <prop k="alpha" v="1" />
                    <prop k="angle" v="0" />
                    <prop k="coordinate_mode" v="0" />
                    <prop k="imageFile" v="{0}/collections/test_collection/image/pikachu.png" />
                    <prop k="offset" v="0,0" />
                    <prop k="offset_map_unit_scale" v="0,0,0,0,0,0" />
                    <prop k="offset_unit" v="MM" />
                    <prop k="width" v="0" />
                    <prop k="width_map_unit_scale" v="0,0,0,0,0,0" />
                    <prop k="width_unit" v="Pixel" />
                </layer>
            </symbol>""".format(
            test_data_path()
        )

        self.assertEqual(fixed_xml, expected_xml)

    def test_resolve_path_local(self):
        """Test resolving the path works correctly."""
        search_paths = []
        img_path = test_data_path(
            "repository_dummy", "collections", "test_collection", "svg", "blastoise.svg"
        )
        fixed_path = resolve_path(img_path, self.collection_path, search_paths)
        self.assertEqual(img_path, fixed_path)

    def test_resolve_path_local_url(self):
        """Test resolving local url works correctly."""
        search_paths = []
        img_path = test_data_path(
            "repository_dummy", "collections", "test_collection", "svg", "blastoise.svg"
        )
        img_url = QUrl.fromLocalFile(img_path)
        fixed_path = resolve_path(
            img_url.toString(), self.collection_path, search_paths
        )
        self.assertEqual(fixed_path, img_path)

    def test_resolve_path_http_url(self):
        """Test resolving the path for an HTTP URL."""
        search_paths = []
        img_path = "http://qgis.org/test/image.svg"
        img_url = QUrl(img_path)
        fixed_path = resolve_path(
            img_url.toString(), self.collection_path, search_paths
        )
        self.assertEqual(fixed_path, img_path)

    def test_resolve_path_local_collection_svg(self):
        """Test resolving the path works correctly."""
        search_paths = []

        # Test case 4: checking in the svg local collection path
        img_path = "/you/would/not/find/this/charizard.svg"
        fixed_path = resolve_path(img_path, self.collection_path, search_paths)
        expected_path = test_data_path(
            "repository_dummy", "collections", "test_collection", "svg", "charizard.svg"
        )
        self.assertEqual(fixed_path, expected_path)

    def test_resolve_path_local_collection_image(self):
        """Test resolving the path checking in the image local collection path."""
        search_paths = []
        img_path = "/you/would/not/find/this/pikachu.png"
        fixed_path = resolve_path(img_path, self.collection_path, search_paths)
        expected_path = test_data_path(
            "repository_dummy", "collections", "test_collection", "image", "pikachu.png"
        )
        self.assertEqual(fixed_path, expected_path)

    def test_resolve_path_search_paths(self):
        """Test resolving the path works correctly."""
        search_paths = [
            test_data_path(
                "repository_dummy", "collections", "test_collection", "preview"
            )
        ]
        img_path = "prev_1.png"
        fixed_path = resolve_path(img_path, self.collection_path, search_paths)
        expected_path = test_data_path(
            "repository_dummy",
            "collections",
            "test_collection",
            "preview",
            "prev_1.png",
        )
        self.assertEqual(fixed_path, expected_path)

    def test_resolve_path_not_found(self):
        """Test resolving the path not finding anywhere (return the original path)."""
        search_paths = []

        img_path = "/you/would/not/find/this/anywhere.png"
        fixed_path = resolve_path(img_path, self.collection_path, search_paths)
        self.assertEqual(fixed_path, img_path)


if __name__ == "__main__":
    unittest.main()

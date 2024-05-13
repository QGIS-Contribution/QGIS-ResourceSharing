#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_plg_metadata
        # for specific test
        python -m unittest tests.test_plg_metadata.TestPluginMetadata.test_version_semver
"""

# standard library
import unittest
from configparser import ConfigParser
from pathlib import Path

# 3rd party
from packaging.version import parse

# project
from qgis_resource_sharing import __about__

# ############################################################################
# ########## Classes #############
# ################################


class TestPluginMetadata(unittest.TestCase):
    """Test QGIS plugin metadata."""

    def test_metadata_types(self):
        """Test types."""
        # plugin metadata.txt file
        self.assertIsInstance(__about__.PLG_METADATA_FILE, Path)
        self.assertTrue(__about__.PLG_METADATA_FILE.is_file())

        # plugin dir
        self.assertIsInstance(__about__.DIR_PLUGIN_ROOT, Path)
        self.assertTrue(__about__.DIR_PLUGIN_ROOT.is_dir())

        # metadata as dict
        self.assertIsInstance(__about__.__plugin_md__, dict)

        # general
        self.assertIsInstance(__about__.__author__, str)
        self.assertIsInstance(__about__.__copyright__, str)
        self.assertIsInstance(__about__.__email__, str)
        self.assertIsInstance(__about__.__keywords__, list)
        self.assertIsInstance(__about__.__license__, str)
        self.assertIsInstance(__about__.__summary__, str)
        self.assertIsInstance(__about__.__title__, str)
        self.assertIsInstance(__about__.__title_clean__, str)
        self.assertIsInstance(__about__.__version__, str)
        self.assertIsInstance(__about__.__version_info__, tuple)

        # misc
        self.assertLessEqual(len(__about__.__title_clean__), len(__about__.__title__))

        # QGIS versions
        # QGIS versions
        self.assertIsInstance(
            __about__.__plugin_md__.get("general").get("qgisminimumversion"), str
        )

        self.assertIsInstance(
            __about__.__plugin_md__.get("general").get("qgismaximumversion"), str
        )

        min_version_parsed = parse(
            __about__.__plugin_md__.get("general").get("qgisminimumversion")
        )
        max_version_parsed = parse(
            __about__.__plugin_md__.get("general").get("qgismaximumversion")
        )
        self.assertLessEqual(min_version_parsed, max_version_parsed)

    def test_required_metadata(self):
        """Test that the plugin __init__ will validate on plugins.qgis.org."""

        required_metadata: list = [
            "about",
            "author",
            "description",
            "email",
            "name",
            "qgisMinimumVersion",
            "repository",
            "version",
        ]

        # check file exists
        metatadata_path: Path = (
            Path(__file__).parent.parent.parent / "qgis_resource_sharing/metadata.txt"
        )
        self.assertTrue(metatadata_path.is_file())

        # load
        config = ConfigParser()
        config.optionxform = str
        config.read(metatadata_path, encoding="UTF-8")

        # check section
        self.assertTrue(config.has_section("general"))
        section = config.options("general")

        # check required metadata
        for md in required_metadata:
            self.assertIn(md, section)

    def test_version_semver(self):
        """Test if version comply with semantic versioning."""
        self.assertTrue(parse(__about__.__version__))


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()

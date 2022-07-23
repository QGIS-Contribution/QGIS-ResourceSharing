#! python3  # noqa E265

"""
    Base class for unit tests on QGIS.
"""

# standard library
import logging
from pathlib import Path

# conditional import
try:
    from qgis.testing import unittest

    IS_PYQGIS_AVAILABLE: bool = True
except ImportError:
    import unittest

    IS_PYQGIS_AVAILABLE: bool = False

# ############################################################################
# ########## Classes #############
# ################################


class BaseTestPlugin(unittest.TestCase):
    """Base test class for plugin."""

    IS_PYQGIS_AVAILABLE: bool = IS_PYQGIS_AVAILABLE

    def get_fixtures_path(self, *args) -> Path:
        """Return the absolute path to the InaSAFE test data or directory path.

        :param args: List of path e.g. ['control', 'files',
            'test-error-message.txt'] or ['control', 'scenarios'] to get the path
            to scenarios dir.
        :type args: list

        :return: Absolute path to the test data or dir path.
        :rtype: Path
        """
        # get fixtures data folder path
        fixtures_data_dir = Path("tests/fixtures")
        if not fixtures_data_dir.exists():
            logging.warning(
                f"Fixtures folder ({fixtures_data_dir}) is not reachable starting "
                "from plugin folder. Trying to get it as relative path..."
            )
            fixtures_data_dir = Path(__file__).parent.parent / "fixtures"
            if not fixtures_data_dir.exists():
                raise FileNotFoundError(
                    f"Fixtures folder not found: {fixtures_data_dir}"
                )

        # build absolute path for asked files
        for item in args:
            item_path = fixtures_data_dir.joinpath(item)

        return item_path.absolute()

    def get_sample_repository_url(self, repository_name: str = "dummy") -> str:
        """Return the test repository URL on file system.

        :return: The test repository URL string
        :rtype: str
        """
        return self.get_fixtures_path(f"repository_{repository_name}").as_uri()

import os
from pathlib import Path

from qgis.PyQt.QtCore import QUrl


def test_data_path(*args):
    """Return the absolute path to the InaSAFE test data or directory path.

    :param args: List of path e.g. ['control', 'files',
        'test-error-message.txt'] or ['control', 'scenarios'] to get the path
        to scenarios dir.
    :type args: list

    :return: Absolute path to the test data or dir path.
    :rtype: str

    """
    # get fixtures data folder path
    fixtures_data_dir = Path(__file__).parent.parent / "fixtures"
    if not fixtures_data_dir.exists():
        raise FileNotFoundError(fixtures_data_dir)
    # build absolute path for asked files
    for item in args:

        fixtures_data_dir = os.path.abspath(os.path.join(fixtures_data_dir, item))

    return fixtures_data_dir


def test_repository_url() -> str:
    """Return the test repository URL on file system.

    :return: The test repository URL string
    :rtype: str
    """
    test_fixtures_path = test_data_path()
    if isinstance(test_fixtures_path, Path):
        test_fixtures_path = str(test_fixtures_path.resolve())
    return QUrl.fromLocalFile(test_fixtures_path).toString()

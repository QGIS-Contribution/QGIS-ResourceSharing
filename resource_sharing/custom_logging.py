# coding=utf-8
import logging

from qgis.core import QgsMessageLog


def setup_logger():
    """Setup logger for the plugin. Should be called only once."""
    logger = logging.getLogger('QGIS Resources Sharing')
    logger.setLevel(logging.DEBUG)
    # Add handler for qgis logger
    qgis_handler = QgisLogger()
    logger.addHandler(qgis_handler)


class QgisLogger(logging.Handler):
    """A custom logger to emit the log to qgis message log."""

    def __init__(self):
        logging.Handler.__init__(self)

        fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)

    def emit(self, record):
        """
        Do whatever it takes to actually log the specified logging record.

        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.
        """
        QgsMessageLog.logMessage(
            record.getMessage(),
            'QGIS Resource Sharing',
            level=QgsMessageLog.CRITICAL)

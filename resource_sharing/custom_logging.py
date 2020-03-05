# coding=utf-8
import logging

from qgis.core import QgsMessageLog, Qgis

LOGGERNAME = 'QGIS Resource Sharing'


def setup_logger():
    """Setup logger for the plugin. Should be called only once."""
    logger = logging.getLogger(LOGGERNAME)
    # logger.setLevel(logging.DEBUG)  # Development
    logger.setLevel(logging.INFO)  # Deploy
    # Add handler for qgis logger once
    qgis_handler = QgisLogger()
    is_registered = False
    handler_class_name = qgis_handler.__class__.__name__
    for logger_handler in logger.handlers:
        if logger_handler.__class__.__name__ == handler_class_name:
            is_registered = True
            break
    if not is_registered:
        logger.addHandler(qgis_handler)


class QgisLogger(logging.Handler):
    """A custom logger to emit the log to the QGIS message log."""

    def __init__(self):
        logging.Handler.__init__(self)
        fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)

    def emit(self, record):
        """
        Do whatever it takes to actually log the specified logging record.
        """
        qgislevel = Qgis.Info  # for NOTSET, DEBUG and INFO
        # Mapping CRITICAL to Qgis.Critical and ERROR to Qgis.Warning:
        if record.levelno == logging.CRITICAL:
            qgislevel = Qgis.Critical
        elif record.levelno == logging.ERROR:
            qgislevel = Qgis.Warning
        elif record.levelno == logging.WARNING:
            qgislevel = Qgis.Warning

        QgsMessageLog.logMessage(
            record.getMessage(),
            LOGGERNAME,
            level=qgislevel)

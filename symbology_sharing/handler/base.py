# coding=utf-8
"""This module contains the base class of repository handler."""

__author__ = 'akbargumbira@gmail.com'
__revision__ = '$Format:%H$'
__date__ = '15/03/15'


class HandlerMeta(type):
    """Handler meta class definition."""
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # This is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # This is a derived class.
            # Add the class if it's not disabled
            if not cls.IS_DISABLED:
                interface_id = name.lower()
                cls.registry[interface_id] = cls

        super(HandlerMeta, cls).__init__(name, bases, dct)


class BaseHandler(object):
    """Abstract class of handler."""
    __metaclass__ = HandlerMeta

    METADATA_FILE = 'metadata.ini'
    IS_DISABLED = False

    def __init__(self, url):
        """Constructor of the base class."""
        self._url = None
        self._metadata = None

        # Call proper setters here
        self.url = url

    def can_handle(self):
        """Checking if handler can handle this URL."""
        raise NotImplementedError

    @property
    def url(self):
        """The URL to the repository.

        Example:
        - https://github.com/anitagraser/QGIS-style-repo-dummy.git
        - file://home/akbar/dev/qgis-style-repo-dummy
        """
        return self._url

    @url.setter
    def url(self, url):
        """Setter to the repository's URL."""
        self._url = url

    @property
    def metadata(self):
        return self._metadata

    def fetch_metadata(self):
        """Fetch the content of the metadata."""
        raise NotImplementedError

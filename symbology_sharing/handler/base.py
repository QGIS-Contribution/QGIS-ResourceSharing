# coding=utf-8


class HandlerMeta(type):
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
    __metaclass__ = HandlerMeta

    METADATA_FILE = 'metadata.ini'
    IS_DISABLED = False

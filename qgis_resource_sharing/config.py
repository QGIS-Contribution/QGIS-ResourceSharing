from enum import IntEnum

"""
# Put the COLLECTIONS object (dict) in the module namespace
# (http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm)

Call this variable as an attribute from the config module e.g:
    from qgis_resource_sharing import config
    print config.COLLECTIONS

config.COLLECTIONS is a dict that contains metadata for the
collections. It has this structure:
    config.COLLECTIONS = {
        collection_id(computed): {
            'register_name': collection,
            'author': author,
            'author_email': email,
            'repository_url': self.url,
            'repository_name': <the name of the repository>,
            'status': CollectionStatus.NOT_INSTALLED,
            'name': parser.get(collection, 'name'),
            'tags': parser.get(collection, 'tags'),
            'description': parser.get(collection, 'description'),
            'qgis_min_version': parser.get(collection, 'qgis_minimum_version'),
            'qgis_max_version': parser.get(collection, 'qgis_maximum_version')
            'preview': ['preview/image1.png', 'preview/image2.png']
            # Additional entries (for resource statistics):
            'models': count of models in the collection,
            'expressions': count of expression files in the collection,
            'processing': count of processing scripts in the collection,
            'rscripts': count of R scripts in the collection,
            'style': count of layer styles (QML) in the collection,
            'svg': count of SVGs in the collection,
            'symbol': count of symbol files (XML) in the collection,
        },
        ....
    }
"""


class CollectionStatus(IntEnum):
    """Describe the status of a collection"""

    NOT_INSTALLED = 0
    INSTALLED = 1
    ALL = 2


COLLECTIONS = {}

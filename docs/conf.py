#!python3

"""
Configuration for project documentation using Sphinx.
"""

# standard
import sys
from datetime import datetime
from os import environ, path

sys.path.insert(0, path.abspath(".."))

# Package
from qgis_resource_sharing import __about__

# -- Build environment -----------------------------------------------------
on_rtd = environ.get("READTHEDOCS", None) == "True"

# -- Project information -----------------------------------------------------
author = __about__.__author__
copyright = __about__.__copyright__
description = __about__.__summary__
project = __about__.__title__
version = release = __about__.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # Sphinx included
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    # 3rd party
    "myst_parser",
    "sphinx_copybutton",
    "sphinxext.opengraph",
]


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
autosectionlabel_prefix_document = True
# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", ".venv", "Thumbs.db", ".DS_Store", "_output", "ext_libs"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# -- Options for HTML output -------------------------------------------------

# -- Theme
html_favicon = "assets/img/icon.png"
html_logo = "assets/img/icon.png"
html_static_path = ["assets"]
html_theme = "furo"

# -- EXTENSIONS --------------------------------------------------------

# Configuration for intersphinx (refer to others docs).
intersphinx_mapping = {
    "PyQt5": ("https://www.riverbankcomputing.com/static/Docs/PyQt5", None),
    "python": ("https://docs.python.org/3/", None),
    "qgis": ("https://qgis.org/pyqgis/master/", None),
}

# MyST Parser
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
]

myst_substitutions = {
    "author": author,
    "date_update": datetime.now().strftime("%d %B %Y"),
    "description": description,
    "qgis_version_max": __about__.__plugin_md__.get("general").get(
        "qgismaximumversion"
    ),
    "qgis_version_min": __about__.__plugin_md__.get("general").get(
        "qgisminimumversion"
    ),
    "repo_url": __about__.__uri__,
    "title": project,
    "version": version,
}

myst_url_schemes = ("http", "https", "mailto")

# OpenGraph
ogp_image = "https://qgis-contribution.github.io/QGIS-ResourceSharing/_images/collection_preview.png"
ogp_site_name = project
ogp_site_url = __about__.__uri_homepage__
ogp_custom_meta_tags = [
    "<meta name='twitter:card' content='summary_large_image'>",
    f'<meta property="twitter:description" content="{description}" />',
    f'<meta property="twitter:image" content="{ogp_image}" />',
    f'<meta property="twitter:title" content="{project}" />',
]

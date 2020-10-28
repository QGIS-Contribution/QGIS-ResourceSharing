"""
Test Suite

Contact : elpaso at gmail dot com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import os
import sys
import unittest

import qgis  # NOQA  For SIP API to V2 if run outside of QGIS
from qgis.PyQt import Qt

# Add ext-libs directory
sys.path.insert(2, os.path.join(os.path.dirname(__file__), "ext_libs"))

# Dulwich tries to call sys.argv while in QGIS, argv module is missing
if not hasattr(sys, "argv"):
    sys.argv = []

sys.path.insert(0, os.path.dirname(__file__))

PLUGIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)

EXT_LIBS_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, "ext_libs"))
if EXT_LIBS_DIR not in sys.path:
    sys.path.insert(0, EXT_LIBS_DIR)


def _run_tests(test_suite, package_name):
    """Core function to test a test suite."""
    count = test_suite.countTestCases()
    print("########")
    print("%s tests has been discovered in %s" % (count, package_name))
    print("QT : %s" % Qt.QT_VERSION)
    print("########")
    return unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(test_suite)


def test_qgis3():
    """Run all QGIS3 tests"""
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover("test")
    return _run_tests(test_suite, "test")


if __name__ == "__main__":
    result = test_qgis3()
    sys.exit(0 if result.wasSuccessful() else 1)

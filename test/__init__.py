# import qgis libs so that ve set the correct sip api version
import os
import sys

import qgis  # pylint: disable=W0611  # NOQA

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "ext_libs"))
)

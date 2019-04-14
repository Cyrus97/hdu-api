# -*- coding: utf-8 -*-

#
#     __  __ ____   __  __        ___     ____   ____
#    / / / // __ \ / / / /       /   |   / __ \ /  _/
#   / /_/ // / / // / / /______ / /| |  / /_/ / / /
#  / __  // /_/ // /_/ //_____// ___ | / ____/_/ /
# /_/ /_//_____/ \____/       /_/  |_|/_/    /___/
#
#

"""
HDU-API
-------

HDU-API is a simple sdk for hdu to access the information in the school's websites, written in Python,
basing on the requests library and the bs4 library mainly.
"""

hard_dependencies = ("requests", "bs4", "lxml")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, missing_dependencies

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__

from .api import HDU, Client
from .sessions import SessionManager, TeachingSession, CardSession, StudentSession, IHDUSession, IHDUPhoneSession
from .models import Card, Exam, Course, Person, Public, get_current_term

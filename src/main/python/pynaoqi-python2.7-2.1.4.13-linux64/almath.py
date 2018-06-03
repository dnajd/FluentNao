""" Helper module to make sure
almath.py works in a relocatable Python
SDK

"""

import os
import sys
import ctypes


def load_almath():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    libalmath = os.path.join(this_dir, "libalmath.so")
    if os.path.exists(libalmath):
        # we are likely to be in a relocatable SDK,
        # load the library so that setting LD_LIBRARY_PATH
        # is not necessary
        ctypes.cdll.LoadLibrary(libalmath)


if sys.platform.startswith("linux"):
    try:
        load_almath()
    except Exception, e:
        print e

from almathswig import *

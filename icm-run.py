#!venv/bin/python
"""Run icm for debugging"""
# ------------------------------------------------
# -- Run icm for debugging
# -- It is not part of icm (it is not installed).
# --  It is just a launcher for the developers
#-------------------------------------------------

import sys

# -- Import the apio entry point
from icm.__main__ import cli as icm

#-- Run apio!
try:
    icm(None)

#-- Apio commands finish with this excepcion
except SystemExit:
    print("")
    print("icm command executed!")

#-- Exit!
sys.exit()

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\pdfalyzer\util\debugging.py

import logging


# Starting pdb.set_trace() this way kind of sucks because yr locals are messed up
def debugger():
    import pdb

    pdb.set_trace(locals())

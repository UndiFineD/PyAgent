# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\pdfalyzer.py\util.py\debugging_5f1c77b70765.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\pdfalyzer\util\debugging.py

import logging

# Starting pdb.set_trace() this way kind of sucks because yr locals are messed up


def debugger():
    import pdb

    pdb.set_trace(locals())

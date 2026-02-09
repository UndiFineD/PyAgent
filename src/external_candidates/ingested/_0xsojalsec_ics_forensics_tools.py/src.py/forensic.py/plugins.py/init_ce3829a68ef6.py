# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\plugins\__init__.py
from forensic.plugins.CodeSysV3.CodeSysV3 import CodeSysV3
from forensic.plugins.s7.s7 import S7

__plugins__ = {"S7": S7, "CodeSysV3": CodeSysV3}

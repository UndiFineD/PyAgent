# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\analyzers\__init__.py
from forensic.analyzers.CodeSysV3.block_logic import CS3BlockLogic
from forensic.analyzers.CodeSysV3.raw_file_parser import CS3RawFileParser
from forensic.analyzers.s7.block_logic import S7BlockLogic
from forensic.analyzers.s7.online_offline_compare import S7OnlineOfflineCompare
from forensic.analyzers.s7.raw_file_parser import S7RawFileParser

__analyzers__ = {
    "S7BlockLogic": S7BlockLogic,
    "S7RawFileParser": S7RawFileParser,
    "S7OnlineOfflineCompare": S7OnlineOfflineCompare,
    "CS3BlockLogic": CS3BlockLogic,
    "CS3RawFileParser": CS3RawFileParser,
}

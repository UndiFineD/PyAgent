# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\__init__.py
import forensic.analyzers
import forensic.plugins

__resources__ = {**forensic.plugins.__plugins__, **forensic.analyzers.__analyzers__}

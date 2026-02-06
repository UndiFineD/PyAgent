# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LitterBox\app\analyzers\dynamic\base.py
# app/analyzers/dynamic/base.py
from ..base import BaseAnalyzer


class DynamicAnalyzer(BaseAnalyzer):
    def __init__(self, config):
        super().__init__(config)
        self.pid = None

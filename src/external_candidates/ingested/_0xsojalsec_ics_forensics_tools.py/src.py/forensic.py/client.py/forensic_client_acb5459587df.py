# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\client\forensic_client.py
from pathlib import Path
from typing import List

from forensic.client.application import Application
from forensic.interfaces.plugin import PluginConfig


class ForensicClient(Application):
    def __init__(self):
        super().__init__()

    def scan(
        self,
        config: List[PluginConfig],
        multiprocess: bool = False,
        output_dir: Path = None,
        verbose: Path = None,
    ):
        super().scan(config, multiprocess, output_dir, verbose)

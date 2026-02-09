# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\rich\_extension.py
from typing import Any


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from pip._vendor.rich.pretty import install
    from pip._vendor.rich.traceback import install as tr_install

    install()
    tr_install()

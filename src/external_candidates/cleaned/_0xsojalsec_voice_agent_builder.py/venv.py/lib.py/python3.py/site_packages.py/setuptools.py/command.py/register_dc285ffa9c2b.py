# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\setuptools\command\register.py
import distutils.command.register as orig
from distutils import log

from setuptools.errors import RemovedCommandError


class register(orig.register):
    """Formerly used to register packages on PyPI."""

    def run(self):
        msg = "The register command has been removed, use twine to upload " + "instead (https://pypi.org/p/twine)"

        self.announce("ERROR: " + msg, log.ERROR)

        raise RemovedCommandError(msg)

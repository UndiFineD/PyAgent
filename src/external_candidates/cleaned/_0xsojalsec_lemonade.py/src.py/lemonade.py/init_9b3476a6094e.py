# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-lemonade\src\lemonade\__init__.py
from lemonade.version import __version__

from .cli import main as lemonadecli
from .state import State, load_state

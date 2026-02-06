# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NetExec\nxc\helpers\bash.py
import os

from nxc.paths import DATA_PATH


def get_script(path):
    with open(os.path.join(DATA_PATH, path)) as script:
        return script.read()

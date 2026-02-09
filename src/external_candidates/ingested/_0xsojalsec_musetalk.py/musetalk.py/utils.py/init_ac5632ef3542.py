# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-MuseTalk\musetalk\utils\__init__.py
import sys
from os.path import abspath, dirname

current_dir = dirname(abspath(__file__))
parent_dir = dirname(current_dir)
sys.path.append(parent_dir + "/utils")

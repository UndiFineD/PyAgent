# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\certifi\__main__.py
import argparse

from pip._vendor.certifi import contents, where

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contents", action="store_true")
args = parser.parse_args()

if args.contents:
    print(contents())
else:
    print(where())

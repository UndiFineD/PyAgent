# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-KernelSU\scripts\abi_gki_all.py
import sys
import xml.dom.minidom
from xml.dom.minidom import parse

DOMTree = xml.dom.minidom.parse(sys.argv[1])
symbols = DOMTree.getElementsByTagName("elf-symbol")
print("[abi_symbol_list]")
for symbol in symbols:
    print("  " + symbol.getAttribute("name"))

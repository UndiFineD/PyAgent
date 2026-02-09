# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-porch-pirate\examples\search.py
import sys

sys.path.append("../src/porch-pirate")
from porchpirate import porchpirate


def main():
    p = porchpirate()
    print(p.search("bell.ca", indice="workspace"))  # Search custom indice with keyword
    print(p.search("bell.ca"))  # Regular search


if __name__ == "__main__":
    main()

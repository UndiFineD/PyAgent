# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-porch-pirate\examples\search_by_page.py
import sys

sys.path.append("../src/porch-pirate")
from porchpirate import porchpirate


def main():
    p = porchpirate()
    print(
        p.search("bell.ca", page=2, indice="workspace")
    )  # Search custom indice with keyword
    print(p.search("bell.ca"))  # Regular search


if __name__ == "__main__":
    main()

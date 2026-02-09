# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-porch-pirate\examples\get_collections.py
import sys

sys.path.append("../src/porch-pirate")
from porchpirate import porchpirate


def main():
    p = porchpirate()
    print(p.collections("4127fdda-08be-4f34-af0e-a8bdc06efaba"))


if __name__ == "__main__":
    main()

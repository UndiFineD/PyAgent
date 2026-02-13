# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-porch-pirate\examples\get_profile.py
import json
import sys

sys.path.append("../src/porch-pirate")
from porchpirate import porchpirate


def main():
    p = porchpirate()
    profile = json.loads(p.profile("redacted"))
    print(profile)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Helper script to invoke pytest with reproducible quoting."""
import sys
import pytest

if __name__ == "__main__":
    # forward any args after the script
    args = sys.argv[1:]
    # default to verbose and maxfail 1 if none provided
    if not args:
        args = ["-v", "--maxfail=1"]
    sys.exit(pytest.main(args))

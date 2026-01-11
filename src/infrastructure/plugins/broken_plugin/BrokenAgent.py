#!/usr/bin/env python3

"""Plugin containing intentional syntax errors for resilience testing."""

# DANGER: Intentional syntax error to test resilience
class BrokenAgent:
    def __init__(self) -> None:
        # this is not valid python code !!!
        pass

#!/usr/bin/env python3
"""Shared helper functions used by development utilities."""

import json
import logging
from typing import Any


def load_config(path: str) -> Any:
    """Load JSON or TOML configuration file from disk."""
    # placeholder uses json only for now
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name, configured to output to console."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
    return logger

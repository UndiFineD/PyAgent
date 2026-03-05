#!/usr/bin/env python3
"""Minimal CrossPlatformHelper shim."""


class CrossPlatformHelper:
    @staticmethod
    def normalize_path(p):
        return p


__all__ = ["CrossPlatformHelper"]

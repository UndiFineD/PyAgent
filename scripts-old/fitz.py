#!/usr/bin/env python3
"""Lightweight shim for PyMuPDF (`fitz`) used during tests.

This provides a minimal `open()` / `Document` / `Page` API so imports succeed
when tests only need basic objects. Keep minimal to avoid side effects.
"""
class Page:
    def __init__(self, text=""):
        self._text = text

    def get_text(self, *args, **kwargs):
        return self._text


class Document:
    def __init__(self, path=None):
        # simple single-empty-page document
        self._pages = [Page("")]

    def __len__(self):
        return len(self._pages)

    def __getitem__(self, idx):
        return self._pages[idx]

    def load_page(self, idx):
        return self._pages[idx]


def open(path=None):
    return Document(path)


__all__ = ["open", "Document", "Page"]

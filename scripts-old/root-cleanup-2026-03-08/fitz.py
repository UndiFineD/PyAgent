import importlib.util
import os
import sys

# Load the shim from scripts/fitz.py so tests importing `fitz` get the shim.
_shim_path = os.path.join(os.path.dirname(__file__), "scripts", "fitz.py")
if os.path.exists(_shim_path):
    spec = importlib.util.spec_from_file_location("_project_fitz_shim", _shim_path)
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    # Re-export public names
    for _name in getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")]):
        try:
            globals()[_name] = getattr(_mod, _name)
        except AttributeError:
            pass
    __all__ = getattr(_mod, "__all__", [])
else:
    # Fallback minimal API if scripts/fitz.py missing
    class Page:
        def __init__(self, text=""):
            self._text = text
        def get_text(self, *a, **k):
            return self._text

    class Document:
        def __init__(self, path=None):
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

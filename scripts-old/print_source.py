"""Script to print the source code of a module."""
import sys
import pathlib
import inspect
import src.infrastructure.fleet.mixins.FleetLookupMixin as mod

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
print(inspect.getsource(mod))

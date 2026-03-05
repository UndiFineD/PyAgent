import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import inspect
import src.infrastructure.fleet.mixins.FleetLookupMixin as mod
print(inspect.getsource(mod))

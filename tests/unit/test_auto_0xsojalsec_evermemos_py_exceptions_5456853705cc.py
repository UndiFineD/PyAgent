
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_exceptions_5456853705cc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DIException'), 'missing DIException'
assert hasattr(mod, 'CircularDependencyError'), 'missing CircularDependencyError'
assert hasattr(mod, 'BeanNotFoundError'), 'missing BeanNotFoundError'
assert hasattr(mod, 'DuplicateBeanError'), 'missing DuplicateBeanError'
assert hasattr(mod, 'FactoryError'), 'missing FactoryError'
assert hasattr(mod, 'DependencyResolutionError'), 'missing DependencyResolutionError'
assert hasattr(mod, 'MockNotEnabledError'), 'missing MockNotEnabledError'
assert hasattr(mod, 'PrimaryBeanConflictError'), 'missing PrimaryBeanConflictError'


import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_thread_with_result_b1bba477313f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ThreadWithReturnValue'), 'missing ThreadWithReturnValue'
assert hasattr(mod, 'ContextAwareFuture'), 'missing ContextAwareFuture'
assert hasattr(mod, 'ThreadPoolExecutorWithReturnValue'), 'missing ThreadPoolExecutorWithReturnValue'

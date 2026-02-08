
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_fetchers_a298e6b96d54.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_profile_nothing'), 'missing _profile_nothing'
assert hasattr(mod, '_DataFetcher'), 'missing _DataFetcher'
assert hasattr(mod, '_PrefetchDataFetcher'), 'missing _PrefetchDataFetcher'
assert hasattr(mod, '_DataLoaderIterDataFetcher'), 'missing _DataLoaderIterDataFetcher'
assert hasattr(mod, '_DataFetcherWrapper'), 'missing _DataFetcherWrapper'

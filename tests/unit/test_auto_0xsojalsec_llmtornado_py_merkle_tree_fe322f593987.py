
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llmtornado_py_merkle_tree_fe322f593987.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MerkleNode'), 'missing MerkleNode'
assert hasattr(mod, 'MerkleTree'), 'missing MerkleTree'

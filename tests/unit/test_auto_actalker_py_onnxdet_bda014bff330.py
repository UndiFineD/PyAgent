
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_onnxdet_bda014bff330.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'nms'), 'missing nms'
assert hasattr(mod, 'multiclass_nms'), 'missing multiclass_nms'
assert hasattr(mod, 'demo_postprocess'), 'missing demo_postprocess'
assert hasattr(mod, 'preprocess'), 'missing preprocess'
assert hasattr(mod, 'inference_detector'), 'missing inference_detector'

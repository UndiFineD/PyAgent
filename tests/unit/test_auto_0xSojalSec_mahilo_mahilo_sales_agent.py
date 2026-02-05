
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_mahilo_mahilo_sales_agent.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'analyze_lead_sources'), 'missing analyze_lead_sources'
assert hasattr(mod, 'collect_feature_feedback'), 'missing collect_feature_feedback'
assert hasattr(mod, 'generate_sales_insights'), 'missing generate_sales_insights'

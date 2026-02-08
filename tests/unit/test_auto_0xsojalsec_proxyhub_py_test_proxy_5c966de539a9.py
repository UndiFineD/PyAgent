
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_proxyhub_py_test_proxy_5c966de539a9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'proxy'), 'missing proxy'
assert hasattr(mod, 'test_create_by_ip'), 'missing test_create_by_ip'
assert hasattr(mod, 'test_create_by_domain'), 'missing test_create_by_domain'
assert hasattr(mod, 'test_repr'), 'missing test_repr'
assert hasattr(mod, 'test_as_json_w_geo'), 'missing test_as_json_w_geo'
assert hasattr(mod, 'test_as_json_wo_geo'), 'missing test_as_json_wo_geo'
assert hasattr(mod, 'test_schemes'), 'missing test_schemes'
assert hasattr(mod, 'test_avg_resp_time'), 'missing test_avg_resp_time'
assert hasattr(mod, 'test_error_rate'), 'missing test_error_rate'
assert hasattr(mod, 'test_geo'), 'missing test_geo'
assert hasattr(mod, 'test_ngtr'), 'missing test_ngtr'
assert hasattr(mod, 'test_log'), 'missing test_log'
assert hasattr(mod, 'test_recv'), 'missing test_recv'
assert hasattr(mod, 'test_recv_eof'), 'missing test_recv_eof'
assert hasattr(mod, 'test_recv_length'), 'missing test_recv_length'
assert hasattr(mod, 'test_recv_head_only'), 'missing test_recv_head_only'
assert hasattr(mod, 'test_recv_content_length'), 'missing test_recv_content_length'
assert hasattr(mod, 'test_recv_content_encoding'), 'missing test_recv_content_encoding'
assert hasattr(mod, 'test_recv_content_encoding_without_eof'), 'missing test_recv_content_encoding_without_eof'
assert hasattr(mod, 'test_recv_content_encoding_chunked'), 'missing test_recv_content_encoding_chunked'

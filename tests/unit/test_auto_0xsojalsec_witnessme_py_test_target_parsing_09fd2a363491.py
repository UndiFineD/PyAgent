
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_witnessme_py_test_target_parsing_09fd2a363491.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_ip_network_target_parsing'), 'missing test_ip_network_target_parsing'
assert hasattr(mod, 'test_stdin_parsing'), 'missing test_stdin_parsing'
assert hasattr(mod, 'test_nmap_xml_target_parsing'), 'missing test_nmap_xml_target_parsing'

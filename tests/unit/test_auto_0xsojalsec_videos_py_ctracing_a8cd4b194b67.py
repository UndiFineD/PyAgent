
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_ctracing_a8cd4b194b67.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LastFewMonths'), 'missing LastFewMonths'
assert hasattr(mod, 'UnemploymentTitle'), 'missing UnemploymentTitle'
assert hasattr(mod, 'ExplainTracing'), 'missing ExplainTracing'
assert hasattr(mod, 'ContactTracingMisnomer'), 'missing ContactTracingMisnomer'
assert hasattr(mod, 'ContactTracingWords'), 'missing ContactTracingWords'
assert hasattr(mod, 'WanderingDotsWithLines'), 'missing WanderingDotsWithLines'
assert hasattr(mod, 'WhatAboutPeopleWithoutPhones'), 'missing WhatAboutPeopleWithoutPhones'
assert hasattr(mod, 'PiGesture1'), 'missing PiGesture1'
assert hasattr(mod, 'PiGesture2'), 'missing PiGesture2'
assert hasattr(mod, 'PiGesture3'), 'missing PiGesture3'
assert hasattr(mod, 'AppleGoogleCoop'), 'missing AppleGoogleCoop'
assert hasattr(mod, 'LocationTracking'), 'missing LocationTracking'
assert hasattr(mod, 'MoreLinks'), 'missing MoreLinks'
assert hasattr(mod, 'LDMEndScreen'), 'missing LDMEndScreen'

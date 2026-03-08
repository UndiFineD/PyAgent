import sys, pathlib, traceback
# add workspace root so that the top-level "src" package is importable
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

print('sys.path:', sys.path[:8])
try:
    from src.core.base.lifecycle import base_agent
    print('success')
except Exception as e:
    print('got exception:', type(e), e)
    traceback.print_exc()

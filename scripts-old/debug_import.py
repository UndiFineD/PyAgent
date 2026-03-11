import pathlib
import sys
import traceback

# add workspace root so that the top-level "src" package is importable
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

print('sys.path:', sys.path[:8])
try:
    print('success')
except Exception as e:
    print('got exception:', type(e), e)
    traceback.print_exc()

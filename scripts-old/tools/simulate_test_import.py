import sys
from pathlib import Path

p = Path('src/logic/agents').resolve().parent
# test uses parent.parent: in test file, Path(__file__).parent.parent points to src/logic
src_path = str(p)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
print('sys.path[0]=', sys.path[0])
from logic.agents.forensics.archive_intelligence import *

print('dir after import:', dir())

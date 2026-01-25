## Issues found by ruffAgent at 20260115-1458

```
F401 [*] `json` imported but unused
 --> src\maintenance\agents.py:2:8
  |
1 | import os
2 | import json
  |        ^^^^
3 | import asyncio
4 | import sys
  |
help: Remove unused import: `json`

F401 [*] `typing.List` imported but unused
 --> src\maintenance\agents.py:6:20
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                    ^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Dict` imported but unused
 --> src\maintenance\agents.py:6:26
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                          ^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Any` imported but unused
 --> src\maintenance\agents.py:6:32
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                                ^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Annotated` imported but unused
 --> src\maintenance\agents.py:6:37
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                                     ^^^^^^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

Found 5 errors.
[*] 5 fixable with the `--fix` option.

```

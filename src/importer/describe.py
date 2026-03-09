from pathlib import Path
from typing import Dict


def describe_file(path: Path) -> Dict[str, object]:
    stat = path.stat()
    return {"path": str(path), "size": stat.st_size}

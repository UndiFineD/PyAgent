from pathlib import Path
from typing import List, Dict


def compile_architecture(descriptors: List[Dict], out_path: Path) -> None:
    out_path = Path(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        for d in descriptors:
            f.write(f"{d.get('path')}\n")

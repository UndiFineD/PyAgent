from pathlib import Path

def read_markdown_file(file_path: str) -> str:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    try:
        return p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return p.read_text(encoding='latin-1')

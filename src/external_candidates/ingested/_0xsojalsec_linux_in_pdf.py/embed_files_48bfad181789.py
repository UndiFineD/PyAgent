# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-linux-in-pdf\embed_files.py
import base64
import json
import pathlib
import sys
import zlib

if len(sys.argv) < 4:
    print("not enough arguments.")
    sys.exit(1)

js_path = pathlib.Path(sys.argv[1]).resolve()
files_dir = pathlib.Path(sys.argv[2]).resolve()
out_path = pathlib.Path(sys.argv[3]).resolve()

files = {}
for file_path in files_dir.rglob("*"):
    if file_path.is_dir():
        continue
    rel_path = str(file_path.relative_to(files_dir))
    data = file_path.read_bytes()
    data_compressed = zlib.compress(data, level=9)
    data_b64 = base64.b64encode(data_compressed)
    files[rel_path] = data_b64.decode()

js = js_path.read_text()
js = js.replace("__files_data__", json.dumps(files))

out_path.write_text(js)

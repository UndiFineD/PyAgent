# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\crud.py\crud_file_997fb9fd0e87.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\crud\crud_file.py

from app.crud.base import CRUDBase

from app.models.file import File, FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]): ...


file = CRUDFile(File)

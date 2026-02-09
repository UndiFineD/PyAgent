# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\crud\crud_file.py
from app.crud.base import CRUDBase
from app.models.file import File, FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]): ...


file = CRUDFile(File)

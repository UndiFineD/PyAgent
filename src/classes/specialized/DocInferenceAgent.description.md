# DocInferenceAgent

**File**: `src\classes\specialized\DocInferenceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 137  
**Complexity**: 7 (moderate)

## Overview

Agent specializing in layout-aware OCR and document reconstruction (Chandra Pattern).
Converts images and PDFs into structured Markdown/JSON/HTML while preserving forms and tables.

## Classes (1)

### `DocInferenceAgent`

**Inherits from**: BaseAgent

Manages high-accuracy OCR and document layout reconstruction.

**Methods** (7):
- `__init__(self, file_path)`
- `parse_pdf_text(self, pdf_path)`
- `ingest_document_to_knowledge(self, doc_path, tags)`
- `process_document(self, doc_path, format)`
- `extract_form_data(self, image_path)`
- `transcribe_handwriting(self, image_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `pypdf.PdfReader`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*

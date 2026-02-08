# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-roampal\ui-implementation\src-tauri\backend\modules\memory\format_extractor\__init__.py
"""
Format Extractor Module for Roampal v0.2.3
Converts various document formats to plain text for processing by SmartBookProcessor
"""

from .base import BaseExtractor, ExtractedDocument, ExtractionError
from .csv_extractor import CSVExtractor
from .detector import FormatDetector, detect_and_extract
from .docx_extractor import DocxExtractor
from .excel_extractor import ExcelExtractor
from .html_extractor import HTMLExtractor
from .pdf_extractor import PDFExtractor
from .rtf_extractor import RTFExtractor

__all__ = [
    "ExtractedDocument",
    "BaseExtractor",
    "ExtractionError",
    "FormatDetector",
    "detect_and_extract",
    "PDFExtractor",
    "DocxExtractor",
    "ExcelExtractor",
    "CSVExtractor",
    "HTMLExtractor",
    "RTFExtractor",
]

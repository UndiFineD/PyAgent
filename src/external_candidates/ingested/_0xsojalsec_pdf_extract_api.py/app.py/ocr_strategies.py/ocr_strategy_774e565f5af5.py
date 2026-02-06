# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\app\ocr_strategies\ocr_strategy.py
class OCRStrategy:
    """Base OCR Strategy Interface"""

    def extract_text_from_pdf(self, pdf_bytes):
        raise NotImplementedError("Subclasses must implement this method")

# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_ocr_strategy.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\app\ocr_strategies\ocr_strategy.py
# NOTE: extracted with static-only rules; review before use

class OCRStrategy:

    """Base OCR Strategy Interface"""

    def extract_text_from_pdf(self, pdf_bytes):

        raise NotImplementedError("Subclasses must implement this method")


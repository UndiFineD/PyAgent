# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdf_extract_api.py\app.py\ocr_strategies.py\ocr_strategy_774e565f5af5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\app\ocr_strategies\ocr_strategy.py


class OCRStrategy:
    """Base OCR Strategy Interface"""

    def extract_text_from_pdf(self, pdf_bytes):

        raise NotImplementedError("Subclasses must implement this method")

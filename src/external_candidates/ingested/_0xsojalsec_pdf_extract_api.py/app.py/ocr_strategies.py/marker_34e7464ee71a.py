# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\app\ocr_strategies\marker.py
from marker.convert import convert_single_pdf
from marker.models import load_all_models
from ocr_strategies.ocr_strategy import OCRStrategy


class MarkerOCRStrategy(OCRStrategy):
    """Marker OCR Strategy"""

    def extract_text_from_pdf(self, pdf_bytes):
        model_lst = load_all_models()
        full_text, images, out_meta = convert_single_pdf(pdf_bytes, model_lst)
        return full_text

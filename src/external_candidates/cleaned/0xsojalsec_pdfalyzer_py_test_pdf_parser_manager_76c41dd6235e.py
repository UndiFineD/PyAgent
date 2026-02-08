# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\tests.py\pdfalyzer.py\test_pdf_parser_manager_76c41dd6235e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\test_pdf_parser_manager.py

from pdfalyzer.util.pdf_parser_manager import PdfParserManager


def test_pdf_parser_manager(analyzing_malicious_pdf_path):

    pdf_parser_manager = PdfParserManager(analyzing_malicious_pdf_path)

    assert pdf_parser_manager.object_ids_containing_stream_data == [
        4,
        71,
        411,
        412,
        416,
        419,
        421,
        423,
        424,
        426,
    ]

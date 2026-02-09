# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\utils\marker_cli.py
import argparse

from marker.convert import convert_single_pdf
from marker.models import load_all_models

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF file.")
    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        default="../examples/example-mri.pdf",
        help="The path to the PDF file to be processed.",
    )
    args = parser.parse_args()

    model_lst = load_all_models()
    pdf_file_path = args.file
    full_text, images, out_meta = convert_single_pdf(pdf_file_path, model_lst)
    print(full_text)

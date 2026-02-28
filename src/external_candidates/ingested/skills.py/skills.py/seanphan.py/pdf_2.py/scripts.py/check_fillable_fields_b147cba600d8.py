# Extracted from: C:\DEV\PyAgent\.external\skills\skills\seanphan\pdf-2\scripts\check_fillable_fields.py
import sys

from pypdf import PdfReader

# Script for Claude to run to determine whether a PDF has fillable form fields. See forms.md.


reader = PdfReader(sys.argv[1])
if reader.get_fields():
    print("This PDF has fillable form fields")
else:
    print(
        "This PDF does not have fillable form fields; you will need to visually determine where to enter data"
    )

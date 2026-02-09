# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\md.py
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("sample.txt")
print(result.text_content)

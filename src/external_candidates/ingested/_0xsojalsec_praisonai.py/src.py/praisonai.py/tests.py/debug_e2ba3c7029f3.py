# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai\tests\debug.py
# tests/debug.py
import logging
import sys
import traceback
import tracemalloc
import warnings

# Enable Tracemalloc
tracemalloc.start()

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
)


# Function to Log Warnings with Traceback
def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, "write") else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))


# Override showwarning
warnings.showwarning = warn_with_traceback

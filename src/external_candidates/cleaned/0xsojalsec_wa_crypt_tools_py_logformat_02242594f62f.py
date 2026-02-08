# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wa_crypt_tools.py\src.py\wa_crypt_tools.py\lib.py\logformat_02242594f62f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wa-crypt-tools\src\wa_crypt_tools\lib\logformat.py

import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"

    yellow = "\x1b[33;20m"

    red = "\x1b[31;20m"

    bold_red = "\x1b[31;1m"

    reset = "\x1b[0m"

    format = "%(filename)s:%(lineno)d \t: [%(levelname).1s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):

        log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_mantis.py\mantis.py\config_parsers.py\logging_utils_2ae9720d637f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\config_parsers\logging_utils.py

import logging

import logging.config

import os

from mantis.config_parsers.config_client import ConfigProvider

from mantis.models.args_model import ArgsModel


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"

    yellow = "\x1b[33;20m"

    red = "\x1b[31;20m"

    green = "\x1b[32;20m"

    bold_red = "\x1b[31;1m"

    reset = "\x1b[0m"

    format = "[%(asctime)s] --> %(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):

        log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)


class LoggingConfig(object):
    @staticmethod
    def configure_logging(args: ArgsModel):

        if args.verbose:
            log_config = ConfigProvider.get_config().logging_debug

            logging.config.dictConfig(log_config)

            logging.StreamHandler().setFormatter(CustomFormatter())

            logging.info("MANTIS ASSET DISCOVERY - STARTED")

            logging.info("Debug mode enabled")

        else:
            log_config = ConfigProvider.get_config().logging

            logging.config.dictConfig(log_config)

            logging.StreamHandler().setFormatter(CustomFormatter())

            logging.info("MANTIS ASSET DISCOVERY - STARTED")

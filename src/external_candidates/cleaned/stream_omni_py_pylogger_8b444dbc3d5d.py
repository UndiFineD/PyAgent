# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\cosyvoice.py\third_party.py\matcha_tts.py\matcha.py\utils.py\pylogger_8b444dbc3d5d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\third_party\Matcha-TTS\matcha\utils\pylogger.py

import logging

from lightning.pytorch.utilities import rank_zero_only


def get_pylogger(name: str = __name__) -> logging.Logger:
    """Initializes a multi-GPU-friendly python command line logger.

    :param name: The name of the logger, defaults to ``__name__``.

    :return: A logger object.

    """

    logger = logging.getLogger(name)

    # this ensures all logging levels get marked with the rank zero decorator

    # otherwise logs would get multiplied for each GPU process in multi-GPU setup

    logging_levels = (
        "debug",
        "info",
        "warning",
        "error",
        "exception",
        "fatal",
        "critical",
    )

    for level in logging_levels:
        setattr(logger, level, rank_zero_only(getattr(logger, level)))

    return logger

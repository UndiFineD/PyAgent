# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\cosyvoice.py\third_party.py\matcha_tts.py\matcha.py\utils.py\instantiators_079894ce0e7e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\third_party\Matcha-TTS\matcha\utils\instantiators.py

from typing import List

import hydra

from lightning import Callback

from lightning.pytorch.loggers import Logger

from matcha.utils import pylogger

from omegaconf import DictConfig

log = pylogger.get_pylogger(__name__)

def instantiate_callbacks(callbacks_cfg: DictConfig) -> List[Callback]:

    """Instantiates callbacks from config.

    :param callbacks_cfg: A DictConfig object containing callback configurations.

    :return: A list of instantiated callbacks.

    """

    callbacks: List[Callback] = []

    if not callbacks_cfg:

        log.warning("No callback configs found! Skipping..")

        return callbacks

    if not isinstance(callbacks_cfg, DictConfig):

        raise TypeError("Callbacks config must be a DictConfig!")

    for _, cb_conf in callbacks_cfg.items():

        if isinstance(cb_conf, DictConfig) and "_target_" in cb_conf:

            log.info(

                f"Instantiating callback <{cb_conf._target_}>"

            )  # pylint: disable=protected-access

            callbacks.append(hydra.utils.instantiate(cb_conf))

    return callbacks

def instantiate_loggers(logger_cfg: DictConfig) -> List[Logger]:

    """Instantiates loggers from config.

    :param logger_cfg: A DictConfig object containing logger configurations.

    :return: A list of instantiated loggers.

    """

    logger: List[Logger] = []

    if not logger_cfg:

        log.warning("No logger configs found! Skipping...")

        return logger

    if not isinstance(logger_cfg, DictConfig):

        raise TypeError("Logger config must be a DictConfig!")

    for _, lg_conf in logger_cfg.items():

        if isinstance(lg_conf, DictConfig) and "_target_" in lg_conf:

            log.info(

                f"Instantiating logger <{lg_conf._target_}>"

            )  # pylint: disable=protected-access

            logger.append(hydra.utils.instantiate(lg_conf))

    return logger


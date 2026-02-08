# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\cosyvoice.py\third_party.py\matcha_tts.py\matcha.py\hifigan.py\env_47786fdbe375.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\third_party\Matcha-TTS\matcha\hifigan\env.py

"""from https://github.com/jik876/hifi-gan"""

import os

import shutil

class AttrDict(dict):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.__dict__ = self

def build_env(config, config_name, path):

    t_path = os.path.join(path, config_name)

    if config != t_path:

        os.makedirs(path, exist_ok=True)

        shutil.copyfile(config, os.path.join(path, config_name))


# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\DiffSinger\data_gen\tts\txt_processors\base_text_processor.py
class BaseTxtProcessor:
    @staticmethod
    def sp_phonemes():
        return ["|"]

    @classmethod
    def process(cls, txt, pre_align_args):
        raise NotImplementedError

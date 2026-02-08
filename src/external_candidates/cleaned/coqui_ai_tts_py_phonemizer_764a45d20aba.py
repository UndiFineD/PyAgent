# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tts.py\tts.py\utils.py\text.py\chinese_mandarin.py\phonemizer_764a45d20aba.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\tts\utils\text\chinese_mandarin\phonemizer.py

try:
    import jieba

    import pypinyin

except ImportError as e:
    raise ImportError("Chinese requires: jieba, pypinyin") from e

from .pinyinToPhonemes import PINYIN_DICT


def _chinese_character_to_pinyin(text: str) -> list[str]:
    pinyins = pypinyin.pinyin(text, style=pypinyin.Style.TONE3, heteronym=False, neutral_tone_with_five=True)

    pinyins_flat_list = [item for sublist in pinyins for item in sublist]

    return pinyins_flat_list


def _chinese_pinyin_to_phoneme(pinyin: str) -> str:
    segment = pinyin[:-1]

    tone = pinyin[-1]

    phoneme = PINYIN_DICT.get(segment, [""])[0]

    return phoneme + tone


def chinese_text_to_phonemes(text: str, seperator: str = "|") -> str:
    tokenized_text = jieba.cut(text, HMM=False)

    tokenized_text = " ".join(tokenized_text)

    pinyined_text: list[str] = _chinese_character_to_pinyin(tokenized_text)

    results: list[str] = []

    for token in pinyined_text:
        if token[-1] in "12345":  # TODO transform to is_pinyin()
            pinyin_phonemes = _chinese_pinyin_to_phoneme(token)

            results += list(pinyin_phonemes)

        else:  # is ponctuation or other
            results += list(token)

    return seperator.join(results)

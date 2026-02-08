# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tts.py\tts.py\utils.py\synthesis_2cac2f704091.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\tts\utils\synthesis.py


def inv_spectrogram(postnet_output, ap, CONFIG):
    if CONFIG.model.lower() in ["tacotron"]:
        wav = ap.inv_spectrogram(postnet_output.T)

    else:
        wav = ap.inv_melspectrogram(postnet_output.T)

    return wav


# TODO: perform GL with pytorch for batching


def apply_griffin_lim(inputs, input_lens, CONFIG, ap):
    """Apply griffin-lim to each sample iterating throught the first dimension.

    Args:

        inputs (Tensor or np.Array): Features to be converted by GL. First dimension is the batch size.

        input_lens (Tensor or np.Array): 1D array of sample lengths.

        CONFIG (Dict): TTS config.

        ap (AudioProcessor): TTS audio processor.

    """

    wavs = []

    for idx, spec in enumerate(inputs):
        wav_len = (input_lens[idx] * ap.hop_length) - ap.hop_length  # inverse librosa padding

        wav = inv_spectrogram(spec, ap, CONFIG)

        # assert len(wav) == wav_len, f" [!] wav lenght: {len(wav)} vs expected: {wav_len}"

        wavs.append(wav[:wav_len])

    return wavs

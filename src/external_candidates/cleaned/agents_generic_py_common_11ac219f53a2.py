# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_plugins.py\livekit_plugins_clova.py\livekit.py\plugins.py\clova.py\common_11ac219f53a2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-clova\livekit\plugins\clova\common.py

import io

from pydub import AudioSegment  # type: ignore[import-untyped]


def resample_audio(audio_bytes: bytes, original_sample_rate: int, target_sample_rate: int) -> bytes:
    resampled_audio = AudioSegment.from_raw(
        io.BytesIO(audio_bytes),
        sample_width=2,
        frame_rate=original_sample_rate,
        channels=1,
    ).set_frame_rate(target_sample_rate)

    return resampled_audio.raw_data  # type: ignore

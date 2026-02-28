# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\fish-speech\tools\server\inference.py
from http import HTTPStatus

import numpy as np
from fish_speech.inference_engine import TTSInferenceEngine
from fish_speech.utils.schema import ServeTTSRequest
from kui.asgi import HTTPException

AMPLITUDE = 32768  # Needs an explaination


def inference_wrapper(req: ServeTTSRequest, engine: TTSInferenceEngine):
    """
    Wrapper for the inference function.
    Used in the API server.
    """
    count = 0
    for result in engine.inference(req):
        match result.code:
            case "header":
                if isinstance(result.audio, tuple):
                    yield result.audio[1]

            case "error":
                raise HTTPException(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    content=str(result.error),
                )

            case "segment":
                count += 1
                if isinstance(result.audio, tuple):
                    yield (result.audio[1] * AMPLITUDE).astype(np.int16).tobytes()

            case "final":
                count += 1
                if isinstance(result.audio, tuple):
                    yield result.audio[1]
                return None  # Stop the generator

    if count == 0:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            content="No audio generated, please check the input text.",
        )

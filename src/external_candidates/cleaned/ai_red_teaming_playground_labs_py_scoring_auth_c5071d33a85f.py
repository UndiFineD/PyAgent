# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_red_teaming_playground_labs.py\src.py\picture_submission.py\webapi.py\server.py\middleware.py\scoring_auth_c5071d33a85f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\picture-submission\webapi\server\middleware\scoring_auth.py

# Copyright (c) Microsoft Corporation.

# Licensed under the MIT License.

from functools import wraps

from flask import Response

from flask import current_app as app

from flask import request

from server.settings import CONFIG_SCORING_KEY, CONFIG_SCORING_SETTINGS

def scoring_auth(f):

    @wraps(f)

    def wrapper(*args, **kwargs):

        if (

            request.headers.get("x-scoring-key")

            != app.config[CONFIG_SCORING_SETTINGS][CONFIG_SCORING_KEY]

        ):

            return Response("Unauthorized", status=401)

        return f(*args, **kwargs)

    return wrapper


# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_red_teaming_playground_labs.py\src.py\picture_submission.py\webapi.py\server.py\middleware.py\ctfd_auth_8317e1e680ac.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\picture-submission\webapi\server\middleware\ctfd_auth.py

# Copyright (c) Microsoft Corporation.

# Licensed under the MIT License.

import logging

from functools import wraps

from flask import Response

from flask import current_app as app

from flask import request

from server.service.ctfd.ctfd import get_ctfd_service_instance

from server.settings import CONFIG_AUTH_SETTINGS, CONFIG_AUTH_TYPE

logger = logging.getLogger(__name__)


def ctfd_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ctfd_service = get_ctfd_service_instance()

        # Check if the auth is set to none or ctfd

        if app.config[CONFIG_AUTH_SETTINGS][CONFIG_AUTH_TYPE] != "ctfd":
            kwargs["user_id"] = "1"  # Set the user_id to 1 if no auth is provided

            return f(*args, **kwargs)

        if ctfd_service is None:
            logger.error("CTFd Service not initialized")

            return Response("CTFd Service not initialized", status=500)

        auth_result = ctfd_service.validate_auth(request)

        if not auth_result[0]:
            return auth_result[2]

        kwargs["ctfd_ticket"] = auth_result[1]

        return f(*args, **kwargs)

    return wrapper

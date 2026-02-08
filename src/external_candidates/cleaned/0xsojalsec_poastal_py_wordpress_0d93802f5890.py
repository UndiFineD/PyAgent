# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_poastal.py\backend.py\modules.py\wordpress_0d93802f5890.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-poastal\backend\modules\wordpress.py

import requests


def wordpress_email(email):

    params = {
        "http_envelope": "1",
    }

    response = requests.get(
        "https://public-api.wordpress.com/rest/v1.1/users/{}/auth-options".format(email),
        params=params,
    )

    checker = response.text

    text = '"email_verified": true'

    if text in checker:
        return f"true"

    else:
        return f"false"

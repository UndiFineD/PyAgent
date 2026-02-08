# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_poastal.py\backend.py\modules.py\snapchat_c2c9272bee82.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-poastal\backend\modules\snapchat.py

import json

import requests


def snapchat_email(email):

    headers = {
        "Content-Type": "text/plain",
    }

    data = {}

    data.update(email=email)

    data = json.dumps(data)

    response = requests.post("https://bitmoji.api.snapchat.com/api/user/find", headers=headers, data=data)

    checker = response.text

    text = '{"account_type":"snapchat"}'

    if text in checker:
        return f"true"

    else:
        return f"false"

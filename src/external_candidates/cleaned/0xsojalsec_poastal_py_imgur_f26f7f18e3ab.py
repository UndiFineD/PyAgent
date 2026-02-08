# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_poastal.py\backend.py\modules.py\imgur_f26f7f18e3ab.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-poastal\backend\modules\imgur.py

import requests


def imgur_email(email):

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    data = "email={}".format(email)

    response = requests.post("https://imgur.com/signin/ajax_email_available", headers=headers, data=data)

    checker = response.text

    text = '{"data":{"available":false},"success":true,"status":200}'

    if text in checker:
        return f"true"

    else:
        return f"false"

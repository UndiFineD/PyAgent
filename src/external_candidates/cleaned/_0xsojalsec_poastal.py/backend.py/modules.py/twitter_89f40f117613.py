# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-poastal\backend\modules\twitter.py
import json

import requests


def twitter_email(email):
    email_checker = "https://api.twitter.com/i/users/email_available.json?email={}".format(email)

    response = requests.get(
        email_checker,
    )

    check = response.json()

    if check["taken"]:
        return f"true"
    else:
        return f"false"

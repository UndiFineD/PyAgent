# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\ruslanlanket.py\avito.py\scripts.py\get_self_9ba44286ccd6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\ruslanlanket\avito\scripts\get_self.py

import json

import sys

import requests

def get_self(token):

    url = "https://api.avito.ru/core/v1/accounts/self"

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        return response.json()

    else:

        print(f"Error: {response.status_code} - {response.text}")

        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage: get_self.py <token>")

        sys.exit(1)

    user = get_self(sys.argv[1])

    print(json.dumps(user))


# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\ruslanlanket.py\avito.py\scripts.py\get_balance_322bbde00cd9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\ruslanlanket\avito\scripts\get_balance.py

import json

import sys

import requests

def get_balance(token, user_id):

    url = f"https://api.avito.ru/core/v1/accounts/{user_id}/balance"

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        return response.json()

    else:

        print(f"Error: {response.status_code} - {response.text}")

        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) < 3:

        print("Usage: get_balance.py <token> <user_id>")

        sys.exit(1)

    balance = get_balance(sys.argv[1], sys.argv[2])

    print(json.dumps(balance))


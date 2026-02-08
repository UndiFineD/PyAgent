# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\module\enum\azuread_list_mfa_status_for_users.py
import datetime
import json
import random
import string
import sys

import requests
from flask_mongoengine import DoesNotExist

from core.database.models import AZURECredentials

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/",
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed.",
    }
}

global device_code_request_json

description = (
    "This module will try to get as many information on the user's account on O365, based on the its privileges."
)
aws_command = "No cli command"


def exploit(profile, workspace):
    access_token = profile["azure_access_token"]

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------
    try:
        usersMFA = json.loads(
            requests.get(
                "https://graph.microsoft.com/beta/reports/credentialUserRegistrationDetails",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(access_token),
                },
            ).text
        )
        if "error" in usersMFA:
            return {"error": {"error": usersMFA["error"]["message"]}}

        return {"givenName": usersMFA["value"]}

    except Exception as e:
        return {"error": str(e)}

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_red_teaming_playground_labs.py\src.py\picture_submission.py\webapi.py\server.py\service.py\ctfd.py\ticket_aae0419b476a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\picture-submission\webapi\server\service\ctfd\ticket.py

# Copyright (c) Microsoft Corporation.

# Licensed under the MIT License.

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class CtfdAuthTicket(DataClassJsonMixin):
    id: int

    nonce: str

    cookie: str

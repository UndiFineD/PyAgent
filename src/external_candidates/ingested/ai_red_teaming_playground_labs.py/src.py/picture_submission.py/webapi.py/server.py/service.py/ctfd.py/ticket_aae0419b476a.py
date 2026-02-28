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

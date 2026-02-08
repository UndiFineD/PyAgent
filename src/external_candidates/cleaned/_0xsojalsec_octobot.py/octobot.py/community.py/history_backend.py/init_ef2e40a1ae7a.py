# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OctoBot\octobot\community\history_backend\__init__.py
#  This file is part of OctoBot (https://github.com/Drakkar-Software/OctoBot)
#  Copyright (c) 2023 Drakkar-Software, All rights reserved.
#
#  OctoBot is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  OctoBot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with OctoBot. If not, see <https://www.gnu.org/licenses/>.

from octobot.community.history_backend import (
    clickhouse_historical_backend_client,
    historical_backend_client,
    history_backend_factory,
)
from octobot.community.history_backend.clickhouse_historical_backend_client import (
    ClickhouseHistoricalBackendClient,
)
from octobot.community.history_backend.historical_backend_client import (
    HistoricalBackendClient,
)
from octobot.community.history_backend.history_backend_factory import (
    history_backend_client,
)

__all__ = [
    "history_backend_client",
    "HistoricalBackendClient",
    "ClickhouseHistoricalBackendClient",
]

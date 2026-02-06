# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OctoBot\octobot\community\__init__.py
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

from octobot.community import (
    authentication,
    community_analysis,
    community_manager,
    errors,
    errors_upload,
    feeds,
    graphql_requests,
    models,
)
from octobot.community.authentication import (
    CommunityAuthentication,
)
from octobot.community.community_analysis import (
    can_read_metrics,
    get_community_metrics,
    get_current_octobots_stats,
)
from octobot.community.community_manager import (
    CommunityManager,
)
from octobot.community.errors import (
    BotError,
    BotNotFoundError,
    NoBotDeviceError,
    RequestError,
    StatusCodeRequestError,
)
from octobot.community.errors_upload import (
    flush_tracker,
    init_sentry_tracker,
)
from octobot.community.feeds import (
    AbstractFeed,
    CommunityMQTTFeed,
    CommunityWSFeed,
    community_feed_factory,
)
from octobot.community.graphql_requests import (
    create_bot_device_query,
    create_bot_query,
    select_bot_query,
    select_bots_query,
    select_startup_info_query,
    select_subscribed_profiles_query,
    update_bot_config_and_stats_query,
    update_bot_portfolio_query,
    update_bot_trades_query,
    upsert_bot_trades_query,
    upsert_historical_bot_portfolio_query,
)
from octobot.community.history_backend import (
    ClickhouseHistoricalBackendClient,
    HistoricalBackendClient,
    history_backend_client,
)
from octobot.community.identifiers_provider import (
    IdentifiersProvider,
)
from octobot.community.models import (
    USD_LIKE,
    CommunityDonation,
    CommunityFields,
    CommunitySupports,
    CommunityTentaclesPackage,
    CommunityUserAccount,
    ExecutedProductDetails,
    StartupInfo,
    StrategyData,
    get_exchange_type_from_availability,
    get_exchange_type_from_internal_name,
    get_master_and_nested_product_slug_from_profile_name,
    get_tentacles_data_exchange_config,
    is_custom_category,
    to_bot_exchange_internal_name,
    to_community_exchange_internal_name,
)
from octobot.community.supabase_backend import (
    ASyncConfigurationStorage,
    AuthenticatedAsyncSupabaseClient,
    CommunitySupabaseClient,
    SyncConfigurationStorage,
)

__all__ = [
    "RequestError",
    "StatusCodeRequestError",
    "BotError",
    "BotNotFoundError",
    "NoBotDeviceError",
    "IdentifiersProvider",
    "CommunityUserAccount",
    "CommunityFields",
    "get_community_metrics",
    "get_current_octobots_stats",
    "can_read_metrics",
    "CommunityManager",
    "CommunityAuthentication",
    "CommunityTentaclesPackage",
    "CommunitySupports",
    "CommunityDonation",
    "init_sentry_tracker",
    "flush_tracker",
    "StartupInfo",
    "StrategyData",
    "ExecutedProductDetails",
    "get_exchange_type_from_availability",
    "to_bot_exchange_internal_name",
    "get_exchange_type_from_internal_name",
    "to_community_exchange_internal_name",
    "is_custom_category",
    "get_master_and_nested_product_slug_from_profile_name",
    "get_tentacles_data_exchange_config",
    "USD_LIKE",
    "SyncConfigurationStorage",
    "ASyncConfigurationStorage",
    "AuthenticatedAsyncSupabaseClient",
    "CommunitySupabaseClient",
    "select_startup_info_query",
    "select_bot_query",
    "select_bots_query",
    "create_bot_query",
    "create_bot_device_query",
    "update_bot_config_and_stats_query",
    "select_subscribed_profiles_query",
    "update_bot_trades_query",
    "upsert_bot_trades_query",
    "update_bot_portfolio_query",
    "upsert_historical_bot_portfolio_query",
    "AbstractFeed",
    "CommunityWSFeed",
    "CommunityMQTTFeed",
    "community_feed_factory",
    "history_backend_client",
    "HistoricalBackendClient",
    "ClickhouseHistoricalBackendClient",
]

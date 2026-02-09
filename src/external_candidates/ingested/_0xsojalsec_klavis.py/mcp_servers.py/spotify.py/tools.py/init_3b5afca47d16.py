# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\spotify\tools\__init__.py
from .albums import (
    check_user_saved_albums,
    get_album_tracks,
    get_albums_info,
    get_user_saved_albums,
    remove_albums_for_current_user,
    save_albums_for_current_user,
)
from .artists import get_artist_albums, get_artist_top_tracks, get_artists_info
from .base import (
    auth_token_context,
    get_spotify_access_token,
    get_spotify_client,
    get_user_spotify_client,
)
from .episodes import (
    check_user_saved_episodes,
    get_episodes_info,
    get_user_saved_episodes,
    remove_episodes_for_current_user,
    save_episodes_for_current_user,
)
from .playlists import (
    add_items_to_playlist,
    get_current_user_playlists,
    get_playlist_by_id,
    get_user_owned_playlists,
    remove_items_from_playlist,
    update_playlist_details,
)
from .search import search_tracks
from .shows import *
from .tracks import (
    check_user_saved_tracks,
    get_tracks_info,
    get_user_saved_tracks,
    remove_user_saved_tracks,
    save_tracks_for_current_user,
)
from .users import *

__all__ = [
    "auth_token_context",
    "get_spotify_access_token",
    "search_tracks",
    "get_tracks_info",
    "get_spotify_client",
    "get_user_spotify_client",
    "get_user_saved_tracks",
    "check_user_saved_tracks",
    "save_tracks_for_current_user",
    "remove_user_saved_tracks",
    "get_albums_info",
    "get_album_tracks",
    "get_user_saved_albums",
    "save_albums_for_current_user",
    "remove_albums_for_current_user",
    "check_user_saved_albums",
    "get_artists_info",
    "get_artist_albums",
    "get_artist_top_tracks",
    "get_episodes_info",
    "save_episodes_for_current_user",
    "get_user_saved_episodes",
    "remove_episodes_for_current_user",
    "check_user_saved_episodes",
    "get_playlist_by_id",
    "get_user_owned_playlists",
    "update_playlist_details",
    "get_current_user_profile",
    "get_current_user_top_items",
    "get_spotify_user_public_profile",
    "follow_playlist",
    "unfollow_playlist",
    "get_current_user_followed_artists",
    "follow_artists_or_users",
    "unfollow_artists_or_users",
    "check_user_follows",
    "add_items_to_playlist",
    "remove_items_from_playlist",
    "get_current_user_playlists",
    "get_multiple_shows",
    "get_show_episodes",
    "get_current_user_saved_shows",
    "save_shows_to_user_library",
    "remove_shows_from_user_library",
    "check_user_saved_shows",
]

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\auth.py
import json
import os


def is_running_in_streamlit():
    try:
        import streamlit
    except ImportError:
        return False
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    return get_script_run_ctx(suppress_warning=True) is not None


def get_posit_user_info():
    import streamlit

    headers = streamlit.context.headers
    if not headers:
        return None
    user_info_json = headers.get("Rstudio-Connect-Credentials")
    if user_info_json is None:
        return None
    return json.loads(user_info_json)


def get_username() -> str:
    if is_running_in_streamlit():
        import streamlit as st

        if hasattr(st.user, "is_logged_in") and st.user.is_logged_in:
            return st.user["email"]
        user_info = get_posit_user_info()
        if user_info is not None:
            return user_info.get("user", "unknown")
    # get the current user of the computer (for local development)
    return os.environ.get("USER", "unknown")

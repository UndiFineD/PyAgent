# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\app.py\utils.py\testing_7386ec4b3902.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\utils\testing.py

import streamlit as st


def is_test_dialog_shown(dialog_key: str):

    return dialog_key in st.session_state.get("test_dialogs", [])


def show_test_dialog(at, dialog_key: str):

    if "test_dialogs" not in at.session_state:
        at.session_state["test_dialogs"] = []

    at.session_state["test_dialogs"].append(dialog_key)

    at.run()


def hide_test_dialog(at, dialog_key: str):

    if "test_dialogs" not in at.session_state:
        at.session_state["test_dialogs"] = []

    at.session_state["test_dialogs"].remove(dialog_key)

    at.run()

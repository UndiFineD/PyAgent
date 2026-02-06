# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\run_app.py
#
# Run everything including imports only in __main__ block
# This is done to avoid subprocesses initializing streamlit
#
import importlib
import os

if __name__ == "__main__":
    import streamlit as st
    from ovo import config, get_username
    from ovo.app.pages import (
        admin_debug_page,
        admin_import_export_page,
        bindcraft_binder_design_page,
        designs_page,
        jobs_page,
        rf_binder_design_page,
        rf_binder_diversification_page,
        rf_scaffold_design_page,
        welcome_page,
    )
    from ovo.core.plugins import plugin_pages

    pages = {
        "Browse": [
            welcome_page,
            jobs_page,
            designs_page,
        ],
        "RFdiffusion": [
            rf_scaffold_design_page,
            rf_binder_design_page,
            rf_binder_diversification_page,
        ],
        "BindCraft": [
            bindcraft_binder_design_page,
        ],
    }

    if plugin_pages:
        url_paths = set(page._url_path for group in pages.values() for page in group)
        for group_label, module_pages in plugin_pages.items():
            for page_dict in module_pages:
                assert isinstance(
                    page_dict, dict
                ), f"Expected dictionaries in '{module_name}.pages, found: {type(page_dict).__name__}: {page_dict}"
                page_module_path = page_dict["page"]
                assert "/" not in page_module_path and not page_module_path.endswith(
                    ".py"
                ), f"Plugin page should be defined by module path (my_tool.page_module), got {page_module_path}"
                module_name = page_module_path.split(".")[0]
                module = importlib.import_module(module_name)
                url_path = page_module_path.split(".")[-1]
                while url_path in url_paths:
                    url_path += "_copy"
                url_paths.add(url_path)
                page_file_path = (
                    page_module_path.removeprefix(module_name)
                    .removeprefix(".")
                    .replace(".", "/")
                    + ".py"
                )
                pages[group_label] = pages.get(group_label, []) + [
                    st.Page(
                        page=os.path.join(
                            os.path.dirname(module.__file__), page_file_path
                        ),
                        url_path=url_path,
                        **{k: v for k, v in page_dict.items() if k != "page"},
                    )
                ]

    if get_username() in config.auth.admin_users:
        pages["Admin section"] = [
            admin_debug_page,
            admin_import_export_page,
        ]

    pg = st.navigation(pages)
    pg.run()

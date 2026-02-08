# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\pages\__init__.py
import streamlit as st

# Page paths relative to entry point (run_app.py)
welcome_page = st.Page("app/pages/welcome.py", title="🥚 Welcome", default=True)
jobs_page = st.Page("app/pages/jobs/jobs.py", title="⏳ Jobs")
designs_page = st.Page("app/pages/designs/designs.py", title="🐣 Designs")

rf_scaffold_design_page = st.Page("app/pages/rfdiffusion/scaffold_design.py", title="🏗️ Scaffold design")
rf_binder_design_page = st.Page("app/pages/rfdiffusion/binder_design.py", title="🧬 Binder design")
rf_binder_diversification_page = st.Page(
    "app/pages/rfdiffusion/binder_diversification.py", title="♻️ Binder diversification"
)

bindcraft_binder_design_page = st.Page("app/pages/bindcraft/bindcraft_binder_design.py", title="⚒️ Binder design")

admin_debug_page = st.Page("app/pages/debug.py", title="🖥️ Debug")
admin_import_export_page = st.Page("app/pages/import_export.py", title="📦 Import & Export")

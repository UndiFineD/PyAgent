#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Download Manager Web Interface using Streamlit.
Provides a modern UI for managing model and dataset downloads.
"""

import streamlit as st
import json
from pathlib import Path
from src.tools.download_agent.core import DownloadAgent
from src.tools.download_agent.models import DownloadConfig

# Page Config
st.set_page_config(
    page_title="PyAgent | Download Manager",
    page_icon="📥",
    layout="wide",
)

# Workspace Detection
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

def load_history():
    history_file = WORKSPACE_ROOT / "temp" / "downloads.json"
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    st.title("📥 PyAgent Download Manager")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Add New Download")
        url = st.text_input("URL (GitHub, Hugging Face, ArXiv, etc.)", placeholder="https://huggingface.co/...")
        
        c1, c2 = st.columns(2)
        dry_run = c1.checkbox("Dry Run", help="Simulate the download process")
        verbose = c2.checkbox("Verbose Log", value=True)

        if st.button("🚀 Start Download", use_container_width=True):
            if url:
                with st.spinner(f"Processing {url}..."):
                    config = DownloadConfig(
                        urls_file="",
                        dry_run=dry_run,
                        verbose=verbose,
                        base_dir=str(WORKSPACE_ROOT)
                    )
                    agent = DownloadAgent(config)
                    result = agent.process_url(url)
                    
                    if result.success:
                        st.success(f"Successfully processed: {result.destination}")
                        # Update global history
                        history_path = WORKSPACE_ROOT / "temp" / "downloads.json"
                        history_path.parent.mkdir(parents=True, exist_ok=True)
                        agent.save_results([result], str(history_path))
                    else:
                        st.error(f"Download failed: {result.error_message}")
            else:
                st.warning("Please enter a valid URL.")

    with col2:
        st.subheader("Current Config & Stats")
        st.info(f"**Workspace:** `{WORKSPACE_ROOT}`")
        st.info("**Default Download Path:** `data/models` | `data/datasets`")
        
        history = load_history()
        if history:
            summary = history.get("summary", {})
            st.metric("Total Success", summary.get("successful", 0))
            st.metric("Total Size", f"{summary.get('total_size_bytes', 0) / (1024*1024):.2f} MB")

    st.markdown("---")
    st.subheader("📦 Download History")
    
    if history:
        for res in reversed(history.get("results", [])):
            with st.expander(f"{'✅' if res['success'] else '❌'} {res['url']}", expanded=False):
                st.code(json.dumps(res, indent=2), language="json")
    else:
        st.write("No download history found in `temp/downloads.json`.")

if __name__ == "__main__":
    main()

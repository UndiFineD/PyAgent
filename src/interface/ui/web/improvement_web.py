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
Self-Improvement Manager Web Interface.
Monitor CoRT thoughts and steer the fleet's autonomous evolution.
"""

import streamlit as st
import os
import json
import time
from pathlib import Path

# Page Config
st.set_page_config(
    page_title="PyAgent | Improvement Manager",
    page_icon="🧠",
    layout="wide",
)

# Workspace Root Detection
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

def load_reasoning_chains():
    log_path = WORKSPACE_ROOT / "data" / "logs" / "reasoning_chains.jsonl"
    if not log_path.exists():
        return []
    
    chains = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    chains.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return chains

def load_audit_log():
    log_path = WORKSPACE_ROOT / "data" / "logs" / "self_improvement_audit.jsonl"
    if not log_path.exists():
        return []
    
    audit = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    audit.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return audit

def save_steering_directive(directive: str):
    steering_file = WORKSPACE_ROOT / "docs" / "prompt" / "steering.txt"
    steering_file.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(steering_file, "a", encoding="utf-8") as f:
        f.write(f"\n# Directive Added on {timestamp}\n")
        f.write(f"research: {directive}\n")

def format_timestamp(ts):
    if isinstance(ts, (int, float)):
        import datetime
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    return ts

def main():
    st.title("🧠 Self-Improvement Manager")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💡 CoRT Reasoning Chains (Thought Stream)")
        chains = load_reasoning_chains()
        if not chains:
            st.info("No reasoning chains found yet. Wait for the swarm to start thinking.")
        else:
            for chain in reversed(chains[-20:]):
                role = chain.get("role", "unknown")
                content = chain.get("content", "")
                timestamp = format_timestamp(chain.get("timestamp", ""))
                
                with st.chat_message(role if role != "thought" else "assistant"):
                    st.write(f"**[{timestamp}]**")
                    st.write(content)
                    if "action" in chain:
                        st.caption(f"Action: {chain['action']}")

    with col2:
        st.subheader("🎯 Steer the Swarm")
        with st.form("steering_form"):
            directive = st.text_area("New Improvement Directive (ArXiv topic, specific fix, etc.)", 
                                     placeholder="e.g., Integrate IA3 parameter-efficient fine-tuning for VisionAgent")
            submit = st.form_submit_button("🚀 Inject Directive")
            
            if submit and directive:
                save_steering_directive(directive)
                st.success("Directive injected into the strategic context!")

        st.markdown("---")
        st.subheader("🛡️ Audit Log")
        audit = load_audit_log()
        if audit:
            for entry in reversed(audit[-10:]):
                status = entry.get("status", "info")
                msg = entry.get("message", "No message")
                ts = format_timestamp(entry.get("timestamp", ""))
                st.write(f"- **{ts}** [{status}]: {msg}")
        else:
            st.write("Clean audit log.")

    st.markdown("---")
    st.subheader("📖 Improvement Research Status")
    research_doc = WORKSPACE_ROOT / "docs" / "IMPROVEMENT_RESEARCH.md"
    if research_doc.exists():
        st.markdown(research_doc.read_text(encoding="utf-8")[:2000] + "...")
    else:
        st.write("No research document found.")

if __name__ == "__main__":
    main()

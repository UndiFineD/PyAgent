# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\examples\sample_apps\difizen_app\intelligence\agentic\knowledge\law_knowledge.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import json

# @Time    : 2024/8/14 15:54
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: law_knowledge.py
from typing import Any, List

from agentuniverse.agent.action.knowledge.knowledge import Knowledge
from agentuniverse.agent.action.knowledge.store.document import Document


class LawKnowledge(Knowledge):
    def to_llm(self, retrieved_docs: List[Document]) -> Any:
        retrieved_texts = [
            json.dumps(
                {"text": doc.text, "from": doc.metadata["file_name"]},
                ensure_ascii=False,
            )
            for doc in retrieved_docs
        ]
        return "\n=========================================\n".join(retrieved_texts)

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\examples\third_party_examples\apps\medical_consultation_assistant_app\intelligence\agentic\knowledge\disease_knowledge.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2025/10/05 10:13
# @Author  : zhangxi
# @Email   : 1724585800@qq.com
# @FileName: law_knowledge.py
import json
from typing import Any, List

from agentuniverse.agent.action.knowledge.knowledge import Knowledge
from agentuniverse.agent.action.knowledge.store.document import Document


class DiseaseKnowledge(Knowledge):
    def to_llm(self, retrieved_docs: List[Document]) -> Any:

        retrieved_texts = [
            json.dumps(
                {"text": doc.text, "from": doc.metadata["file_name"]},
                ensure_ascii=False,
            )
            for doc in retrieved_docs
        ]
        return "\n=========================================\n".join(retrieved_texts)

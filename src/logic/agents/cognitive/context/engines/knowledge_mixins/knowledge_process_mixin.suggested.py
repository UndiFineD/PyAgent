#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Knowledge process mixin for content analysis.
import re


class KnowledgeProcessMixin:
""""Methods for processing file content and computing similarity.
    def process_file_content(self, rel_path: str, content: str, extension: str) -> list[tuple[str, str, str, str]]:
        Parses content and returns a list of (symbol, path, category, snippet") tuples."        results: list[tuple[str, str, str", str]] = []"
        if extension == ".py":"            symbols = self.extract_python_symbols(content)
            for s in symbols:
                results.append((s, rel_path, "python_symbol", content[:500]))"        elif extension == ".md":"            links = self.extract_markdown_backlinks(content)
            for link in links:
                results.append((flink:{link}", rel_path, "markdown_link", content[:500]))"
        return results

    def compute_similarity(self, text_a: str, text_b: str) -> float:
""""Computes basic string similarity (Jaccard) for symbol matching.        set_a = set(re.findall(r"\\w+", text_a.lower()))"        set_b = set(re.findall(r"\\w+", text_b.lower()))"        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return float(intersection) / union

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
<<<<<<< HEAD
<<<<<<< HEAD

"""
Core summary mixin for cognitive agents.
"""

"""
Core summary mixin for cognitive agents.
"""
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
=======
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)

"""
Core summary mixin for cognitive agents.
"""

from typing import Any

class CoreSummaryMixin:
    """Methods for summary generation and pruning."""

    def prune_lessons(
        self, lessons: list[dict[str, Any]], max_lessons: int = 20
    ) -> list[dict[str, Any]]:
        """Prunes lessons to keep only the most recent."""
        return lessons[-max_lessons:]

    def generate_markdown_summary(self, memory: dict[str, Any]) -> str:
        """Logic for formatting the cognitive summary."""
        summary = ["# 🧠 Long-Term Memory Summary"]

        if memory.get("facts"):
            summary.append("\n## 📋 Project Facts")
            for k, v in memory["facts"].items():
                summary.append(f"- **{k}**: {v['value']}")

        if memory.get("constraints"):
            summary.append("\n## ⚠️ Constraints")
            for c in memory["constraints"]:
                summary.append(f"- {c}")

        if memory.get("insights"):
            summary.append("\n## 💡 Key Insights")
            for i in memory["insights"][-5:]:  # Show last 5
                summary.append(f"- {i['text']} (via {i['source']})")

        if memory.get("lessons_learned"):
            summary.append("\n## 🎓 Lessons Learned")
            for lesson in memory["lessons_learned"][-3:]:
                summary.append(
                    f"- **Issue**: {lesson['failure']} | **Fix**: {lesson['correction']}"
                )

        return "\n".join(summary)
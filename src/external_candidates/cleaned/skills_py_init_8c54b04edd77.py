# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\dgriffin831.py\skill_scan.py\skill_scan.py\init_8c54b04edd77.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\dgriffin831\skill-scan\skill_scan\__init__.py

"""skill-scan — Agent Security Scanner.



Public API and convenience functions.

"""

from __future__ import annotations


__version__ = "0.3.0"


import json

from pathlib import Path


from .alignment_analyzer import AlignmentAnalyzer

from .clawhub import download_skill_for_scan, get_skill_info, search_skills

from .llm_analyzer import LLMAnalyzer

from .meta_analyzer import MetaAnalyzer

from .reporter import format_compact_report, format_moltbook_post, format_text_report

from .scanner import SkillScanner


__all__ = [
    "SkillScanner",
    "LLMAnalyzer",
    "AlignmentAnalyzer",
    "MetaAnalyzer",
    "format_text_report",
    "format_compact_report",
    "format_moltbook_post",
    "search_skills",
    "download_skill_for_scan",
    "get_skill_info",
    "quick_scan",
    "quick_content_scan",
]


def _load_rules() -> list[dict]:
    rules_path = Path(__file__).parent.parent / "rules" / "dangerous-patterns.json"

    data = json.loads(rules_path.read_text())

    return data["rules"]


def quick_scan(
    skill_path: str,
    options: dict | None = None,
) -> tuple[dict, str]:
    """Quick scan — one function to scan a path and get a report.



    Returns (report_dict, formatted_text).

    """

    options = options or {}

    rules = _load_rules()

    scanner = SkillScanner(rules)

    report = scanner.scan_directory(skill_path)

    if options.get("format") == "compact":
        return report, format_compact_report(report, options.get("name"))

    return report, format_text_report(report)


def quick_content_scan(
    content: str,
    source: str = "unknown",
) -> list[dict]:
    """Quick content scan — scan arbitrary text for threats."""

    rules = _load_rules()

    scanner = SkillScanner(rules)

    return scanner.scan_content(content, source)

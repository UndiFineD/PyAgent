
"""
Web search essay agent.py module.
"""
# Copyright 2026 PyAgent Authors
# WebSearchEssayAgent: Research-driven Essay Writing Specialist - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.search_agent import SearchAgent

__version__ = VERSION


class EssayStyle(Enum):
    ACADEMIC = "academic"
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    JOURNALISTIC = "journalistic"
    PERSUASIVE = "persuasive"
    EXPOSITORY = "expository"


class EssayLength(Enum):
    SHORT = "short"  # ~500 words
    MEDIUM = "medium"  # ~1000 words
    LONG = "long"  # ~2000 words
    COMPREHENSIVE = "comprehensive"  # ~3000+ words


@dataclass
class Source:
    """Represents a research source."""

    title: str
    url: str
    snippet: str
    relevance: float = 0.0
    date: Optional[str] = None


@dataclass
class EssayOutline:
    """Represents an essay outline."""

    title: str
    thesis: str
    sections: List[Dict[str, Any]]
    sources: List[Source]


class WebSearchEssayAgent(SearchAgent):
    """
    Agent that researches complex subjects via web search and
    composes structured essays based on findings.
    """

    def __init__(self, context: str) -> None:
        super().__init__(context)
        self._research_cache: Dict[str, List[Source]] = {}
        self._essay_history: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Subject WebSearch Essay Writing Agent. Your task is to: "
            "1. Research the provided subject using web search tools. "
            "2. Synthesize information from multiple sources. "
            "3. Write a high-quality, academic or professional essay with proper citations. "
            "4. Ensure logical flow, clear argumentation, and proper structure."
        )

    @as_tool
    async def write_essay(
        self,
        subject: str,
        length: str = "medium",
        style: str = "academic",
        include_citations: bool = True,
        target_audience: str = "general",
    ) -> Dict[str, Any]:
        """Researches a subject and writes an essay."""
        logging.info(f"WebSearchEssayAgent: Researching subject: {subject}")

        essay_style = EssayStyle(style) if style in [s.value for s in EssayStyle] else EssayStyle.ACADEMIC
        essay_length = EssayLength(length) if length in [ell.value for ell in EssayLength] else EssayLength.MEDIUM

        word_targets = {
            EssayLength.SHORT: 500,
            EssayLength.MEDIUM: 1000,
            EssayLength.LONG: 2000,
            EssayLength.COMPREHENSIVE: 3000,
        }
        target_words = word_targets.get(essay_length, 1000)

        # Step 1: Multi-query research
        sources = await self._research_topic(subject)

        # Step 2: Generate outline
        outline = await self._generate_outline(subject, sources, essay_style)

        # Step 3: Compose essay
        essay_prompt = (
            f"Subject: {subject}\n"
            f"Style: {essay_style.value}\n"
            f"Target Audience: {target_audience}\n"
            f"Target Length: ~{target_words} words\n\n"
            f"Outline:\n{json.dumps(outline, indent=2)}\n\n"
            f"Research Sources:\n{self._format_sources(sources)}\n\n"
            "Write a well-structured essay following the outline. "
            f"{'Include inline citations in [Author, Year] format.' if include_citations else ''}\n"
            "Ensure:\n"
            "1. Strong introduction with clear thesis\n"
            "2. Well-developed body paragraphs with evidence\n"
            "3. Smooth transitions between sections\n"
            "4. Compelling conclusion that synthesizes the argument\n"
            "5. Professional tone appropriate for the style"
        )

        essay = await self.improve_content(essay_prompt)

        # Step 4: Generate references if citations included
        references = ""
        if include_citations:
            references = await self._generate_references(sources)

        result = {
            "subject": subject,
            "style": essay_style.value,
            "essay": essay,
            "references": references if include_citations else None,
            "sources_used": len(sources),
            "target_words": target_words,
            "estimated_words": len(essay.split()),
        }

        self._essay_history.append(
            {"subject": subject, "timestamp": time.time(), "word_count": result["estimated_words"]}
        )

        return result

    @as_tool
    async def research_topic(self, subject: str, depth: str = "standard") -> Dict[str, Any]:
        """Performs in-depth research on a topic without writing an essay."""
        sources = await self._research_topic(subject, depth)

        # Synthesize findings
        synthesis_prompt = (
            f"Synthesize the key findings from this research on '{subject}':\n\n"
            f"{self._format_sources(sources)}\n\n"
            "Provide:\n"
            "1. Key facts and statistics\n"
            "2. Main arguments/perspectives\n"
            "3. Areas of consensus\n"
            "4. Controversies or debates\n"
            "5. Gaps in available information\n"
            "Output JSON: {'key_facts': [...], 'perspectives': [...], 'consensus': [...], "
            "'controversies': [...], 'gaps': [...]}"
        )

        res = await self.improve_content(synthesis_prompt)

        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                synthesis = json.loads(match.group(1))
            else:
                synthesis = {"raw": res}
        except Exception:
            synthesis = {"raw": res}

        return {
            "subject": subject,
            "sources": [{"title": s.title, "url": s.url, "snippet": s.snippet} for s in sources],
            "synthesis": synthesis,
        }

    @as_tool
    async def generate_outline(self, subject: str, style: str = "academic", num_sections: int = 4) -> Dict[str, Any]:
        """Generates an essay outline for a subject."""
        sources = await self._research_topic(subject, "light")
        essay_style = EssayStyle(style) if style in [s.value for s in EssayStyle] else EssayStyle.ACADEMIC

        outline = await self._generate_outline(subject, sources, essay_style, num_sections)

        return {"subject": subject, "style": essay_style.value, "outline": outline}

    @as_tool
    async def fact_check(self, claim: str) -> Dict[str, Any]:
        """Fact-checks a claim using web search."""
        logging.info(f"WebSearchEssayAgent: Fact-checking: {claim}")

        # Search for verification
        search_query = f"fact check {claim}"
        search_data = self._search_duckduckgo(search_query)

        prompt = (
            f"Claim to fact-check: {claim}\n\n"
            f"Search Results:\n{search_data}\n\n"
            "Analyze whether this claim is:\n"
            "1. TRUE - supported by evidence\n"
            "2. FALSE - contradicted by evidence\n"
            "3. PARTIALLY TRUE - some aspects are accurate\n"
            "4. UNVERIFIABLE - insufficient evidence\n\n"
            "Output JSON: {'verdict': '...', 'confidence': 0-1, 'evidence': [...], 'explanation': '...'}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw": res}

    @as_tool
    async def compare_perspectives(self, topic: str, perspectives: List[str]) -> Dict[str, Any]:
        """Compares different perspectives on a topic."""
        # Research each perspective
        all_findings = []
        for perspective in perspectives:
            query = f"{topic} {perspective}"
            data = self._search_duckduckgo(query)
            all_findings.append({"perspective": perspective, "findings": data})

        prompt = (
            f"Topic: {topic}\n\n"
            f"Perspectives to compare:\n"
            + "\n".join([f"**{p['perspective']}**:\n{p['findings'][:1000]}" for p in all_findings])
            + "\n\nProvide a balanced comparison:\n"
            "1. Key arguments for each perspective\n"
            "2. Strengths and weaknesses\n"
            "3. Common ground\n"
            "4. Irreconcilable differences\n"
            "Output JSON: {'comparison': {...}, 'common_ground': [...], 'key_differences': [...]}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw": res}

    async def _research_topic(self, subject: str, depth: str = "standard") -> List[Source]:
        """Performs multi-query research on a topic."""
        if subject in self._research_cache:
            return self._research_cache[subject]

        queries = [
            f"comprehensive overview {subject}",
            f"{subject} latest research 2025 2026",
            f"{subject} expert analysis",
        ]

        if depth == "deep":
            queries.extend(
                [
                    f"{subject} statistics data",
                    f"{subject} criticism controversy",
                    f"{subject} future trends predictions",
                ]
            )

        sources = []
        for query in queries:
            try:
                data = self._search_duckduckgo(query)
                # Parse search results into sources
                source = Source(
                    title=f"Search: {query}", url="duckduckgo.com", snippet=data[:500] if data else "", relevance=0.8
                )
                sources.append(source)
            except Exception as e:
                logging.debug(f"Search failed for query '{query}': {e}")

        self._research_cache[subject] = sources
        return sources

    async def _generate_outline(
        self, subject: str, sources: List[Source], style: EssayStyle, num_sections: int = 4
    ) -> Dict[str, Any]:
        """Generates an essay outline."""
        prompt = (
            f"Create an essay outline for: {subject}\n"
            f"Style: {style.value}\n"
            f"Number of body sections: {num_sections}\n\n"
            f"Available research:\n{self._format_sources(sources)}\n\n"
            "Output JSON:\n"
            "{\n"
            '  "title": "Essay title",\n'
            '  "thesis": "Clear thesis statement",\n'
            '  "sections": [\n'
            '    {"heading": "Introduction", "points": ["hook", "context", "thesis"]},\n'
            '    {"heading": "Body 1", "points": ["topic sentence", "evidence", "analysis"]},\n'
            "    ...\n"
            '    {"heading": "Conclusion", "points": ["restate thesis", "synthesis", "call to action"]}\n'
            "  ]\n"
            "}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"title": subject, "thesis": "", "sections": []}

    async def _generate_references(self, sources: List[Source]) -> str:
        """Generates a references section."""
        ref_prompt = (
            "Format these sources as APA-style references:\n\n"
            + "\n".join([f"- {s.title}: {s.url}" for s in sources])
            + "\n\nOutput only the formatted reference list."
        )
        return await self.improve_content(ref_prompt)

    def _format_sources(self, sources: List[Source]) -> str:
        """Formats sources for prompts."""
        return "\n\n".join([f"**{s.title}**\nURL: {s.url}\n{s.snippet}" for s in sources])

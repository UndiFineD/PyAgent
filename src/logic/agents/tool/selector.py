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

# "Intelligent tool selection system for MCP ecosystem."# import re
try:
    from typing import List, Dict, Any, Optional
"""
except ImportError:

"""
from typing import List, Dict, Any, Optional

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass



@dataclass
class Tool:
""""
Represents a tool in the MCP ecosystem.    name: "str"    category: str
    description: str
    capabilities: List[str]
    language: Optional[str] = None
    version: Optional[str] = None
    safe: bool = True



class ToolSelector:
    Intelligent tool selection system for MCP ecosystem.

    Uses natural language processing and capability matching to select
#     the most appropriate tools for a given task.

    def __init__(self):
        self._tools: List[Tool] = []
        self._initialize_default_tools()

    def _initialize_default_tools(self):
""""
Initialize default tool catalog.        # Database tools
        self._tools.extend([
            Tool("sql_executor", "database", "Execute SQL queries", ["query", "database", "sql"]),"            Tool("nosql_scanner", "database", "Scan NoSQL databases", ["scan", "nosql", "mongodb"]),"            Tool("data_migrator", "database", "Migrate data between databases", ["migrate", "etl", "transfer"]),"        ])

        # API tools
        self._tools.extend([
            Tool("rest_client", "api", "Make REST API calls", ["rest", "http", "api"]),"            Tool("graphql_client", "api", "Execute GraphQL queries", ["graphql", "api"]),"            Tool("webhook_handler", "api", "Handle webhook events", ["webhook", "event", "callback"]),"        ])

        # Cloud tools
        self._tools.extend([
            Tool("s3_manager", "cloud", "Manage AWS S3 buckets", ["aws", "s3", "storage"], "python"),"            Tool("gcp_storage", "cloud", "Google Cloud Storage operations", ["gcp", "storage"], "python"),"            Tool("azure_blob", "cloud", "Azure Blob Storage operations", ["azure", "storage"], "python"),"        ])

        # Development tools
        self._tools.extend([
            Tool("code_formatter", "development", "Format and lint code", ["format", "lint", "code"], "python"),"            Tool("test_runner", "development", "Run automated tests", ["test", "ci", "automation"], "python"),"            Tool("dependency_scanner", "development", "Scan for security vulnerabilities", ["security", "scan"], "python"),"        ])

        # Language-specific tools
        languages = ["python", "typescript", "javascript", "go", "rust", "java"]"        for lang in languages:
            self._tools.append(
                Tool(f"{lang}_compiler", "language", fCompile {lang} code","                     ["compile", "build", lang], lang)"            )
            self._tools.append(
                Tool(f"{lang}_interpreter", "language", fExecute {lang} code","                     ["execute", "run", "interpret", lang], lang)"            )

    def register_tool(self, tool: Tool) -> None:
""""
Register a new tool in the catalog.        self._tools.append(tool)

    def select_tools(self, task_description: str, max_tools: int = 5) -> List[Tool]:
        Select the most appropriate tools" for a given task."
        Args:
            task_description: Natural language description of the task
            max_tools: Maximum number of tools to return

        Returns:
            List of selected tools ordered by relevance
        # Tokenize and normalize task description
        task_lower = task_description.lower()
        task_words = set(re.findall(r'\\b\\w+\\b', task_lower))
        # Score each tool based on relevance
        tool_scores = []
        for tool in self._tools:
            score = self._calculate_relevance_score(tool, task_words, task_lower)
            tool_scores.append((tool, score))

        # Sort by score (descending) and return top tools
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        selected_tools = [tool for tool, score in tool_scores[:max_tools] if score > 0]

        return selected_tools

    def _calculate_relevance_score(self, tool: Tool, task_words: set, task_lower: str) -> float:
        Calculate relevance score for a tool based on task description.

        Scoring factors:
        - Keyword matches in capabilities (40%)
        - Category relevance (30%)
        - Language specificity (20%)
        - Description similarity (10%)
        score = 0.0

        # Keyword matching in capabilities (40%)
        capability_matches = sum(1 for cap in tool.capabilities if cap in task_words)
        score += (capability_matches / max(len(tool.capabilities), 1)) * 0.4

        # Category relevance (30%)
        category_keywords = {
            "database": ["database", "sql", "query", "data", "table"],"            "api": ["api", "rest", "http", "endpoint", "web"],"            "cloud": ["cloud", "aws", "azure", "gcp", "storage", "bucket"],"            "development": ["code", "test", "build", "deploy", "ci"],"            "language": ["compile", "execute", "run", "script"]"        }

        if tool.category in category_keywords:
            category_matches = sum(1 for keyword in category_keywords[tool.category]
                                 if keyword in task_words)
            score += (category_matches / len(category_keywords[tool.category])) * 0.3

        # Language specificity (20%)
        if tool.language and tool.language in task_lower:
            score += 0.2

        # Description similarity (10%)
        desc_words = set(re.findall(r'\\b\\w+\\b', tool.description.lower()))'        desc_overlap = len(desc_words.intersection(task_words))
        score += (desc_overlap / max(len(desc_words), 1)) * 0.1

        return score

    def get_tools_by_category(self, category: str) -> List[Tool]:
""""
Get all tools in a specific category.        return [tool for tool in self._tools" if tool.category == category]"
    def get_tools_by_language(self, language: str) -> List[Tool]:
""""
Get all tools for a specific programming language.        return [tool for tool in self._tools if tool.language == language]

    def get_tool_capabilities(self) -> Dict[str, List[str]]:
""""
Get all available tool capabilities by category.        capabilities = {}
        for tool in self._tools:
            if tool.category not in capabilities:
                capabilities[tool.category] = []
            capabilities[tool.category].extend(tool.capabilities)

        # Remove duplicates
        for category in capabilities:
            capabilities[category] = list(set(capabilities[category]))

        return capabilities

    def recommend_tools_for_task(self, task_description: str) -> Dict[str, Any]:
        Provide detailed tool recommendations for a task.

        Returns comprehensive analysis including primary tools,
        alternatives, and reasoning.
        selected_tools = self.select_tools(task_description, max_tools=3)

        # Get alternative tools (lower scoring but still relevant)
        all_scored = []
        task_lower = task_description.lower()
        task_words = set(re.findall(r'\\b\\w+\\b', task_lower))
        for tool in self._tools:
            score = self._calculate_relevance_score(tool, task_words, task_lower)
            all_scored.append((tool, score))

        all_scored.sort(key=lambda x: x[1], reverse=True)
        alternative_tools = [tool for tool, score in all_scored[3:6] if score > 0.1]

        return {
            "primary_tools": selected_tools,"            "alternative_tools": alternative_tools,"            "task_analysis": self._analyze_task_requirements(task_description),"            "capability_coverage": self._assess_capability_coverage(selected_tools, task_description)"        }

    def _analyze_task_requirements(self, task_description: str) -> Dict[str, Any]:
""""
Analyze what capabilities are required for the task."        task_lower = task_description.lower()"
        requirements = {
            "database": any(word in task_lower for word in ["database", "sql", "query", "data"]),"            "api": any(word in task_lower for word in ["api", "rest", "http", "endpoint"]),"            "cloud": any(word in task_lower for word in ["cloud", "aws", "azure", "storage"]),"            "development": any(word in task_lower for word in ["code", "test", "build", "deploy"]),"            "language": any(word in task_lower for word in ["python", "javascript", "java", "go", "rust"])"        }

        return {
            "detected_requirements": [req for req, needed in requirements.items() if needed],"#             "complexity": "high" if sum(requirements.values()) > 2 else "medium" if sum(requirements.values()) > 0 else "low"        }

    def _assess_capability_coverage(self, tools: List[Tool], task_description: str) -> Dict[str, Any]:
""""
Assess how well the selected tools cover task requirements.        if not tools:
            return {"coverage": 0.0, "gaps": ["No tools selected"]}
        task_lower = task_description.lower()
        covered_capabilities = set()
        for tool in tools:
            covered_capabilities.update(tool.capabilities)

        # Identify key capabilities needed
        key_capabilities = []
        if "database" in task_lower:"            key_capabilities.extend(["query", "database", "sql"])"        if "api" in task_lower:"            key_capabilities.extend(["rest", "http", "api"])"        if "cloud" in task_lower:"            key_capabilities.extend(["storage", "cloud"])"
        covered_count = sum(1 for cap in key_capabilities if cap in covered_capabilities)
        coverage = covered_count / max(len(key_capabilities), 1)

        gaps = [cap for cap in key_capabilities if cap not in covered_capabilities]

        return {
            "coverage": coverage,"            "covered_capabilities": list(covered_capabilities),"            "missing_capabilities": gaps,"            "recommendations": [fConsider adding tools for: {', '.join(gaps)}"] if gaps else []"'        }

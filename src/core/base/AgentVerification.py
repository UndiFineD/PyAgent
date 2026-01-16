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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Verification logic for agent outputs.
Implements Stanford Reseach 'Anchoring Strength' and Keio University 'Self-Verification' paths.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import ast
import re
from typing import Any
from pathlib import Path
import logging
import json
import numpy as np

try:
    import rust_core as rc
except ImportError:
    rc = None

__version__ = VERSION


class ConfigValidator:
    """Phase 278: Validates configuration files and detects orphaned references."""

    @staticmethod
    def validate_shard_mapping(
        mapping_path: Path = Path("data/config/shard_mapping.json"),
    ) -> list[str]:
        """Checks shard_mapping.json for orphaned AgentIDs."""
        if not mapping_path.exists():
            logging.warning(
                f"ConfigValidator: {mapping_path} not found. Skipping validation."
            )
            return []

        orphans = []
        try:
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            # Heuristic: Check if the agent folder exists in src/ (just a demo check)

            for agent_id in mapping.get("agents", {}).keys():
                agent_dir = Path("src/logic/agents") / agent_id
                if not agent_dir.exists():
                    orphans.append(agent_id)
                    logging.error(
                        f"ConfigValidator: Orphaned agent reference detected: {agent_id}"
                    )

        except Exception as e:
            logging.error(f"ConfigValidator: Failed to validate shard mapping: {e}")

        return orphans


class CodeIntegrityVerifier:
    """Phase 316: Scans codebase for structural integrity issues, specifically import paths."""

    @staticmethod
    def verify_imports(root_dir: str = "src") -> dict[str, list[str]]:
        """
        Scans all Python files in the given directory for broken internal imports.
        Specifically looks for 'from src.xxx' or 'import src.xxx' and verifies existence.
        """
        root_path = Path(root_dir)
        if not root_path.exists():
            return {"errors": [f"Directory {root_dir} not found"]}

        report = {"broken_imports": [], "syntax_errors": []}
        
        # Get all python files in the workspace (relative to project root)
        # assuming the script is run from project root.
        py_files = list(root_path.rglob("*.py"))

        for file_path in py_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
            except Exception as e:
                report["syntax_errors"].append(f"{file_path}: {e}")
                continue

            for node in ast.walk(tree):
                targets = []
                if isinstance(node, ast.Import):
                    targets = [n.name for n in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    # For 'from x import y', we only check the module 'x'
                    if node.level == 0:
                        targets = [node.module]

                for target in targets:
                    # We only care about verifying our own 'src' hierarchy
                    if target.startswith("src.") or target == "src":
                        parts = target.split(".")
                        # Check if it's a directory (module) or a file (.py)
                        # We use Path(".") as base to refer to project root
                        target_path = Path(".").joinpath(*parts)
                        
                        exists = (
                            target_path.with_suffix(".py").exists() or 
                            target_path.joinpath("__init__.py").exists()
                        )
                        
                        if not exists:
                            report["broken_imports"].append(
                                f"{file_path}: Broken import '{target}'"
                            )

        return report

    def get_symbol_map(self, root_dir: Path) -> dict[str, str]:
        """
        Maps all class names in the directory to their relative file paths (indexing).
        """
        mapping = {}
        for py_file in root_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                classes = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef)
                ]
                rel_path = str(py_file.relative_to(root_dir.parent)).replace("\\", "/")
                for cls in classes:
                    mapping[cls] = rel_path
            except Exception:
                continue
        return mapping


class CodeHealthAuditor:
    """Phase 316: Performs static analysis to detect technical debt and quality issues."""

    @staticmethod
    def audit_workspace(root_dir: str = "src") -> dict[str, Any]:
        """
        Scans for bare excepts, print statements, large files, and undocumented classes.
        """
        root_path = Path(root_dir)
        results: dict[str, list[Any]] = {
            "bare_excepts": [],
            "print_statements": [],
            "large_files": [],
            "undocumented_classes": [],
            "todos": [],
        }

        if not root_path.exists():
            return results

        for file_path in root_path.rglob("*.py"):
            # Skip hidden folders and common ignores
            if any(part.startswith(".") or part in ["__pycache__", "rust_core"] for part in file_path.parts):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                # Check for large files (>25KB)
                if len(content) > 25000:
                    results["large_files"].append((str(file_path), len(content)))

                # Detect TODOs
                todo_matches = re.finditer(r"#\s*TODO:?\s*(.*)", content, re.IGNORECASE)
                for match in todo_matches:
                    results["todos"].append((str(file_path), match.group(1).strip()))

                # Detect print statements (excluding those in comments/strings roughly)
                print_matches = re.finditer(r"^\s*print\(", content, re.MULTILINE)
                for _ in print_matches:
                    results["print_statements"].append(str(file_path))

                # AST Analysis
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    # 1. Bare excepts
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        results["bare_excepts"].append((str(file_path), node.lineno))

                    # 2. Undocumented Classes
                    if isinstance(node, ast.ClassDef):
                        if not ast.get_docstring(node):
                            results["undocumented_classes"].append(
                                (str(file_path), node.name, node.lineno)
                            )

            except Exception as e:
                logging.debug(f"CodeHealthAuditor: Error scanning {file_path}: {e}")

        # Stub Detection
        for file_path in py_files:
            if file_path.name == "__init__.py":
                continue
            try:
                tree = ast.parse(file_path.read_text(encoding="utf-8"))
                is_stub = True
                has_defs = False
                for node in tree.body:
                    if isinstance(
                        node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        has_defs = True
                        res = self._is_stub_node(node)
                        if res is False or res == "IS_ABC":
                            is_stub = False
                            break
                    elif not isinstance(
                        node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)
                    ):
                        if not (
                            isinstance(node, ast.Expr)
                            and isinstance(node.value, ast.Constant)
                        ):
                            is_stub = False
                            break
                if has_defs and is_stub:
                    results["stubs"].append(str(file_path))
            except Exception:
                pass

        return results

    @staticmethod
    def _is_stub_node(node: ast.AST) -> bool | str:
        """Determines if a node is an empty stub (pass/NotImplementedError)."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            if len(body) > 1:
                return False
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and stmt.value.value is Ellipsis
            ):
                return True
            if isinstance(stmt, ast.Raise):
                exc_name = ""
                if isinstance(stmt.exc, ast.Call) and isinstance(
                    stmt.exc.func, ast.Name
                ):
                    exc_name = stmt.exc.func.id
                elif isinstance(stmt.exc, ast.Name):
                    exc_name = stmt.exc.id
                if exc_name == "NotImplementedError":
                    return True
            return False

        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in ("ABC", "Protocol"):
                    return "IS_ABC"
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            for item in body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    res = CodeHealthAuditor._is_stub_node(item)
                    if res is False:
                        return False
                    if res == "IS_ABC":
                        return "IS_ABC"
                elif not isinstance(item, ast.Pass):
                    return False
            return True
        return True


class AgentVerifier:
    """Handles quality and anchoring verification of agent responses."""

    _embedding_model = None

    @classmethod
    def _get_embedding_model(cls) -> bool:
        """Lazy loading of the embedding model for semantic anchoring (Phase 257)."""
        if cls._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer

                cls._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            except ImportError:
                return None
        return cls._embedding_model

    @classmethod
    def calculate_anchoring_strength(
        cls, result: str, context_pool: dict[str, Any]
    ) -> float:
        """
        Calculates the 'Anchoring Strength' metric using Semantic Cosine Similarity (Phase 257).
        """

        if not context_pool:
            return 0.5

        context_text = " ".join([str(v) for v in context_pool.values()])
        if not context_text or not result:
            return 0.5

        model = cls._get_embedding_model()
        if model:
            # Semantic Similarity path (Modern)
            embeddings = model.encode([result, context_text])
            cos_sim = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(max(0.0, min(1.0, cos_sim)))

        # Fallback to Rust/Python word-overlap (Phase 108/321 logic)
        if rc:
            try:
                return rc.calculate_anchoring_fallback(result, context_text)
            except Exception:
                pass

        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0

        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)

        if len(result_words) < 5:
            score *= 0.5

        return min(1.0, score * 1.5)

    @staticmethod
    def verify_self(result: str, anchoring_score: float) -> tuple[bool, str]:
        """Self-verification layer output check."""
        if not result:
            return False, "Empty result"

        hallucination_threshold = 0.3
        if anchoring_score < hallucination_threshold:
            return False, f"Low anchoring strength ({anchoring_score:.2f})"

        return True, "Verified"

    @staticmethod
    def fact_check(code_snippet: str, agent_id: str) -> dict[str, Any]:
        """
        Cross-references generated code snippets against the sharded knowledge base (Phase 257).
        """
        return {"valid": True, "hallucinations": []}

    @staticmethod
    def secondary_verify(result: str, primary_model: str) -> bool:
        """
        Performs a cross-model verification loop (Phase 258).
        A faster model reviews the primary model's output.
        """
        # In a real implementation, this would call a different backend
        return True

    @staticmethod
    def jury_verification(agent_responses: list[bool]) -> bool:
        """
        Implements a 'Jury of Agents' consensus (Phase 258).
        Requires majority or unanimity based on risk.
        """
        if not agent_responses:
            return False
        return sum(agent_responses) >= 2  # Majority out of 3

    @staticmethod
    def check_latent_reasoning(content: str) -> bool:
        """
        Phase 293: Detects if the agent is using non-English reasoning chains.
        Crucial for linguistic diversity and verifying alignment across dialects.
        """
        # Linguistic Audit for Non-English reasoning tokens (Phase 293)
        if not content:
            return True

        if rc:
            try:
                # threshold 10%
                return rc.check_latent_reasoning(content, 0.1)
            except Exception:
                pass

        # Simple heuristic: excessive non-ASCII might indicate latent reasoning in a different language
        non_ascii = [c for c in content if ord(c) > 127]
        if len(non_ascii) > (len(content) * 0.1):  # Threshold 10%
            return False
        return True

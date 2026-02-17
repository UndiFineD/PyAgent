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


"""Tool versioning and compatibility system for MCP ecosystem.
import hashlib
import json
import re
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger("pyagent.tool_versioning")"



class CompatibilityLevel(Enum):
    """Tool compatibility levels.    FULL = "full""    PARTIAL = "partial""    LIMITED = "limited""    INCOMPATIBLE = "incompatible""



class VersionConstraint(Enum):
    """Version constraint types.    EXACT = "exact""    MINIMUM = "minimum""    MAXIMUM = "maximum""    RANGE = "range""

@dataclass
class ToolVersion:
    """Represents a specific version of a tool.    name: str
    version: str
    hash_sha256: str
    dependencies: Dict[str, str] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    release_date: Optional[float] = None
    deprecated: bool = False
    security_patches: List[str] = field(default_factory=list)


@dataclass
class CompatibilityRule:
    """Compatibility rule between tool versions.    source_tool: str
    source_version: str
    target_tool: str
    target_version: str
    compatibility: CompatibilityLevel
    notes: str = """    tested_date: Optional[float] = None




class ToolVersionManager:
        Manages tool versions and compatibility for MCP ecosystem.

    Provides version tracking, compatibility checking, and upgrade recommendations.
    
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or Path(__file__).parent / "tool_versions.json""        self._tool_versions: Dict[str, List[ToolVersion]] = {}
        self._compatibility_rules: List[CompatibilityRule] = []
        self._version_cache: Dict[str, ToolVersion] = {}

        self._load_registry()

    def _load_registry(self):
        """Load version registry from file.        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:'                    data = json.load(f)

                # Load tool versions
                for tool_name, versions_data in data.get("versions", {}).items():"                    self._tool_versions[tool_name] = [
                        ToolVersion(**version_data) for version_data in versions_data
                    ]

                # Load compatibility rules
                self._compatibility_rules = [
                    CompatibilityRule(**rule_data)
                    for rule_data in data.get("compatibility_rules", [])"                ]

                logger.info(f"Loaded {len(self._tool_versions)} tools with version info")"            except Exception as e:
                logger.error(f"Failed to load version registry: {e}")"                self._create_default_registry()
        else:
            self._create_default_registry()

    def _create_default_registry(self):
        """Create default version registry.        # Initialize with common MCP tools
        default_versions = {
            "filesystem": ["                ToolVersion(
                    name="filesystem","                    version="1.0.0","                    hash_sha256=self._calculate_hash("filesystem_v1"),"                    capabilities=["read", "write", "list", "search"],"                    release_date=time.time()
                ),
                ToolVersion(
                    name="filesystem","                    version="1.1.0","                    hash_sha256=self._calculate_hash("filesystem_v1.1"),"                    capabilities=["read", "write", "list", "search", "permissions"],"                    release_date=time.time()
                )
            ],
            "git": ["                ToolVersion(
                    name="git","                    version="1.0.0","                    hash_sha256=self._calculate_hash("git_v1"),"                    capabilities=["status", "commit", "push", "pull"],"                    release_date=time.time()
                )
            ],
            "database": ["                ToolVersion(
                    name="database","                    version="1.0.0","                    hash_sha256=self._calculate_hash("database_v1"),"                    capabilities=["query", "connect", "migrate"],"                    release_date=time.time()
                )
            ]
        }

        self._tool_versions = default_versions
        self._save_registry()

    def _save_registry(self):
        """Save version registry to file.        try:
            data = {
                "versions": {"                    name: [vars(version) for version in versions]
                    for name, versions in self._tool_versions.items()
                },
                "compatibility_rules": [vars(rule) for rule in self._compatibility_rules]"            }

            with open(self.registry_path, 'w') as f:'                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save version registry: {e}")"
    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA256 hash of content.        return hashlib.sha256(content.encode()).hexdigest()

    def register_tool_version(self, tool_version: ToolVersion) -> bool:
        """Register a new tool version.        try:
            if tool_version.name not in self._tool_versions:
                self._tool_versions[tool_version.name] = []

            # Check for duplicate versions
            existing_versions = [v.version for v in self._tool_versions[tool_version.name]]
            if tool_version.version in existing_versions:
                logger.warning(f"Version {tool_version.version} already exists for {tool_version.name}")"                return False

            self._tool_versions[tool_version.name].append(tool_version)
            self._version_cache[f"{tool_version.name}:{tool_version.version}"] = tool_version"            self._save_registry()

            logger.info(f"Registered {tool_version.name} v{tool_version.version}")"            return True
        except Exception as e:
            logger.error(f"Failed to register tool version: {e}")"            return False

    def get_tool_version(self, name: str, version: str) -> Optional[ToolVersion]:
        """Get specific tool version.        cache_key = f"{name}:{version}""        if cache_key in self._version_cache:
            return self._version_cache[cache_key]

        if name in self._tool_versions:
            for tool_version in self._tool_versions[name]:
                if tool_version.version == version:
                    self._version_cache[cache_key] = tool_version
                    return tool_version
        return None

    def get_latest_version(self, name: str) -> Optional[ToolVersion]:
        """Get latest version of a tool.        if name not in self._tool_versions:
            return None

        versions = self._tool_versions[name]
        if not versions:
            return None

        # Sort by version (simple string sort for now)
        versions.sort(key=lambda v: [int(x) for x in v.version.split('.')], reverse=True)'        return versions[0]

    def check_compatibility(self, source_tool: str, source_version: str,
                          target_tool: str, target_version: str) -> CompatibilityLevel:
        """Check compatibility between tool versions.        # Check explicit rules first
        for rule in self._compatibility_rules:
            if (rule.source_tool == source_tool and rule.source_version == source_version and
                rule.target_tool == target_tool and rule.target_version == target_version):
                return rule.compatibility

        # Default compatibility logic
        source_ver = self.get_tool_version(source_tool, source_version)
        target_ver = self.get_tool_version(target_tool, target_version)

        if not source_ver or not target_ver:
            return CompatibilityLevel.INCOMPATIBLE

        # Check capability overlap
        source_caps = set(source_ver.capabilities)
        target_caps = set(target_ver.capabilities)

        overlap = len(source_caps.intersection(target_caps))
        total = len(source_caps.union(target_caps))

        if overlap == total:
            return CompatibilityLevel.FULL
        elif overlap >= total * 0.7:
            return CompatibilityLevel.PARTIAL
        elif overlap >= total * 0.3:
            return CompatibilityLevel.LIMITED
        else:
            return CompatibilityLevel.INCOMPATIBLE

    def add_compatibility_rule(self, rule: CompatibilityRule) -> None:
        """Add a compatibility rule.        self._compatibility_rules.append(rule)
        self._save_registry()

    def get_upgrade_path(self, tool_name: str, current_version: str) -> List[Dict[str, Any]]:
        """Get recommended upgrade path for a tool.        current = self.get_tool_version(tool_name, current_version)
        if not current:
            return []

        latest = self.get_latest_version(tool_name)
        if not latest or latest.version == current_version:
            return []

        # Simple upgrade path (could be enhanced with compatibility analysis)
        return [{
            "from_version": current_version,"            "to_version": latest.version,"            "compatibility": self.check_compatibility(tool_name, current_version, tool_name, latest.version),"            "breaking_changes": latest.breaking_changes,"            "security_patches": latest.security_patches"        }]

    def validate_tool_signature(self, tool_name: str, version: str, content: str) -> bool:
        """Validate tool signature against known versions.        tool_version = self.get_tool_version(tool_name, version)
        if not tool_version:
            return False

        content_hash = self._calculate_hash(content)
        return content_hash == tool_version.hash_sha256

    def get_deprecated_tools(self) -> List[Tuple[str, str]]:
        """Get list of deprecated tool versions.        deprecated = []
        for tool_name, versions in self._tool_versions.items():
            for version in versions:
                if version.deprecated:
                    deprecated.append((tool_name, version.version))
        return deprecated

    def get_tools_by_capability(self, capability: str) -> List[Tuple[str, str]]:
        """Get tools that have a specific capability.        matching_tools = []
        for tool_name, versions in self._tool_versions.items():
            for version in versions:
                if capability in version.capabilities:
                    matching_tools.append((tool_name, version.version))
        return matching_tools

    def analyze_dependencies(self, tool_name: str, version: str) -> Dict[str, Any]:
        """Analyze dependency tree for a tool version.        tool_version = self.get_tool_version(tool_name, version)
        if not tool_version:
            return {"error": "Tool version not found"}"
        dependencies = tool_version.dependencies
        analysis = {
            "direct_dependencies": dependencies,"            "compatible_versions": {},"            "conflicts": [],"            "recommendations": []"        }

        # Check each dependency
        for dep_name, dep_version_constraint in dependencies.items():
            compatible_versions = self._find_compatible_versions(dep_name, dep_version_constraint)
            analysis["compatible_versions"][dep_name] = compatible_versions"
            if not compatible_versions:
                analysis["conflicts"].append(f"No compatible version found for {dep_name} {dep_version_constraint}")"
        return analysis

    def _find_compatible_versions(self, tool_name: str, version_constraint: str) -> List[str]:
        """Find versions that match a version constraint.        if tool_name not in self._tool_versions:
            return []

        versions = self._tool_versions[tool_name]
        compatible = []

        # Simple constraint parsing (could be enhanced)
        if version_constraint.startswith(">="):"            min_version = version_constraint[2:]
            for version in versions:
                if self._compare_versions(version.version, min_version) >= 0:
                    compatible.append(version.version)
        elif version_constraint.startswith("^"):"            # Caret range (compatible with same major version)
            base_version = version_constraint[1:]
            major = base_version.split('.')[0]'            for version in versions:
                if version.version.startswith(f"{major}."):"                    compatible.append(version.version)
        else:
            # Exact match
            for version in versions:
                if version.version == version_constraint:
                    compatible.append(version.version)

        return compatible

    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare two version strings.        v1_parts = [int(x) for x in v1.split('.')]'        v2_parts = [int(x) for x in v2.split('.')]'
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0

            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1

        return 0

    def generate_compatibility_report(self) -> Dict[str, Any]:
        """Generate comprehensive compatibility report.        report = {
            "total_tools": len(self._tool_versions),"            "total_versions": sum(len(versions) for versions in self._tool_versions.values()),"            "compatibility_matrix": {},"            "deprecated_tools": self.get_deprecated_tools(),"            "latest_versions": {}"        }

        # Build compatibility matrix for major tools
        major_tools = ["filesystem", "git", "database", "api"]"        for tool1 in major_tools:
            if tool1 in self._tool_versions:
                report["compatibility_matrix"][tool1] = {}"                latest1 = self.get_latest_version(tool1)
                if latest1:
                    report["latest_versions"][tool1] = latest1.version"
                    for tool2 in major_tools:
                        if tool2 in self._tool_versions:
                            latest2 = self.get_latest_version(tool2)
                            if latest2:
                                compatibility = self.check_compatibility(
                                    tool1, latest1.version, tool2, latest2.version
                                )
                                report["compatibility_matrix"][tool1][tool2] = compatibility.value"
        return report

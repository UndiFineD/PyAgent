#!/usr/bin/env python3
""
Minimal, parser-safe Response Modifier Core used for tests.""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import asyncio


@dataclass
class ResponseModificationRule:
    name: str
    condition: str
    target_status: int
    preserve_original: bool = True
    enabled: bool = True


@dataclass
class ModifiedResponse:
    original_status: int
    modified_status: int
    headers: List[str]
    body: bytes
    rule_applied: str
    timestamp: float


class ResponseModifierCore:
    def __init__(self):
        self.modification_rules: List[ResponseModificationRule] = []
        self.modification_history: List[ModifiedResponse] = []
        self.enabled = False

    async def initialize(self) -> bool:
        return True

    async def add_modification_rule(self, rule: ResponseModificationRule) -> None:
        self.modification_rules.append(rule)

    async def remove_modification_rule(self, rule_name: str) -> bool:
        for i, rule in enumerate(self.modification_rules):
            if rule.name == rule_name:
                del self.modification_rules[i]
                return True
        return False

    async def enable_modifications(self) -> None:
        self.enabled = True

    async def disable_modifications(self) -> None:
        self.enabled = False

    async def modify_response(
        self,
        url: str,
        status_code: int,
        headers: List[str],
        body: bytes
    ) -> Tuple[int, List[str], bytes]:
        if not self.enabled:
            return status_code, headers, body

        for rule in self.modification_rules:
            if not rule.enabled:
                continue
            if rule.condition in url:
                modified_status = rule.target_status
                modified_headers = headers.copy()
                modified_body = body
                modified_response = ModifiedResponse(
                    original_status=status_code,
                    modified_status=modified_status,
                    headers=modified_headers,
                    body=modified_body,
                    rule_applied=rule.name,
                    timestamp=asyncio.get_event_loop().time(),
                )
                self.modification_history.append(modified_response)
                return modified_status, modified_headers, modified_body

        return status_code, headers, body

    async def get_modification_history(self, limit: int = 100, rule_filter: Optional[str] = None) -> List[ModifiedResponse]:
        history = self.modification_history
        if rule_filter:
            history = [h for h in history if h.rule_applied == rule_filter]
        return history[-limit:] if limit > 0 else history

    async def clear_history(self) -> None:
        self.modification_history.clear()

    async def get_active_rules(self) -> List[ResponseModificationRule]:
        return [rule for rule in self.modification_rules if rule.enabled]

    async def export_rules(self) -> Dict[str, Any]:
        return {
            "rules": [
                {
                    "name": rule.name,
                    "condition": rule.condition,
                    "target_status": rule.target_status,
                    "preserve_original": rule.preserve_original,
                    "enabled": rule.enabled,
                }
                for rule in self.modification_rules
            ],
            "enabled": self.enabled,
        }

    async def import_rules(self, rules_data: Dict[str, Any]) -> None:
        self.modification_rules.clear()
        for rule_data in rules_data.get("rules", []):
            rule = ResponseModificationRule(
                name=rule_data["name"],
                condition=rule_data["condition"],
                target_status=rule_data["target_status"],
                preserve_original=rule_data.get("preserve_original", True),
                enabled=rule_data.get("enabled", True),
            )
            self.modification_rules.append(rule)
        self.enabled = rules_data.get("enabled", False)

    async def analyze_response_patterns(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        analysis = {
            "total_responses": len(responses),
            "status_distribution": {},
            "modification_suggestions": [],
            "vulnerability_indicators": [],
        }
        for response in responses:
            status = response.get("status_code", 0)
            analysis["status_distribution"][status] = analysis["status_distribution"].get(status, 0) + 1
            if status == 403:
                analysis["vulnerability_indicators"].append("Potential authorization bypass opportunity")
            elif status == 500:
                analysis["vulnerability_indicators"].append("Server error - potential injection point")
            elif status == 401:
                analysis["modification_suggestions"].append("Consider forcing 200 OK to bypass auth")
        return analysis

    async def cleanup(self) -> None:
        self.modification_rules.clear()
        self.modification_history.clear()

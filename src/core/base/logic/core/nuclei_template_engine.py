#!/usr/bin/env python3
"""Minimal, parser-safe Nuclei template engine stub used for tests.

This module provides small dataclasses and a lightweight engine that
can parse simple YAML content and present the expected symbols to
tests without executing real HTTP requests.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging
import yaml


@dataclass
class TemplateInfo:
    name: str
    author: str
    severity: str
    description: str
    reference: Optional[List[str]] = None
    tags: Optional[List[str]] = None


@dataclass
class TemplateRequest:
    method: str
    path: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None


@dataclass
class MatcherCondition:
    type: str
    dsl: Optional[List[str]] = None
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    words: Optional[List[str]] = None
    regex: Optional[List[str]] = None


@dataclass
class TemplateHTTP:
    requests: List[TemplateRequest]
    matchers: List[MatcherCondition]
    matchers_condition: Optional[str] = None


@dataclass
class NucleiTemplate:
    id: str
    info: TemplateInfo
    http: Optional[TemplateHTTP] = None


@dataclass
class ScanResult:
    template_id: str
    url: str
    matched: bool
    info: TemplateInfo
    request_details: Dict[str, Any]
    response_details: Dict[str, Any]
    extracted_data: Optional[Dict[str, Any]] = None


class NucleiTemplateEngine:
    def __init__(self):
        self.templates: Dict[str, NucleiTemplate] = {}
        self.logger = logging.getLogger(__name__)

    def load_template_from_yaml(self, yaml_content: str) -> Optional[NucleiTemplate]:
        try:
            data = yaml.safe_load(yaml_content) or {}
            info_data = data.get('info', {})
            info = TemplateInfo(
                name=info_data.get('name', ''),
                author=info_data.get('author', ''),
                severity=info_data.get('severity', 'info'),
                description=info_data.get('description', ''),
                reference=info_data.get('reference', []),
                tags=info_data.get('tags', []),
            )

            http = None
            http_data = data.get('http')
            if http_data:
                requests_list = []
                for req in http_data.get('requests', []):
                    requests_list.append(TemplateRequest(
                        method=req.get('method', 'GET'),
                        path=req.get('path', '/'),
                        headers=req.get('headers', {}),
                        body=req.get('body'),
                    ))

                matchers = []
                for m in http_data.get('matchers', []):
                    matchers.append(MatcherCondition(
                        type=m.get('type', 'word'),
                        dsl=m.get('dsl'),
                        status_code=m.get('status_code'),
                        headers=m.get('headers'),
                        body=m.get('body'),
                        words=m.get('words'),
                        regex=m.get('regex'),
                    ))

                http = TemplateHTTP(requests=requests_list, matchers=matchers,
                                   matchers_condition=http_data.get('matchers-condition'))

            template = NucleiTemplate(id=data.get('id', ''), info=info, http=http)
            self.templates[template.id] = template
            return template
        except Exception as e:
            self.logger.error(f"Failed to parse template: {e}")
            return None

    def load_template_from_file(self, file_path: str) -> Optional[NucleiTemplate]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.load_template_from_yaml(content)
        except Exception as e:
            self.logger.error(f"Failed to load template from {file_path}: {e}")
            return None

    async def scan_url_with_template(self, template: NucleiTemplate, base_url: str) -> Optional[ScanResult]:
        # Minimal stub: never actually perform HTTP requests in tests
        return None

    async def scan_url_with_templates(self, base_url: str,
                                      template_ids: Optional[List[str]] = None) -> List[ScanResult]:
        results: List[ScanResult] = []
        template_ids = template_ids or []
        templates_to_scan = [self.templates.get(tid) for tid in template_ids]
        for template in templates_to_scan:
            if template:
                res = await self.scan_url_with_template(template, base_url)
                if res:
                    results.append(res)
        return results

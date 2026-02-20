#!/usr/bin/env python3
""
Minimal, parser-safe SOP Core used for tests.""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class SopStep:
    id: str
    description: str


@dataclass
class SopManifest:
    domain: str
    steps: List[SopStep] = field(default_factory=list)


class SopCore:
    def __init__(self):
        self.manifests: Dict[str, SopManifest] = {}

    def register_manifest(self, manifest: SopManifest) -> None:
        self.manifests[manifest.domain] = manifest

    def merge_manifests(self, a: SopManifest, b: SopManifest) -> SopManifest:
        merged = SopManifest(domain=f"{a.domain}_{b.domain}", steps=a.steps + b.steps)
        return merged

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\definition\repo_definitions.py
from typing import Set

from feathr.definition.anchor import FeatureAnchor
from feathr.definition.feature import Feature
from feathr.definition.feature_derivations import DerivedFeature
from feathr.definition.source import Source
from feathr.definition.transformation import Transformation


class RepoDefinitions:
    """A list of shareable Feathr objects defined in the project."""

    def __init__(
        self,
        sources: Set[Source],
        features: Set[Feature],
        transformations: Set[Transformation],
        feature_anchors: Set[FeatureAnchor],
        derived_features: Set[DerivedFeature],
    ) -> None:
        self.sources = sources
        self.features = features
        self.transformations = transformations
        self.feature_anchors = feature_anchors
        self.derived_features = derived_features

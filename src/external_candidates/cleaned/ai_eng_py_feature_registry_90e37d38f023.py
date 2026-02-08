# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\registry.py\feature_registry_90e37d38f023.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\registry\feature_registry.py

from abc import ABC, abstractmethod

from typing import List, Tuple

from feathr.definition.anchor import FeatureAnchor

from feathr.definition.feature_derivations import DerivedFeature

class FeathrRegistry(ABC):

    """This is the abstract class for all the feature registries. All the feature registries should implement those interfaces."""

    @abstractmethod

    def register_features(

        self,

        anchor_list: List[FeatureAnchor] = [],

        derived_feature_list: List[DerivedFeature] = [],

    ):

        """Registers features based on the current workspace

        Args:

        anchor_list: List of FeatureAnchors

        derived_feature_list: List of DerivedFeatures

        """

        pass

    @abstractmethod

    def list_registered_features(self, project_name: str) -> List[str]:

        """List all the already registered features under the given project.

        `project_name` must not be None or empty string because it violates the RBAC policy

        """

        pass

    @abstractmethod

    def list_dependent_entities(self, qualified_name: str):

        """

        Returns list of dependent entities for provided entity

        """

        pass

    @abstractmethod

    def delete_entity(self, qualified_name: str):

        """

        Deletes entity if it has no dependent entities

        """

        pass

    @abstractmethod

    def get_features_from_registry(

        self, project_name: str

    ) -> Tuple[List[FeatureAnchor], List[DerivedFeature]]:

        """[Sync Features from registry to local workspace, given a project_name, will write project's features from registry to to user's local workspace]

        Args:

            project_name (str): project name.

        Returns:

            bool: Returns true if the job completed successfully, otherwise False

        """

        pass


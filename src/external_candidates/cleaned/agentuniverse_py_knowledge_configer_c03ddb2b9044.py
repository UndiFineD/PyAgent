# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\base.py\config.py\component_configer.py\configers.py\knowledge_configer_c03ddb2b9044.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\base\config\component_configer\configers\knowledge_configer.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/3/13 12:01

# @Author  : jerry.zzw

# @Email   : jerry.zzw@antgroup.com

# @FileName: knowledge_configer.py

from typing import Dict, List, Optional

from agentuniverse.base.config.component_configer.component_configer import (
    ComponentConfiger,
)

from agentuniverse.base.config.configer import Configer


class KnowledgeConfiger(ComponentConfiger):
    """The KnowledgeConfiger class, which is used to load and manage the Knowledge configuration."""

    def __init__(self, configer: Optional[Configer] = None):
        """Initialize the KnowledgeConfiger."""

        super().__init__(configer)

        self.__name: Optional[str] = None

        self.__description: Optional[str] = None

        self.__ext_info: Optional[Dict] = None

        self.stores: List[str] = []

        self.query_paraphrasers: Optional[List[str]] = []

        self.insert_processors: Optional[List[str]] = []

        self.rag_router: str = "base_router"

        self.post_processors: List[str] = []

        self.readers: Dict[str, str] = dict()

    @property
    def name(self) -> Optional[str]:
        """Return the name of the Knowledge."""

        return self.__name

    @property
    def description(self) -> Optional[str]:
        """Return the description of the Knowledge."""

        return self.__description

    @property
    def ext_info(self) -> Optional[Dict]:
        return self.__ext_info

    def load(self) -> "KnowledgeConfiger":
        """Load the configuration by the Configer object.

        Returns:

            KnowledgeConfiger: the KnowledgeConfiger object

        """

        return self.load_by_configer(self.__configer)

    def load_by_configer(self, configer: Configer) -> "KnowledgeConfiger":
        """Load the configuration by the Configer object.

        Args:

            configer(Configer): the Configer object

        Returns:

            KnowledgeConfiger: the KnowledgeConfiger object

        """

        super().load_by_configer(configer)

        try:
            self.__name = configer.value.get("name")

            self.__description = configer.value.get("description")

            self.__ext_info = configer.value.get("ext_info")

        except Exception as e:
            raise Exception(f"Failed to parse the Knowledge configuration: {e}")

        return self

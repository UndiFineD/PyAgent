# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Grammar Engine.
Delegates to modularized sub-packages in src.infrastructure.engine.structured/.
"""

from .models import (
    FSMState as FSMState,
    FSMTransitionTable as FSMTransitionTable,
    TokenMask as TokenMask,
)
from .base import GrammarEngine as GrammarEngine
from .regex import RegexGrammar as RegexGrammar
from .json_schema import JsonSchemaGrammar as JsonSchemaGrammar
from .choice import ChoiceGrammar as ChoiceGrammar
from .ebnf import EBNFGrammar as EBNFGrammar

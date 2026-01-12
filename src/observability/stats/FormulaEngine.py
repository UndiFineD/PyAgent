#!/usr/bin/env python3
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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Shell for FormulaEngine using pure core logic."""



import logging
from typing import Any, Dict, List, Optional
from .FormulaValidation import FormulaValidation
from .FormulaEngineCore import FormulaEngineCore



































class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation.
    
    Acts as the I/O Shell for FormulaEngineCore.
    """
    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        """Define a formula."""
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        """Define a formula (backward compat)."""
        self.define(name, formula)

    def calculate(self, formula_or_name: str, variables: Optional[Dict[str, Any]] = None) -> float:
        """Calculate formula result via Core."""
        variables = variables or {}
        
        # If formula_or_name is in formulas dict, use stored formula
        formula = self.formulas.get(formula_or_name, formula_or_name)
            
        try:
            return self.core.calculate_logic(formula, variables)
        except Exception as e:
            logging.error(f"Formula calculation failed: {e}")
            return 0.0

    def validate(self, formula: str) -> FormulaValidation:
        """Validate formula syntax via Core."""
        result = self.core.validate_logic(formula)
        return FormulaValidation(
            is_valid=result["is_valid"], 
            error=result["error"]
        )

    def validate_formula(self, formula: str) -> bool:
        """Validate formula syntax (backward compat)."""
        return self.validate(formula).is_valid

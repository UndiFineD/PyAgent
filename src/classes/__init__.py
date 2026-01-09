"""
Core class hierarchy for the PyAgent ecosystem.
"""

# Classes package initialization

from .base_agent import BaseAgent
from .context.KnowledgeAgent import KnowledgeAgent
from .context.GraphContextEngine import GraphContextEngine
from .context.MemoryEngine import MemoryEngine
try:
    from .stats.ObservabilityEngine import ObservabilityEngine
    from .stats.ResourceMonitor import ResourceMonitor
except ImportError:
    # Handle cases where stats might have import issues during heavy refactoring
    pass
from .coder.SecurityGuardAgent import SecurityGuardAgent

from .coder.LintingAgent import LintingAgent
from .coder.SelfOptimizerAgent import SelfOptimizerAgent
from .coder.TypeSafetyAgent import TypeSafetyAgent
from .coder.DocumentationAgent import DocumentationAgent
from .coder.QualityGateAgent import QualityGateAgent
from .coder.ArchAdvisorAgent import ArchAdvisorAgent
from .fleet.FleetManager import FleetManager

from .fleet.AsyncFleetManager import AsyncFleetManager
from .fleet.TaskPlannerAgent import TaskPlannerAgent
from .fleet.WorkflowState import WorkflowState
from .coder.ReasoningAgent import ReasoningAgent
from .coder.SelfHealingAgent import SelfHealingAgent
from .orchestration.ToolRegistry import ToolRegistry
from .context.GlobalContextEngine import GlobalContextEngine



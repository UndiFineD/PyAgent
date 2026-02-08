# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\eval.py\algorithms.py\mcts.py\planning_models_fde7172a48a8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\algorithms\mcts\planning_models.py

from datetime import datetime

from typing import Dict, Optional

from fle.commons.models.conversation import Conversation

from fle.commons.models.game_state import GameState

from fle.commons.models.program import Program

from pydantic import BaseModel, Field


class LanguageOutput(BaseModel):
    id: Optional[int] = None

    response: str

    conversation: Conversation

    parent_id: Optional[int] = None

    state: Optional[GameState] = None

    meta: Optional[dict] = {}

    created_at: datetime = Field(default_factory=datetime.now)

    prompt_token_usage: Optional[int] = None

    completion_token_usage: Optional[int] = None

    token_usage: Optional[int] = None

    version: int = 1

    version_description: str = ""


class TaskOutput(BaseModel):
    task: str

    language_output: Optional[LanguageOutput] = None


class InitialPlanOutput(BaseModel):
    initial_plan: str

    language_output: LanguageOutput


class Step(BaseModel):
    candidate_language_outputs: list[LanguageOutput] = []

    judge_step_str: str = ""

    chosen_step: str = ""

    judge_language_output_step: LanguageOutput = None

    sampled_programs: list[Program] = []

    program: Program = None

    start_state: GameState = None

    end_state: GameState = None

    reward: float = None

    meta: dict = {}


class PlanOutput(BaseModel):
    task: TaskOutput

    initial_plan: Optional[InitialPlanOutput] = None

    final_output: str = ""

    steps: list[Step] = []

    logs: Optional[list] = []

    success: bool = False

    meta: Optional[Dict] = {}

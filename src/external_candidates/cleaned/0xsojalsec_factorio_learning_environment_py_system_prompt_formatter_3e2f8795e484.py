# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\gym_env.py\system_prompt_formatter_3e2f8795e484.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\gym_env\system_prompt_formatter.py


class SystemPromptFormatter:
    """Formats the system prompt for the agent, only including the task and instructions."""

    def __init__(self, include_task=True, include_instructions=True):

        self.include_task = include_task

        self.include_instructions = include_instructions

    def format(self, task, instructions=None):

        parts = []

        if self.include_task and task:
            # Try to get a string description

            desc = getattr(task, "goal_description", str(task))

            parts.append(f"## Task\n{desc}")

        if self.include_instructions and instructions:
            parts.append(f"## Instructions\n{instructions}")

        return "\n\n".join(parts)

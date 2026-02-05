class SystemPromptFormatter:
    def __init__(self, include_task=True, include_instructions=True):
        self.include_task = include_task
        self.include_instructions = include_instructions

    def format(self, task, instructions=None):
        parts = []
        if self.include_task and task:
            desc = getattr(task, "goal_description", str(task))
            parts.append(f"## Task\n{desc}")
        if self.include_instructions and instructions:
            parts.append(f"## Instructions\n{instructions}")
        return "\n\n".join(parts)

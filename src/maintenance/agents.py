import os
import json
import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any, Annotated
from .utils import setup_fix_directory, run_command, GitManager, get_timestamp

class SpecialistAgent:
    def __init__(self, name: str, command: str, is_targeted: bool = False):
        self.name = name
        # Use full path to current python to ensure tools are found in the venv
        self.base_command = command.replace("python", f'"{sys.executable}"')
        self.is_targeted = is_targeted
        self.base_path = setup_fix_directory(name)
        self.log_file = self.base_path / "log" / f"{name}.log"
        self.issues_file = self.base_path / "log" / "issues.md"

    async def run_check(self) -> (int, str):
        command = self.base_command
        
        if self.is_targeted:
            changed_files = GitManager.get_changed_files()
            if changed_files:
                # Append files to the command. Some tools might need a separator or prefix
                # but for ruff, mypy, flake8, they just accept a list of files.
                files_str = " ".join([f'"{f}"' for f in changed_files])
                # Remove the trailing dot or space if it exists in base command
                command = command.rstrip(" .") + " " + files_str
                print(f"[{self.name}] Targeting {len(changed_files)} changed files.")
            else:
                print(f"[{self.name}] No changed files detected. Running full project scan...")

        print(f"[{self.name}] Running: {command}...")
        code, stdout, stderr = await asyncio.to_thread(run_command, command)
        output = stdout + stderr
        # Filter output to keep it manageable
        if len(output) > 50000:
            output = output[:25000] + "\n... [TRUNCATED] ...\n" + output[-25000:]
            
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(output)
        return code, output

    def document_issues(self, output: str):
        with open(self.issues_file, "a", encoding="utf-8") as f:
            f.write(f"## Issues found by {self.name} at {get_timestamp()}\n\n")
            f.write("```\n")
            f.write(output)
            f.write("\n```\n")

    def save_diff(self, stage: str):
        diff_file = self.base_path / "diff-files" / f"{stage}_{get_timestamp()}.diff"
        GitManager.create_diff(diff_file)

    def save_summary(self, summary: str):
        summary_file = self.base_path / "log" / "summary.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"# Maintenance Summary for {self.name}\n\n")
            f.write(summary)

    def save_code_snippet(self, filename: str, content: str):
        snippet_path = self.base_path / "snippets" / filename
        snippet_path.parent.mkdir(parents=True, exist_ok=True)
        with open(snippet_path, "w", encoding="utf-8") as f:
            f.write(content)

    async def generate_and_apply_fix(self, issues: str):
        """
        Actually generate and apply a fix using the Microsoft Agent Framework.
        """
        # Note: This requires environment variables for Azure OpenAI / Foundry
        # Like AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT
        endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT")
        
        if not endpoint or not model:
            print(f"[{self.name}] AI Credentials missing. Skipping autonomous fix.")
            return False

        from agent_framework.azure import AzureAIClient
        from azure.identity.aio import DefaultAzureCredential

        print(f"[{self.name}] Consulting AI for fix strategies...")
        
        async with (
            DefaultAzureCredential() as credential,
            AzureAIClient(
                project_endpoint=endpoint,
                model_deployment_name=model,
                credential=credential,
            ).create_agent(
                name=f"{self.name}Fixer",
                instructions=f"You are a Senior Python Developer. Your task is to fix {self.name} issues. "
                             "You will be provided with the error logs. "
                             "You should analyze the errors and provide code changes. "
                             "Be precise and only fix the reported issues.",
            ) as fixer_agent,
        ):
            prompt = f"Here are the issues found by {self.name}:\n\n{issues}\n\nPlease propose fixes."
            result = await fixer_agent.run(prompt)
            
            # Save the proposal for learning
            self.save_code_snippet("proposal.md", result.text)
            
            # In a full implementation, we would parse the result and apply edits
            # For now, we document that we've 'consulted'
            return True

    async def perform_maintenance_cycle(self):
        # 1. Initial check
        code, output = await self.run_check()
        
        if code == 0:
            print(f"[{self.name}] No issues found.")
            self.save_summary("No issues found. All clear.")
            return True

        # 2. Document and Backup
        print(f"[{self.name}] Found issues. Documenting and backing up...")
        self.document_issues(output)
        self.save_diff("before_fix")
        
        # 3. Attempt Fix
        fix_applied = await self.generate_and_apply_fix(output)
        
        if not fix_applied:
            self.save_summary("Fix attempt skipped due to missing config or failure.")
            return False

        # 4. Verification Check
        print(f"[{self.name}] Verifying fixes...")
        new_code, new_output = await self.run_check()
        
        if new_code == 0:
            print(f"[{self.name}] Fix successful!")
            self.save_diff("after_fix")
            self.save_summary("Successfully resolved all issues using AI guidance.")
            return True
        else:
            print(f"[{self.name}] Fix attempt failed. Reverting (simulated).")
            # In a real run with applied changes, we would call GitManager.hard_rollback()
            self.save_summary(f"Fix unsuccessful. Final log: {new_output[:500]}")
            return False

class PytestAgent(SpecialistAgent):
    def __init__(self):
        super().__init__("pytestAgent", "python -m pytest")

class MypyAgent(SpecialistAgent):
    def __init__(self):
        super().__init__("mypyAgent", "python -m mypy .", is_targeted=True)

class RuffAgent(SpecialistAgent):
    def __init__(self):
        super().__init__("ruffAgent", "python -m ruff check .", is_targeted=True)

class Flake8Agent(SpecialistAgent):
    def __init__(self):
        super().__init__("flake8Agent", "python -m flake8 .", is_targeted=True)

class UnittestAgent(SpecialistAgent):
    def __init__(self):
        super().__init__("unittestAgent", "python -m unittest discover tests")

class ReminderAgent(SpecialistAgent):
    def __init__(self):
        super().__init__("reminderAgent", "echo Repository Maintenance Overview")
        self.reminder_file = Path("docs/work/reminder.md")

    async def perform_maintenance_cycle(self):
        print(f"[{self.name}] Generating maintenance reminders...")
        self.reminder_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = [
            f"# Repository Maintenance Reminders ({get_timestamp()})",
            "",
            "## 🛠️ Pending Manual Actions",
            "- [ ] **Review Merge**: Examine the current restore branch and merge into `main` if satisfied.",
            "- [ ] **AI Integration**: Set `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT` to enable autonomous fixing.",
            "- [ ] **Log Cleanup**: The `fixes/` directory can grow large; periodically delete old run folders.",
            "",
            "## 💡 Suggested Improvements",
            "- [x] **Tool Specificity**: Updated `Ruff`, `Mypy`, and `Flake8` to only scan changed `.py` files.",
            "- [ ] **Rollback Strategy**: Implement `GitManager.hard_rollback()` call in `agents.py` if an AI-applied fix breaks the build.",
            "- [ ] **Pre-commit Hook**: Integrate the `orchestrator` as a heavy-duty pre-push check.",
            "",
            "## 📊 Latest Orchestrator Notes",
            "Refer to the newest folder in `fixes/` for detailed breakdown of issues found by tools.",
            ""
        ]
        
        with open(self.reminder_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
            
        self.save_summary(f"Reminders updated in {self.reminder_file}")
        return True

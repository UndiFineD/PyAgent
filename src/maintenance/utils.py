import os
import datetime
import subprocess
from pathlib import Path

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M")

def setup_fix_directory(agent_name):
    timestamp = get_timestamp()
    base_path = Path("fixes") / agent_name / "date" / timestamp
    
    (base_path / "diff-files").mkdir(parents=True, exist_ok=True)
    (base_path / "log").mkdir(parents=True, exist_ok=True)
    (base_path / "code").mkdir(parents=True, exist_ok=True)
    
    return base_path

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd or os.getcwd(),
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.returncode, result.stdout or "", result.stderr or ""
    except Exception as e:
        return -1, "", str(e)

class GitManager:
    @staticmethod
    def create_restore_point(branch_name=None):
        if not branch_name:
            timestamp = get_timestamp()
            branch_name = f"restore-point-{timestamp}"
        
        _, current_branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
        current_branch = current_branch.strip()
        
        code, stdout, stderr = run_command(f"git checkout -b {branch_name}")
        return branch_name if code == 0 else None, current_branch

    @staticmethod
    def get_changed_files():
        """Returns a list of changed/added python files relative to main or uncommitted."""
        # 1. Uncommitted changes
        _, stdout, _ = run_command("git diff --name-only")
        files = set(stdout.splitlines())
        
        # 2. Files changed in this branch relative to main
        _, stdout_main, _ = run_command("git diff --name-only main")
        files.update(stdout_main.splitlines())
        
        # 3. Filter for Python files only and ensure they exist
        py_files = [f for f in files if f.endswith(".py") and os.path.exists(f)]
        return py_files

    @staticmethod
    def commit_changes(message):
        run_command("git add .")
        code, stdout, stderr = run_command(f'git commit -m "{message}"')
        return code == 0

    @staticmethod
    def create_diff(output_path):
        code, stdout, stderr = run_command(f"git diff main > {output_path}")
        return code == 0

    @staticmethod
    def rollback(branch_name):
        code, stdout, stderr = run_command(f"git checkout {branch_name}")
        return code == 0

    @staticmethod
    def hard_rollback():
        code, stdout, stderr = run_command("git reset --hard HEAD")
        # removed git clean -fd to avoid accidental deletion of fresh files
        return code == 0

    @staticmethod
    def merge_to_main(branch_name):
        run_command("git checkout main")
        run_command("git pull origin main")
        code, stdout, stderr = run_command(f"git merge {branch_name}")
        if code == 0:
            run_command(f"git branch -d {branch_name}")
        return code == 0

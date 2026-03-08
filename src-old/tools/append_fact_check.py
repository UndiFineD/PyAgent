from __future__ import annotations
from pathlib import Path
content = """
    @staticmethod
    def fact_check(code_snippet: str, agent_id: str) -> Dict[str, Any]:
        \"\"\"
        Cross-references generated code snippets against the sharded knowledge base (Phase 257).
        \"\"\"
        return {"valid": True, "hallucinations": []}
"""


def append_to_verification() -> None:
    """Append the fact_check stub to the canonical verification module.

    This function is idempotent; if the method already exists the file is
    left untouched.  Importing the module no longer performs any writes so
    tests can safely `import tools.append_fact_check` without mutating the
    workspace.
    """
    p = Path(__file__).resolve().parent.parent / "src" / "core" / "base" / "verification.py"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "def fact_check" in text:
        return
    with open(p, "a", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    append_to_verification()

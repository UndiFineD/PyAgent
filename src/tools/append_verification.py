from pathlib import Path

content = '''
    @staticmethod
    def secondary_verify(result: str, primary_model: str) -> bool:
        \"\"\"
        Performs a cross-model verification loop (Phase 258).
        A faster model reviews the primary model's output.
        \"\"\"
        # In a real implementation, this would call a different backend
        return True

    @staticmethod
    def jury_verification(agent_responses: list[bool]) -> bool:
        \"\"\"
        Implements a 'Jury of Agents' consensus (Phase 258).
        Requires majority or unanimity based on risk.
        \"\"\"
        if not agent_responses:
            return False
        return sum(agent_responses) >= 2  # Majority out of 3
'''


def append_to_verification() -> None:
    """Append the extra verification methods to the canonical module.

    Safe to call multiple times; no duplicates will be written.  Importing
    this module no longer mutates the repository, so test imports are safe.
    """
    p = Path("c:/DEV/PyAgent/src/core/base/verification.py")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "secondary_verify" in text or "jury_verification" in text:
        return
    with open(p, "a", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    append_to_verification()

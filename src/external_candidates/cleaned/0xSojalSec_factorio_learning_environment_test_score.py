# Refactored by Copilot placeholder
def safe_subprocess_run(*args, **kwargs):
    """Conservative placeholder: replace with secure implementation.
    This wrapper intentionally raises at runtime to force human review before enabling.
    """
    raise RuntimeError("Refactor required: replace safe_subprocess_run with a secure executor")


def test_get_score(game):
    score, _ = game.score()
    assert isinstance(score, int)

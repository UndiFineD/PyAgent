# Repository Maintenance Reminders (20260115-1513)

## 🛠️ Pending Manual Actions
- [ ] **Review Merge**: Examine the current restore branch and merge into `main` if satisfied.
- [ ] **AI Integration**: Set `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT` to enable autonomous fixing.
- [ ] **Log Cleanup**: The `fixes/` directory can grow large; periodically delete old run folders.

## 💡 Suggested Improvements
- [x] **Tool Specificity**: Updated `Ruff`, `Mypy`, and `Flake8` to only scan changed `.py` files.
- [ ] **Rollback Strategy**: Implement `GitManager.hard_rollback()` call in `agents.py` if an AI-applied fix breaks the build.
- [ ] **Pre-commit Hook**: Integrate the `orchestrator` as a heavy-duty pre-push check.

## 📊 Latest Orchestrator Notes
Refer to the newest folder in `fixes/` for detailed breakdown of issues found by tools.

# flm-tps-benchmark

**Project ID:** `prj0000046`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Zero TypeScript errors in `CodeBuilder.tsx` and `vite.config.ts`
- [x] Agent Doc tab displays rendered Markdown (not a download prompt)
- [x] Docs loaded from actual `.github/agents/*.agent.md` files
- [x] Edit/Preview toggle works; edits auto-saved to disk
- [x] Backend doc endpoints added and validated (no Python linter errors)
- [x] `start.ps1 start` auto-kills stale port holders
- [x] `.pyagent.pids` added to `.gitignore`

## Status

7 of 7 tasks completed

## Code detection

- Code detected in:
  - `scripts\FlmTpsBenchmark.py`
  - `src\core\memory\BenchmarkRunner.py`
  - `src\core\providers\FlmChatAdapter.py`
  - `src\core\providers\FlmModelProbe.py`
  - `src\core\providers\FlmProviderConfig.py`
  - `tests\test_BenchmarkRunner.py`
  - `tests\test_benchmarks.py`
  - `tests\test_core_providers_FlmChatAdapter.py`
  - `tests\test_core_providers_FlmModelProbe.py`
  - `tests\test_core_providers_FlmProviderConfig.py`
  - `tests\test_flm_chat_adapter.py`
  - `tests\test_flm_dashboard.py`
  - `tests\test_flm_provider_config.py`
  - `tests\test_flm_provider_docs.py`
  - `tests\test_flm_runtime_errors.py`
  - `tests\test_flm_tool_loop.py`
  - `tests\test_providers_flm.py`
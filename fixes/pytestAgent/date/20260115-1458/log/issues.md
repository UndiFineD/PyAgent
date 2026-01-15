## Issues found by pytestAgent at 20260115-1504

```
============================= test session starts =============================
platform win32 -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\DEV\PyAgent
configfile: pytest.ini
plugins: anyio-4.12.1, hypothesis-6.150.1, asyncio-1.3.0, cov-7.0.0, xdist-3.8.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 1456 items

tests\adversarial\test_red_queen.py .                                    [  0%]
tests\community\test_community_architecture.py .                         [  0%]
tests\community\test_community_demo.py .                                 [  0%]
tests\community\test_community_orchestrator.py .                         [  0%]
tests\community\test_resilience_community.py .                           [  0%]
tests\integration\test_agent_integration.py ..                           [  0%]
tests\integration\test_agent_logic_integration.py ......                 [  0%]
tests\integration\test_backend_integration.py ..............             [  1%]
tests\integration\test_coder_logic_integration.py ..........             [  2%]
tests\integration\test_context_integration.py ......                     [  2%]
tests\integration\test_formula_integration.py ..........                 [  3%]
tests\integration\test_gui_integration.py ....                           [  3%]
tests\integration\test_gui_modular.py .....                              [  4%]
tests\integration\test_interaction_pipeline.py .                         [  4%]
tests\integration\test_webhooks_integration.py .                         [  4%]
tests\performance\test_agent_PERFORMANCE.py .                            [  4%]
tests\performance\test_base_agent_PERFORMANCE.py ...                     [  4%]
tests\performance\test_coder_PERFORMANCE.py .                            [  4%]
tests\performance\test_dedup_benchmark.py .                              [  4%]
tests\performance\test_economy_benchmark.py .                            [  4%]
tests\phases\test_phase123_decentralization.py ......                    [  5%]
tests\phases\test_phase123_discovery.py ..                               [  5%]
tests\phases\test_phase123_final_realization.py .....                    [  5%]
tests\phases\test_phase130.py ....                                       [  6%]
tests\phases\test_phase19.py .                                           [  6%]
tests\phases\test_phase21.py .                                           [  6%]
tests\phases\test_phase22.py .                                           [  6%]
tests\phases\test_phase23.py .                                           [  6%]
tests\phases\test_phase24.py .                                           [  6%]
tests\phases\test_phase25.py .                                           [  6%]
tests\phases\test_phase26.py .                                           [  6%]
tests\phases\test_phase27.py .                                           [  6%]
tests\phases\test_phase33.py .                                           [  6%]
tests\phases\test_phase34.py .                                           [  6%]
tests\phases\test_phase35.py .                                           [  6%]
tests\phases\test_phase36.py .                                           [  6%]
tests\phases\test_phase37.py .                                           [  6%]
tests\phases\test_phase38.py .                                           [  7%]
tests\phases\test_phase39.py .                                           [  7%]
tests\phases\test_phase40.py ...                                         [  7%]
tests\phases\test_phase41.py ...                                         [  7%]
tests\phases\test_phase42.py ...                                         [  7%]
tests\phases\test_phase43.py ...                                         [  7%]
tests\phases\test_phase44.py ..                                          [  8%]
tests\phases\test_phase45.py ..                                          [  8%]
tests\phases\test_phase46.py ..                                          [  8%]
tests\phases\test_phase50.py .                                           [  8%]
tests\phases\test_phase51.py .                                           [  8%]
tests\phases\test_phase52.py .                                           [  8%]
tests\phases\test_phase71.py ..                                          [  8%]
tests\phases\test_phase72.py .                                           [  8%]
tests\phases\test_phase73.py .                                           [  8%]
tests\phases\test_phase74.py .                                           [  8%]
tests\phases\test_phase75.py .                                           [  8%]
tests\phases\test_phase76.py .                                           [  8%]
tests\phases\test_phase77.py .                                           [  9%]
tests\phases\test_phase78.py .                                           [  9%]
tests\phases\test_phase79.py .                                           [  9%]
tests\phases\test_phase80.py .                                           [  9%]
tests\phases\test_phase81.py ..                                          [  9%]
tests\phases\test_phase82.py .                                           [  9%]
tests\phases\test_phase83.py ...                                         [  9%]
tests\phases\test_phase84.py ..                                          [  9%]
tests\phases\test_phase85.py ..                                          [  9%]
tests\phases\test_phase86.py ..                                          [ 10%]
tests\phases\test_phase87.py FF.                                         [ 10%]
tests\phases\test_phase88.py ..                                          [ 10%]
tests\phases\test_phase89.py .                                           [ 10%]
tests\phases\test_phase90.py ..                                          [ 10%]
tests\phases\test_phase91.py ...                                         [ 10%]
tests\phases\test_phase92.py ..                                          [ 10%]
tests\phases\test_phase93.py ...                                         [ 11%]
tests\phases\test_phase94.py ..                                          [ 11%]
tests\phases\test_phase95.py ...                                         [ 11%]
tests\phases\test_phase96.py ..                                          [ 11%]
tests\phases\test_phases47_49.py ...                                     [ 11%]
tests\phases\test_phases53_55.py ...                                     [ 12%]
tests\phases\test_phases56_58.py ...                                     [ 12%]
tests\phases\test_phases59_61.py ...                                     [ 12%]
tests\phases\test_phases62_64.py ...                                     [ 12%]
tests\phases\test_phases65_67.py ...                                     [ 12%]
tests\phases\test_phases68_70.py ...                                     [ 13%]
tests\specialists\test_asynciothreadingcoderagent_UNIT.py .              [ 13%]
tests\specialists\test_phase122_specialists.py ....                      [ 13%]
tests\specialists\test_specialists.py ..                                 [ 13%]
tests\unit\core\test_AgentCommandHandler_UNIT.py ....                    [ 13%]
tests\unit\core\test_base_agent_CORE_UNIT.py ........................... [ 15%]
.......                                                                  [ 16%]
tests\unit\core\test_base_agent_LEGACY.py .............................. [ 18%]
..                                                                       [ 18%]
tests\unit\core\test_base_agent_UNIT.py .....                            [ 18%]
tests\unit\core\test_context_CORE_UNIT.py .............................. [ 20%]
..........................................                               [ 23%]
tests\unit\core\test_context_LEGACY.py .                                 [ 23%]
tests\unit\core\test_context_UNIT.py .....................               [ 25%]
tests\unit\core\test_knowledge_graph.py .                                [ 25%]
tests\unit\core\test_semantic.py ..                                      [ 25%]
tests\unit\infrastructure\test_backend_CORE_UNIT.py .................... [ 26%]
.......................................                                  [ 29%]
tests\unit\infrastructure\test_backend_LEGACY.py ......................  [ 30%]
tests\unit\infrastructure\test_backend_UNIT.py ......................... [ 32%]
..........                                                               [ 33%]
tests\unit\infrastructure\test_gossip_UNIT.py ..                         [ 33%]
tests\unit\infrastructure\test_models_propagation.py .                   [ 33%]
tests\unit\infrastructure\test_ollama_access.py .                        [ 33%]
tests\unit\infrastructure\test_orchestrator_resilience.py .              [ 33%]
tests\unit\infrastructure\test_plugins.py ..                             [ 33%]
tests\unit\infrastructure\test_resilience.py .                           [ 33%]
tests\unit\infrastructure\test_sdk_v2_2.py .                             [ 33%]
tests\unit\infrastructure\test_strategies.py ...                         [ 34%]
tests\unit\logic\test_agent_ADVANCED_UNIT.py ..........................s [ 36%]
s...s..sssss.s....s...                                                   [ 37%]
tests\unit\logic\test_agent_CORE_UNIT.py ............................... [ 39%]
........................................                                 [ 42%]
tests\unit\logic\test_agent_LEGACY.py ........................           [ 44%]
tests\unit\logic\test_agent_UNIT.py .................................... [ 46%]
.....                                                                    [ 46%]
tests\unit\logic\test_coder_CORE_UNIT.py ............................... [ 49%]
.................................                                        [ 51%]
tests\unit\logic\test_coder_LEGACY.py .                                  [ 51%]
tests\unit\logic\test_coder_UNIT.py .........................            [ 53%]
tests\unit\logic\test_new_agents_UNIT.py ..                              [ 53%]
tests\unit\observability\test_reports_CORE.py .......................... [ 55%]
...........                                                              [ 55%]
tests\unit\observability\test_reports_INTEGRATION.py ................    [ 56%]
tests\unit\observability\test_reports_LEGACY.py .                        [ 56%]
tests\unit\observability\test_reports_PERFORMANCE.py ...                 [ 57%]
tests\unit\observability\test_reports_SHELL.py ......................... [ 58%]
...............................................................          [ 63%]
tests\unit\observability\test_reports_UNIT.py ................           [ 64%]
tests\unit\observability\test_stats_CORE.py ...................          [ 65%]
tests\unit\observability\test_stats_INTEGRATION.py ...                   [ 65%]
tests\unit\observability\test_stats_LEGACY.py .                          [ 65%]
tests\unit\observability\test_stats_PERFORMANCE.py .......               [ 66%]
tests\unit\observability\test_stats_SHELL.py .......................s... [ 68%]
........................................................................ [ 73%]
.................                                                        [ 74%]
tests\unit\observability\test_stats_UNIT.py ............................ [ 76%]
................................                                         [ 78%]
tests\unit\test_agent_filters.py .                                       [ 78%]
tests\unit\test_auction_core.py ..                                       [ 78%]
tests\unit\test_auth_core.py .....                                       [ 78%]
tests\unit\test_autonomy_core.py ...                                     [ 79%]
tests\unit\test_base_agent_core.py ................................      [ 81%]
tests\unit\test_benchmark_core.py ....................                   [ 82%]
tests\unit\test_byzantine_core.py ....                                   [ 83%]
tests\unit\test_convergence_core.py ..                                   [ 83%]
tests\unit\test_error_mapping_core.py .....................              [ 84%]
tests\unit\test_formula_engine_core.py ....                              [ 84%]
tests\unit\test_identity_core.py .....                                   [ 85%]
tests\unit\test_metrics_core.py ...........                              [ 85%]
tests\unit\test_model_fallback_core.py ....                              [ 86%]
tests\unit\test_privacy_core.py ...                                      [ 86%]
tests\unit\test_profiling_core.py ...                                    [ 86%]
tests\unit\test_pruning_core.py ....                                     [ 86%]
tests\unit\test_resilience_core.py ...                                   [ 87%]
tests\unit\test_rust_core_parity.py .....                                [ 87%]
tests\unit\test_stability_core.py ......                                 [ 87%]
tests\unit\test_tracing_core.py ....                                     [ 88%]
tests\unit\test_utils\test_test_utils_COMPREHENSIVE_UNIT.py ............ [ 89%]
..........................                                               [ 90%]
tests\unit\test_utils\test_test_utils_CORE_UNIT.py ..................... [ 92%]
..............................................................           [ 96%]
tests\unit\test_utils\test_test_utils_INTEGRATION.py ......              [ 96%]
tests\unit\test_utils\test_test_utils_LEGACY.py .                        [ 96%]
tests\unit\test_utils\test_test_utils_PERFORMANCE.py .......             [ 97%]
tests\unit\test_utils\test_test_utils_UNIT.py .......................... [ 99%]
..........                                                               [ 99%]
tests\unit\test_version_gate.py .                                        [100%]

================================== FAILURES ===================================
____________________ TestCodeQuality.test_aggregate_score _____________________

self = <test_phase87.TestCodeQuality testMethod=test_aggregate_score>

    def test_aggregate_score(self) -> None:
        self.agent.analyze_file_quality(self.py_file)
        score = self.agent.get_aggregate_score()
>       self.assertTrue(score < 100)
E       AssertionError: False is not true

tests\phases\test_phase87.py:80: AssertionError
---------------------------- Captured stdout call -----------------------------
Code Quality: Analyzing test_quality.py
_____________________ TestCodeQuality.test_python_quality _____________________

self = <test_phase87.TestCodeQuality testMethod=test_python_quality>

    def test_python_quality(self) -> None:
        report = self.agent.analyze_file_quality(self.py_file)
        self.assertEqual(report['file'], self.py_file)
>       self.assertTrue(any("too long" in i['message'] for i in report['issues']))
E       AssertionError: False is not true

tests\phases\test_phase87.py:39: AssertionError
---------------------------- Captured stdout call -----------------------------
Code Quality: Analyzing test_quality.py
============================== warnings summary ===============================
tests/integration/test_formula_integration.py: 15 warnings
tests/unit/observability/test_stats_SHELL.py: 2 warnings
tests/unit/test_formula_engine_core.py: 168 warnings
  C:\DEV\PyAgent\src\observability\stats\metrics_engine.py:700: DeprecationWarning: ast.Num is deprecated and will be removed in Python 3.14; use ast.Constant instead
    elif hasattr(ast, "Num") and isinstance(node, ast.Num):

tests/unit/observability/test_stats_SHELL.py::TestDerivedMetricCalculator::test_calculate
tests/unit/observability/test_stats_SHELL.py::TestDerivedMetricCalculator::test_get_all_derived
  C:\DEV\PyAgent\src\observability\stats\metrics_engine.py:307: DeprecationWarning: ast.Num is deprecated and will be removed in Python 3.14; use ast.Constant instead
    elif isinstance(node, ast.Num):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
FAILED tests/phases/test_phase87.py::TestCodeQuality::test_aggregate_score - ...
FAILED tests/phases/test_phase87.py::TestCodeQuality::test_python_quality - A...
==== 2 failed, 1443 passed, 11 skipped, 187 warnings in 329.76s (0:05:29) =====

```

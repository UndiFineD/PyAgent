
import pytest
from hypothesis import given, strategies as st
from src.core.base.core.ConvergenceCore import ConvergenceCore




class TestConvergenceCore:
    @pytest.fixture
    def convergence_core(self):
        return ConvergenceCore(workspace_root="/tmp/workspace")

    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.booleans(), max_size=20))
    def test_verify_fleet_health_hypothesis(self, agent_reports):
        convergence_core = ConvergenceCore(workspace_root="/tmp/workspace")
        result = convergence_core.verify_fleet_health(agent_reports)

        expected_healthy = sum(1 for status in agent_reports.values() if status)
        expected_total = len(agent_reports)
        expected_passed = expected_healthy == expected_total if expected_total > 0 else False
        expected_failed = [name for name, status in agent_reports.items() if not status]

        assert result['all_passed'] == expected_passed
        assert result['healthy_count'] == expected_healthy
        assert result['total_count'] == expected_total
        assert set(result['failed_agents']) == set(expected_failed)

    def test_generate_strategic_summary(self, convergence_core):
        # Pass dummy history as it seems unused in current logic
        summary = convergence_core.generate_strategic_summary([])
        assert "SWARM STRATEGIC SUMMARY" in summary
        assert "PROXIMA EVOLUTION" in summary

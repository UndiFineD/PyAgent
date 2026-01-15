
from hypothesis import given, strategies as st, settings, HealthCheck
from src.logic.agents.security.core.ByzantineCore import ByzantineCore




class TestByzantineCore:
    def setup_method(self):
        self.core = ByzantineCore()

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=50)
    @given(st.lists(
        st.fixed_dictionaries({
            'weight': st.floats(min_value=0.1, max_value=1.0),
            'hash': st.sampled_from(["a", "b", "c"])
        }), min_size=0, max_size=20))
    def test_calculate_agreement_score(self, votes):
        score = self.core.calculate_agreement_score(votes)
        import math
        assert 0.0 <= score <= 1.0 or math.isclose(score, 1.0)
        if not votes:
            assert score == 0.0
        else:
            # Manual verification
            total = sum(v['weight'] for v in votes)
            counts = {}
            for v in votes:
                counts[v['hash']] = counts.get(v['hash'], 0.0) + v['weight']
            max_c = max(counts.values()) if counts else 0
            expected = max_c / total if total > 0 else 0
            assert abs(score - expected) < 1e-9

    @given(st.dictionaries(st.text(), st.floats(0.0, 1.0), min_size=0, max_size=20), st.integers(1, 10))
    def test_select_committee(self, ratings, min_size):
        committee = self.core.select_committee(ratings, min_size=min_size)
        assert isinstance(committee, list)
        if len(ratings) > 0:
            assert len(committee) <= len(ratings)
        # If we have enough good agents, size should be >= min_size (if available)

    def test_get_required_quorum(self):
        assert self.core.get_required_quorum("infrastructure") == 0.8
        assert self.core.get_required_quorum("documentation") == 0.5
        assert self.core.get_required_quorum("other") == 0.67

    def test_detect_deviating_hashes(self):
        votes = [
            {'id': '1', 'hash': 'a'},
            {'id': '2', 'hash': 'b'},
            {'id': '3', 'hash': 'a'}
        ]
        deviants = self.core.detect_deviating_hashes(votes, 'a')
        assert deviants == ['2']
        deviants = self.core.detect_deviating_hashes(votes, 'b')
        assert set(deviants) == {'1', '3'}

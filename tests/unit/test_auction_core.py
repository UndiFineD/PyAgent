from hypothesis import given, strategies as st, settings, HealthCheck
from src.logic.agents.swarm.core.AuctionCore import AuctionCore


class TestAuctionCore:
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=50)
    @given(
        st.lists(
            st.fixed_dictionaries(
                {
                    "agent_id": st.text(min_size=1, max_size=5),
                    "amount": st.floats(min_value=0.0, max_value=1e6),
                }
            ),
            min_size=0,
            max_size=10,
        ),
        st.integers(min_value=1, max_value=5),
    )
    def test_calculate_vcg_auction_hypothesis(self, bids, slots):
        # Python implementation logic check
        winners = AuctionCore.calculate_vcg_auction([b.copy() for b in bids], slots)

        # Invariants
        assert len(winners) <= len(bids)
        assert len(winners) <= slots

        # Check sorting
        amounts = [w["amount"] for w in winners]
        assert amounts == sorted(amounts, reverse=True)

        # Check clearing price
        if winners:
            if len(bids) > slots:
                expected_price = sorted([b["amount"] for b in bids], reverse=True)[
                    slots
                ]
            else:
                expected_price = 0.0

            for w in winners:
                assert w["price_paid"] == expected_price

    @given(
        st.floats(min_value=0.0, max_value=1e5),
        st.floats(min_value=1.0, max_value=1e5),
        st.floats(min_value=0.0, max_value=1.0),
    )
    def test_enforce_vram_quota(self, request, total, quota):
        result = AuctionCore.enforce_vram_quota(request, total, quota)
        expected = request <= (total * quota)
        assert result == expected

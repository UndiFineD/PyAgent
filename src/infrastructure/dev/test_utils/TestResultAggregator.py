class TestResultAggregator:
    def aggregate(self, results):
        return {"total": len(results)}


__all__ = ["TestResultAggregator"]

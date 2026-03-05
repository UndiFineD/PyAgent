class TestReportGenerator:
    def generate(self, results):
        return {"summary": len(results)}


__all__ = ["TestReportGenerator"]

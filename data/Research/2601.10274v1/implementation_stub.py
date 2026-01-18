class LoadAwareReasoningScheduler:
    """
    Dynamically adjusts reasoning token budget based on queue pressure (arXiv:2601.10274).
    """
    def __init__(self, target_latency_ms: float = 2000):
        self.target_latency = target_latency_ms

    def calculate_budget(self, queue_length: int, avg_latency: float) -> int:
        """
        Calculates the maximum allowed reasoning tokens.
        """
        if queue_length > 50: # High pressure
            return 128 # Minimal "thinking"
        elif queue_length < 5: # Idle
            return 2048 # Maximum reasoning depth
        
        # Adaptive scaling logic
        pressure_factor = 1.0 - (queue_length / 50.0)
        return int(2048 * pressure_factor)

if __name__ == "__main__":
    scheduler = LoadAwareReasoningScheduler()
    print(f"High Load Budget: {scheduler.calculate_budget(60, 5000)}")
    print(f"Med Load Budget: {scheduler.calculate_budget(25, 2000)}")
    print(f"Low Load Budget: {scheduler.calculate_budget(2, 500)}")

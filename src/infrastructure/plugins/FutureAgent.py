
"""Plugin demonstrating forward-compatibility testing for the SDK."""

SDK_REQUIRED = "10.0.0"

class FutureAgent:
    def __init__(self, *args) -> None:
        pass
    
    def execute(self, task) -> str:
        return "I am from the future!"

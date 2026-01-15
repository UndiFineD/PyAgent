from dataclasses import dataclass




@dataclass
class ValidationRule:
    name: str
    pattern: str
    message: str
    severity: str

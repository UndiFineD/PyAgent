
from __future__ import annotations
from typing import List
import random

class SynthesisCore:
    """
    SynthesisCore handles synthetic data generation for fine-tuning.
    It also implements the Feature Store logic for vectorized insights.
    """

    def __init__(self) -> None:
        # Edge-case templates for Python snippets
        self.edge_case_templates = [
            "def {name}(*args, **kwargs): return args[0] if args else kwargs.get('default')",
            "async with {context} as c: yield await c.exec(f'{{a}} + {{b}}')",
            "lambda x: [i for i in x if i is not None and not isinstance(i, (int, float))]",
            "class {name}(metaclass=Singleton): pass"
        ]

    def generate_python_edge_cases(self, count: int) -> List[str]:
        """Generates synthetic Python snippets based on templates."""
        results = []
        for i in range(count):
            tpl = random.choice(self.edge_case_templates)
            results.append(tpl.format(name=f"func_{i}", context=f"ctx_{i}"))
        return results

    def vectorize_insight(self, insight: str) -> List[float]:
        """
        Simulated vectorization of a text insight.
        Returns a mock embedding vector.
        """
        # In a real scenario, this would call a local embedding model
        # Use a deterministic mock based on text length and first char
        seed = len(insight) + (ord(insight[0]) if insight else 0)
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(128)]

    def merge_feature_vectors(self, vectors: List[List[float]]) -> List[float]:
        """Averages multiple feature vectors into a single swarm insight."""
        if not vectors:
            return [0.0] * 128
        
        dim = len(vectors[0])
        total = [0.0] * dim
        for v in vectors:
            for i in range(dim):
                total[i] += v[i]
                
        return [x / len(vectors) for x in total]
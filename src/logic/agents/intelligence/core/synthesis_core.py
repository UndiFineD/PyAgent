"""
SynthesisCore handles synthetic data generation for fine-tuning.
It also implements the Feature Store logic for vectorized insights.
"""

from __future__ import annotations
import random
import logging

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class SynthesisCore:
    """
    SynthesisCore handles synthetic data generation for fine-tuning.
    It also implements the Feature Store logic for vectorized insights.
    """

    _transformer_cache: Any = None
    _rust_failed: bool = False

    def __init__(self) -> None:
        # Edge-case templates for Python snippets
        self.edge_case_templates = [
            "def {name}(*args, **kwargs): return args[0] if args else kwargs.get('default')",
            "async with {context} as c: yield await c.exec(f'{{a}} + {{b}}')",
            "lambda x: [i for i in x if i is not None and not isinstance(i, (int, float))]",
            "class {name}(metaclass=Singleton): pass",
        ]

    def _get_transformer(self) -> Any:
        """Lazily initializes and caches the Rust transformer."""
        if not HAS_RUST or SynthesisCore._rust_failed:
            return None
        
        if SynthesisCore._transformer_cache is None:
            try:
                # Use a hardware profile to auto-configure to available resources
                profile = rust_core.HardwareProfile(None)
                config = rust_core.TransformerConfig.auto_configure(profile)
                
                # We can't easily modify the config as attributes are read-only in this Rust build.
                # However, the auto-configure logic already scales based on system memory.
                # Caching it here ensures we only pay the initialization cost once.
                
                SynthesisCore._transformer_cache = rust_core.NeuralTransformer(config)
                logging.info(f"SynthesisCore: Initialized Rust transformer.")
            except Exception as e:
                logging.warning(f"SynthesisCore: Failed to initialize Rust transformer: {e}")
                SynthesisCore._rust_failed = True
        
        return SynthesisCore._transformer_cache

    def generate_python_edge_cases(self, count: int) -> list[str]:
        """Generates synthetic Python snippets based on templates."""
        if HAS_RUST:
            try:
                res, stats = rust_core.generate_synthetic_snippets_with_stats(count)
                print(f"[SynthesisCore] Generated {stats.token_count} tokens in {stats.duration_ms:.2f}ms ({stats.tps:.2f} tokens/s)")
                print(f"[SynthesisCore] Hardware Savings: ${stats.cost_usd:.6f} (@ 0.0005 cent/token)")
                
                # Optional: persistent tracking via FleetEconomy
                try:
                    from src.logic.agents.swarm.fleet_economy_agent import FleetEconomyAgent
                    fea = FleetEconomyAgent()
                    fea.log_hardware_savings("SynthesisCore/Generation", stats.token_count, stats.tps, stats.cost_usd)
                except ImportError:
                    pass
                
                return res
            except Exception as e:
                logging.debug(f"SynthesisCore: Rust generation failed: {e}")

        results = []
        for i in range(count):
            tpl = random.choice(self.edge_case_templates)
            results.append(tpl.format(name=f"func_{i}", context=f"ctx_{i}"))
        return results

    def vectorize_insight(self, insight: str) -> list[float]:
        """
        Simulated vectorization of a text insight.
        Returns a mock embedding vector.
        """
        transformer = self._get_transformer()
        if transformer:
            try:
                vec, stats = transformer.vectorize_with_stats(insight)
                # We typically only log if it's a large insight or for performance tracking
                if len(insight) > 100:
                    print(f"[SynthesisCore] Vectorized {stats.token_count} tokens at {stats.tps:.2f} t/s")
                    print(f"[SynthesisCore] Hardware Savings: ${stats.cost_usd:.6f}")
                    
                    try:
                        from src.logic.agents.swarm.fleet_economy_agent import FleetEconomyAgent
                        fea = FleetEconomyAgent()
                        fea.log_hardware_savings("SynthesisCore/Vectorization", stats.token_count, stats.tps, stats.cost_usd)
                    except ImportError:
                        pass
                
                return vec
            except Exception as e:
                logging.debug(f"SynthesisCore: Rust vectorization failed: {e}")

        # In a real scenario, this would call a local embedding model
        # Use a deterministic mock based on text length and first char
        seed = len(insight) + (ord(insight[0]) if insight else 0)
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(128)]

    def merge_feature_vectors(self, vectors: list[list[float]]) -> list[float]:
        """Averages multiple feature vectors into a single swarm insight."""
        if HAS_RUST:
            try:
                return rust_core.average_feature_vectors(vectors)  # type: ignore[attr-defined]
            except Exception:
                pass

        if not vectors:
            return [0.0] * 128

        dim = len(vectors[0])
        total = [0.0] * dim
        for v in vectors:
            for i in range(dim):
                total[i] += v[i]

        return [x / len(vectors) for x in total]

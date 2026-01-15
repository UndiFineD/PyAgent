
from __future__ import annotations
from typing import Any

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False




class SearchMeshCore:
    """
    SearchMeshCore implements federated search result aggregation and ranking.
    It synthesizes results from multiple providers (Google, Bing, Perplexity, Tavily).
    """

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        # Default relevance weights for different providers
        self.weights = weights or {
            "google": 1.2,
            "bing": 0.8,
            "perplexity": 1.5,
            "tavily": 1.3,
            "generic": 1.0
        }

    def aggregate_results(self, raw_results: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
        """
        Takes raw results from multiple providers and merges them into a ranked list.
        Each result should have: 'title', 'url', 'snippet', 'score' (optional).
        """
        if HAS_RUST:
            try:
                return rust_core.aggregate_search_results(raw_results, self.weights)  # type: ignore[attr-defined]
            except Exception:
                pass

        master_list: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        # Step 1: Flatten and apply weights
        for provider, results in raw_results.items():
            weight = self.weights.get(provider.lower(), self.weights["generic"])
            for res in results:
                url = res.get("url", "")
                if not url:
                    continue

                # Basic score calculation
                base_score = res.get("score", 0.5)
                weighted_score = base_score * weight

                if url in seen_urls:
                    # If duplicate, boost the existing entry
                    for item in master_list:
                        if item["url"] == url:
                            item["total_score"] += weighted_score
                            item["providers"].append(provider)
                            break
                    continue

                seen_urls.add(url)
                master_list.append({
                    "title": res.get("title", "No Title"),
                    "url": url,
                    "snippet": res.get("snippet", ""),
                    "providers": [provider],
                    "total_score": weighted_score
                })

        # Step 2: Sort by total score
        master_list.sort(key=lambda x: x["total_score"], reverse=True)
        return master_list

    def filter_redundant(self, results: list[dict[str, Any]], remembered_urls: set[str]) -> list[dict[str, Any]]:
        """
        Filters out results that have already been seen in previous search research sessions (MemoRAG integration).
        """
        return [res for res in results if res["url"] not in remembered_urls]

    async def parallel_search_placeholder(self, providers: list[str], query: str) -> dict[str, list[dict[str, Any]]]:
        """
        Generic structure for the Mesh agent to invoke search providers in parallel.
        (The Shell agent will provide the actual API implementation callbacks).
        """
        # This logic stays in the shell, but the core defines the expected structure.
        return {}

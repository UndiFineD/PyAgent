import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class LocalContextRecorder:
    """
    Records LLM prompts and results for future training/fine-tuning.
    Stores data in JSONL format with monthly and hash-based sharding.
    Optimized for trillion-parameter data harvesting (Phase 105).
    """

    def __init__(self, workspace_root: Path) -> None:
        self.log_dir = workspace_root / "logs" / "external_ai_learning"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # Phase 105: Monthly + Hash-based Sharding (Deeper distribution for trillion-param scale)
        self.shard_count = 256
        self.current_month = datetime.now().strftime('%Y%m')
        self.use_compression = True # Save 70-80% space for massive datasets

    def record_interaction(self, provider: str, model: str, prompt: str, result: str, meta: Dict[str, Any] = None) -> None:
        """
        Appends a new interaction record.
        Includes unique context hashing for future deduplication and sharded storage.
        Optimized for high-throughput and low-latency disk writes.
        """
        import hashlib
        import zlib
        import gzip
        
        # Stability: generate a stable hash for the prompt to allow O(1) deduplication
        prompt_hash = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        
        # Determine sub-shard for massively parallel access (256 virtual buckets)
        shard_id = zlib.adler32(prompt_hash.encode()) % self.shard_count
        
        # Use .jsonl.gz if compression is enabled
        ext = ".jsonl.gz" if self.use_compression else ".jsonl"
        log_file = self.log_dir / f"shard_{self.current_month}_{shard_id:03d}{ext}"
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "prompt_hash": prompt_hash,
            "prompt": prompt,
            "result": result,
            "meta": meta or {}
        }
        
        line = (json.dumps(record) + "\n").encode('utf-8')
        
        try:
            if self.use_compression:
                with gzip.open(log_file, "ab") as f:
                    f.write(line)
            else:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")
                    
            # Update a centralized index for fast semantic lookup in the future (Phase 106)
            self._update_index(prompt_hash, str(log_file.name))
            
        except Exception as e:
            logging.error(f"Failed to record interaction to shard {shard_id}: {e}")

    def _update_index(self, prompt_hash: str, filename: str) -> None:
        """Simple index updates to avoid scanning all shards for a specific query."""
        import os
        index_file = self.log_dir / "shards_lookup.index"
        try:
            # Atomic append for the index
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(f"{prompt_hash}:{filename}\n")
        except Exception:
            pass


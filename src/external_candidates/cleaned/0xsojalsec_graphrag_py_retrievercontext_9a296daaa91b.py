# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\schema.py\retrievercontext_9a296daaa91b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Schema\RetrieverContext.py

from dataclasses import asdict, dataclass, field


@dataclass
class RetrieverContext:
    context: dict = field(default_factory=dict)

    def register_context(self, key, value):
        self.context[key] = value

    @property
    def as_dict(self):
        return self.context

    @property
    def config(self):
        return self.context["config"]

    @property
    def llm(self):
        return self.context["llm"]

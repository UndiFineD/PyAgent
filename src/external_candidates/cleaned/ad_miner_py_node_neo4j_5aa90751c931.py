# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ad_miner.py\ad_miner.py\sources.py\modules.py\node_neo4j_5aa90751c931.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AD_Miner\ad_miner\sources\modules\node_neo4j.py


class Node:
    # TODO PARSE LABELS HERE

    def __init__(self, id, labels, name, domain, relation_type):

        self.id = id

        self.labels = labels

        self.name = name

        self.domain = domain

        self.relation_type = relation_type

    # Needed to use set() on a list of nodes (to remove duplicates from lists)

    def __hash__(self):

        return hash(self.id)

    def __eq__(self, other):

        if not isinstance(other, Node):
            return NotImplemented

        ret = (
            (self.id == other.id)
            and (self.labels == other.labels)
            and (self.name == other.name)
            and (self.domain == other.domain)
            and (self.relation_type == other.relation_type)
        )

        return ret

#!/usr/bin/env python3


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict


class GraphIntelligence:
    """Intelligence module for Graph-based security analysis and AD relationships.
    Ported from FalconHound & FalkorDB.
    """

    @staticmethod
    def get_ad_graph_queries() -> Dict[str, str]:
        """Cypher queries for Active Directory graph analysis."""
        return {
            "unroll_group_members": ("MATCH (g:Group)-[:MemberOf*0..]->(u:User) RETURN g.name, u.name"),
            "shortest_path_to_da": (
                "MATCH (u:User {name: '{username}'}), (da:Group {name: 'DOMAIN ADMINS'}), "
                "p = shortestPath((u)-[*..]->(da)) "
                "RETURN p"
            ),
            "kerberoastable_admins": (
                "MATCH (u:User {hasspn: true})-[:MemberOf*0..]->(g:Group) WHERE g.name CONTAINS 'ADMIN' RETURN u.name"
            ),
            "constrained_delegation_path": ("MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name, c.name"),
            "dangerous_acl_rights": (
                "MATCH (u:User)-[r:WriteDacl|WriteOwner|AllExtendedRights]->(target) "
                "RETURN u.name, type(r), target.name"
            ),
        }

    @staticmethod
    def get_graph_performance_primitives() -> Dict[str, str]:
        """Techniques for high-performance graph querying (Ported from FalkorDB)."""
        return {
            "sparse_matrix_adjacency": (
                "Representing graph relationships as sparse matrices for linear algebra operations"
            ),
            "linear_algebra_query_exec": "Using vector-matrix multiplication for BFS/DFS traversal",
            "multi_tenant_isolation": "Namespace-based graph separation in memory",
            "opencypher_extension_indices": "Using specialized indices for property-based filtering in Cypher",
        }

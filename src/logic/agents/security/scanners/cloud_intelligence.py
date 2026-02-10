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

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional


class CloudIntelligence:
    """
    Handles discovery and auditing of cloud assets (S3, Azure Blobs, GCP Buckets).
    Ported logic from s3crets_scanner and other cloud-focused tools.
    """

    # Common patterns for cloud bucket discovery
    BUCKET_PATTERNS = [
        r"{target}.s3.amazonaws.com",
        r"{target}.s3-external-1.amazonaws.com",
        r"{target}.s3.dualstack.{region}.amazonaws.com",
        r"s3.amazonaws.com/{target}",
        r"{target}.storage.googleapis.com",
        r"{target}.blob.core.windows.net",
        r"{target}.azureedge.net",
        r"{target}.digitaloceanspaces.com",
    ]

    S3_SEARCH_PATTERNS = [
        r".*\.bak$",
        r".*\.sql$",
        r".*\.env$",
        r".*\.config$",
        r"credentials",
        r"secret",
        r"password",
        r"key",
        r".*\.p12$",
        r".*\.pfx$",
        r".*\.pem$",
        r"database",
        r"backup",
        r"dump",
    ]

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers={"User-Agent": "PyAgent CloudAudit/1.0"})
        return self.session

    async def check_bucket_accessibility(self, bucket_url: str) -> Dict[str, Any]:
        """Checks if a cloud bucket is public, private, or non-existent."""
        session = await self.get_session()
        try:
            async with session.get(bucket_url, timeout=5) as resp:
                if resp.status == 200:
                    return {"url": bucket_url, "status": "public"}
                elif resp.status == 403:
                    return {"url": bucket_url, "status": "private"}
                else:
                    return {"url": bucket_url, "status": "not_found", "code": resp.status}
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            return {"url": bucket_url, "status": "error", "message": str(e)}
        except Exception as e:
            return {"url": bucket_url, "status": "error", "message": f"Unexpected error: {str(e)}"}

    async def list_public_files(self, _bucket_url: str) -> List[str]:
        """Attempts to list files in a public S3 bucket."""
        # Simple XML parsing would happen here
        return []

    async def audit_target_on_cloud(self, target: str) -> List[Dict[str, Any]]:
        """Scans for common bucket names based on target name."""
        results = []
        tasks = []
        for pattern in self.BUCKET_PATTERNS:
            url = "https://" + pattern.format(target=target, region="us-east-1")
            tasks.append(self.check_bucket_accessibility(url))

        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    def get_gcp_audit_targets() -> List[str]:
        """GCP services to audit for security misconfigurations (Ported from gcp_scanner)."""
        return [
            "bigquery",
            "bigtable",
            "cloud_functions",
            "compute_disks",
            "compute_firewalls",
            "compute_instances",
            "dns_managed_zones",
            "iam_policies",
            "kms_keys",
            "service_accounts",
            "sql_instances",
            "storage_buckets",
            "pubsub_subscriptions",
        ]

    @staticmethod
    def get_dangling_resource_indicators() -> Dict[str, str]:
        """Indicators of dangling or orphaned cloud resources (Ported from ghostbuster)."""
        return {
            "danging_elastic_ip": "DNS records pointing to Elastic IPs not associated with any instance",
            "orphaned_dns_record": "Route53/CloudDNS entries pointing to deleted load balancers or S3 buckets",
            "unused_network_interface": "ENIs with 'available' status potentially incurring costs or security risks",
        }

    @staticmethod
    def get_cspm_misconfigurations() -> Dict[str, Dict[str, Any]]:
        """Common cloud misconfigurations across AWS, Azure, and GCP (Ported from fixinventory)."""
        return {
            "unencrypted_storage": {
                "desc": "Storage volumes (EBS, Managed Disks) not encrypted at rest",
                "severity": "HIGH",
            },
            "public_buckets": {
                "desc": "S3 buckets or Azure Blobs with public read/write access",
                "severity": "CRITICAL",
            },
            "exposed_management_ports": {
                "desc": "Security groups allowing 22 (SSH) or 3389 (RDP) from 0.0.0.0/0",
                "severity": "HIGH",
            },
            "mfa_disabled_admins": {
                "desc": "Privileged IAM users without Multi-Factor Authentication",
                "severity": "CRITICAL",
            },
            "root_account_usage": {
                "desc": "Recent activity detected using the cloud root account credentials",
                "severity": "MEDIUM",
            },
        }

    @staticmethod
    def get_ciem_path_finding_logic() -> Dict[str, str]:
        """Techniques for identifying lateral movement paths in cloud IAM."""
        return {
            "role_assumption_chain": "Tracing 'AssumeRole' permissions to find escalation paths to AdministratorAccess",
            "cross_account_trust": "Identifying external accounts with trust relationships to internal roles",
            "overprivileged_service_accounts": "Finding compute instances with attached roles exceeding required scope",
            "identity_bridging_vulnerabilities": "Exploiting misconfigured SAML/OIDC providers for identity takeover",
        }

    @staticmethod
    def get_ai_spm_indicators() -> Dict[str, str]:
        """Indicators for AI service exposure and data leakage."""
        return {
            "exposed_llm_endpoints": "Identifying public-facing SageMaker, Vertex AI, or OpenAI-proxy endpoints",
            "unprotected_vector_stores": "Public unauthenticated access to Pinecone, Qdrant, or Milvus instances",
            "sensitive_data_in_training": "Identification of PII within datasets used for fine-tuning or RAG",
            "model_inversion_potential": "API configurations allowing prompts that could leak training set data",
        }

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

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class IAMIntelligence:
    """
    Intelligence module for AWS IAM Privilege Escalation analysis.
    Ported from 0xSojalSec-AWS-IAM-Privilege-Escalation.
    """

    # Mapping of escalation paths to required permissions
    ESCALATION_PATHS = {
        "CreatePolicyVersion": ["iam:CreatePolicyVersion"],
        "SetDefaultPolicyVersion": ["iam:SetDefaultPolicyVersion"],
        "CreateEC2WithRole": ["iam:PassRole", "ec2:RunInstances"],
        "CreateAccessKey": ["iam:CreateAccessKey"],
        "CreateLoginProfile": ["iam:CreateLoginProfile"],
        "UpdateLoginProfile": ["iam:UpdateLoginProfile"],
        "AttachUserPolicy": ["iam:AttachUserPolicy"],
        "AttachGroupPolicy": ["iam:AttachGroupPolicy"],
        "AttachRolePolicy": ["iam:AttachRolePolicy"],
        "PutUserPolicy": ["iam:PutUserPolicy"],
        "PutGroupPolicy": ["iam:PutGroupPolicy"],
        "PutRolePolicy": ["iam:PutRolePolicy"],
        "AddUserToGroup": ["iam:AddUserToGroup"],
        "UpdateAssumeRolePolicy": ["iam:UpdateAssumeRolePolicy", "sts:AssumeRole"],
        "LambdaPassRoleInvoke": ["iam:PassRole", "lambda:CreateFunction", "lambda:InvokeFunction"],
        "GlueUpdateDevEndpoint": ["iam:PassRole", "glue:UpdateDevEndpoint"],
        "CloudFormationStackCreation": ["iam:PassRole", "cloudformation:CreateStack"],
        "DataPipelineActivation": ["iam:PassRole", "datapipeline:CreatePipeline", "datapipeline:PutPipelineDefinition"],
    }

    @staticmethod
    def identify_escalation_opportunities(current_permissions: List[str]) -> List[Dict[str, Any]]:
        """
        Identifies potential privilege escalation paths based on a list of current IAM permissions.
        """
        opportunities = []

        # Normalize permissions to lowercase for comparison if needed,
        # but AWS is case-sensitive for action names usually.
        # We assume standard naming.

        for name, req_perms in IAMIntelligence.ESCALATION_PATHS.items():
            if all(
                perm in current_permissions
                or "*" in current_permissions
                or f"{perm.split(':')[0]}:*" in current_permissions
                for perm in req_perms
            ):
                opportunities.append(
                    {"path": name, "required_permissions": req_perms, "description": f"Potential escalation via {name}"}
                )

        return opportunities

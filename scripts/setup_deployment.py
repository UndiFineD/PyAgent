#!/usr/bin/env python3
# Utility to bootstrap deployment directory structure

import os


def create_deployment_structure(root: str) -> None:
    paths = [
        "Deployment/development/servers",
        "Deployment/development/networks",
        "Deployment/development/services",
        "Deployment/staging/servers",
        "Deployment/staging/networks",
        "Deployment/staging/services",
        "Deployment/production/servers",
        "Deployment/production/networks",
        "Deployment/production/services",
        "Deployment/infrastructure/cloud_provider",
        "Deployment/infrastructure/load_balancers",
        "Deployment/infrastructure/databases",
        "Deployment/infrastructure/monitoring",
    ]
    for p in paths:
        os.makedirs(os.path.join(root, p), exist_ok=True)

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\vibrant.py\agentns.py\scripts.py\buy_domain_8afecfde82a4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\vibrant\agentns\scripts\buy_domain.py

#!/usr/bin/env python3

"""

AgentNS Domain Purchase Script

Usage:

    python buy_domain.py <domain>

Example:

    python buy_domain.py myagent.xyz

Dependencies:

    pip install httpx eth-account siwe

"""

import argparse

import base64

import json

import os

import secrets

import sys

import time

import httpx

from eth_account import Account

from eth_account.messages import encode_defunct

from payment_utils import (
    CHAIN_ID,
    load_or_create_wallet,
    sign_eip3009_authorization,
)

from siwe import SiweMessage

# Configuration

API_BASE = os.getenv("AGENTNS_API", "https://agentns.xyz")

# Default registrant data (customize as needed)

DEFAULT_REGISTRANT = {
    "name": "Agent Smith",
    "organization": "AI Agents Inc",
    "street_address": "123 Agent Street",
    "city": "San Francisco",
    "state_province": "CA",
    "postal_code": "94102",
    "country_code": "US",
    "email": "agent@example.com",
    "phone": "+14155551234",
    "whois_privacy": True,
}


def get_nonce(client: httpx.Client) -> str:
    """Get SIWE nonce from API."""

    response = client.get(f"{API_BASE}/auth/nonce")

    response.raise_for_status()

    return response.json()["nonce"]


def authenticate(client: httpx.Client, account: Account) -> str:
    """Authenticate with SIWE and return JWT token."""

    print("Authenticating with SIWE...")

    # Get nonce

    nonce = get_nonce(client)

    # Build SIWE message

    siwe_message = SiweMessage(
        domain="agentns.xyz",
        address=account.address,
        statement="Sign in to AgentNS",
        uri=API_BASE,
        version="1",
        chain_id=CHAIN_ID,
        nonce=nonce,
        issued_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

    message_str = siwe_message.prepare_message()

    # Sign the SIWE message

    signable = encode_defunct(text=message_str)

    signed = account.sign_message(signable)

    # Verify signature with API

    response = client.post(
        f"{API_BASE}/auth/verify",
        json={
            "message": message_str,
            "signature": "0x" + signed.signature.hex(),
        },
    )

    response.raise_for_status()

    token = response.json()["access_token"]

    print("✓ Authenticated successfully")

    return token


def ensure_registrant(client: httpx.Client, token: str) -> None:
    """Ensure registrant profile exists, create if missing."""

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"{API_BASE}/registrant", headers=headers)

    if response.status_code == 200:
        print("✓ Registrant profile exists")

        return

    print("Creating registrant profile...")

    response = client.post(
        f"{API_BASE}/registrant",
        headers=headers,
        json=DEFAULT_REGISTRANT,
    )

    response.raise_for_status()

    print("✓ Registrant profile created")


def check_domain(client: httpx.Client, domain: str) -> dict:
    """Check domain availability and price."""

    print(f"Checking availability of {domain}...")

    response = client.post(f"{API_BASE}/domains/check", json={"domain": domain})

    response.raise_for_status()

    data = response.json()

    if not data["available"]:
        print(f"✗ Domain {domain} is not available")

        sys.exit(1)

    print(f"✓ Domain available: {domain}")

    print(f"  Price: {data['price_usdc']} USDC")

    return data


def register_domain(client: httpx.Client, token: str, account: Account, domain: str, years: int = 1) -> dict:
    """Register domain with x402 payment."""

    headers = {"Authorization": f"Bearer {token}"}

    print(f"Registering {domain} for {years} year(s)...")

    # First request - get 402 with payment requirement

    response = client.post(
        f"{API_BASE}/domains/register",
        headers=headers,
        json={"domain": domain, "years": years},
    )

    if response.status_code != 402:
        if response.status_code == 201:
            print("✓ Domain registered (no payment required?)")

            return response.json()

        response.raise_for_status()

    # Parse payment requirement

    payment_required = response.headers.get("X-PAYMENT-REQUIRED")

    if not payment_required:
        print("✗ No payment requirement in 402 response")

        sys.exit(1)

    requirement = json.loads(base64.b64decode(payment_required))

    print(f"  Payment required: {int(requirement['maxAmountRequired']) / 1e6} USDC")

    print(f"  Pay to: {requirement['payTo']}")

    # Generate authorization nonce

    auth_nonce = "0x" + secrets.token_hex(32)

    valid_after = 0

    valid_before = int(time.time()) + requirement["maxTimeoutSeconds"]

    # Sign EIP-3009 authorization

    print("Signing payment authorization...")

    payment_payload = sign_eip3009_authorization(
        account=account,
        to_address=requirement["payTo"],
        value=requirement["maxAmountRequired"],
        valid_after=valid_after,
        valid_before=valid_before,
        nonce=auth_nonce,
    )

    # Build X-PAYMENT header

    x_payment = {
        "x402Version": 1,
        "scheme": "exact",
        "network": requirement["network"],
        "payload": payment_payload,
    }

    x_payment_encoded = base64.b64encode(json.dumps(x_payment).encode()).decode()

    # Resubmit with payment

    print("Submitting payment...")

    headers["X-PAYMENT"] = x_payment_encoded

    response = client.post(
        f"{API_BASE}/domains/register",
        headers=headers,
        json={"domain": domain, "years": years},
    )

    if response.status_code == 201:
        print(f"✓ Domain {domain} registered successfully!")

        return response.json()

    print(f"✗ Registration failed: {response.status_code}")

    print(response.text)

    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Register a domain via AgentNS")

    parser.add_argument("domain", help="Domain to register (e.g., myagent.xyz)")

    parser.add_argument("--years", type=int, default=1, help="Years to register (1-10)")

    parser.add_argument("--check-only", action="store_true", help="Only check availability")

    args = parser.parse_args()

    # Load or create wallet

    account = load_or_create_wallet()

    with httpx.Client(timeout=60) as client:
        # Check domain first

        check_domain(client, args.domain)

        if args.check_only:
            return

        # Authenticate

        token = authenticate(client, account)

        # Ensure registrant profile

        ensure_registrant(client, token)

        # Register domain

        result = register_domain(client, token, account, args.domain, args.years)

        print(f"\nDomain details:")

        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

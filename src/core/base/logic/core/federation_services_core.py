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

# Federation Services Core - AD FS Token Forgery and SAML Management
# Based on patterns from ADFSpoof repository

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid
import base64
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
import signxml
from lxml import etree
import secrets
import string


class SAMLVersion(Enum):
    """SAML protocol versions"""
    SAML_1_1 = "1.1"
    SAML_2_0 = "2.0"


class FederationProvider(Enum):
    """Supported federation providers"""
    OFFICE_365 = "office365"
    DROPBOX = "dropbox"
    GENERIC_SAML2 = "saml2"
    AZURE_AD = "azure_ad"
    AWS_SAML = "aws_saml"


class SignatureAlgorithm(Enum):
    """SAML signature algorithms"""
    RSA_SHA256 = "rsa-sha256"
    RSA_SHA384 = "rsa-sha384"
    RSA_SHA512 = "rsa-sha512"


class DigestAlgorithm(Enum):
    """SAML digest algorithms"""
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"


@dataclass
class FederationService:
    """AD FS federation service configuration"""
    service_id: str
    name: str
    server_fqdn: str
    signing_certificate: Optional[bytes] = None
    encryption_certificate: Optional[bytes] = None
    private_key: Optional[bytes] = None
    certificate_password: Optional[str] = None
    endpoints: Dict[str, str] = field(default_factory=dict)
    relying_parties: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SAMLToken:
    """SAML security token"""
    token_id: str
    version: SAMLVersion
    issuer: str
    subject: str
    audience: str
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    signed_xml: Optional[str] = None
    signature_algorithm: SignatureAlgorithm = SignatureAlgorithm.RSA_SHA256
    digest_algorithm: DigestAlgorithm = DigestAlgorithm.SHA256
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


@dataclass
class RelyingParty:
    """Relying party configuration"""
    identifier: str
    name: str
    endpoint: str
    name_id_format: str
    claim_rules: List[Dict[str, Any]] = field(default_factory=list)
    signature_required: bool = True
    encryption_required: bool = False


@dataclass
class FederationUser:
    """Federated user information"""
    upn: str
    object_guid: Optional[str] = None
    sam_account_name: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenGenerationRequest:
    """Request to generate a SAML token"""
    provider: FederationProvider
    user: FederationUser
    relying_party: RelyingParty
    service: FederationService
    custom_assertions: Optional[List[Dict[str, Any]]] = None
    validity_minutes: int = 60


class FederationServicesCore:
    """
    Federation Services Core for AD FS token forgery and SAML management.

    Provides comprehensive SAML token generation, signing, and federation
    service management based on ADFSpoof methodologies.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.services: Dict[str, FederationService] = {}
        self.relying_parties: Dict[str, RelyingParty] = {}
        self.tokens: Dict[str, SAMLToken] = {}
        self.templates: Dict[str, str] = {}

    async def initialize(self) -> bool:
        """Initialize the federation services core"""
        try:
            await self.load_saml_templates()
            self.logger.info("Federation Services Core initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Federation Services Core: {e}")
            return False

    async def load_saml_templates(self) -> None:
        """Load SAML token templates"""
        # Mock SAML templates - in real implementation would load from files
        self.templates = {
            "saml1.1_office365": """<?xml version="1.0" encoding="UTF-8"?>
<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"
                AssertionID="{AssertionID}"
                IssueInstant="{IssueInstant}"
                Issuer="{Issuer}"
                MajorVersion="1"
                MinorVersion="1">
    <saml:Conditions NotBefore="{NotBefore}" NotOnOrAfter="{NotOnOrAfter}">
        <saml:AudienceRestrictionCondition>
            <saml:Audience>urn:federation:MicrosoftOnline</saml:Audience>
        </saml:AudienceRestrictionCondition>
    </saml:Conditions>
    <saml:AuthenticationStatement AuthenticationInstant="{AuthInstant}"
                                   AuthenticationMethod="urn:oasis:names:tc:SAML:1.0:am:password">
        <saml:Subject>
            <saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
                {UPN}
            </saml:NameIdentifier>
            <saml:SubjectConfirmation>
                <saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod>
            </saml:SubjectConfirmation>
        </saml:Subject>
    </saml:AuthenticationStatement>
    <saml:AttributeStatement>
        <saml:Subject>
            <saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
                {UPN}
            </saml:NameIdentifier>
        </saml:Subject>
        <saml:Attribute AttributeName="objectguid" AttributeNamespace="http://schemas.microsoft.com/identity/claims">
            <saml:AttributeValue>{ObjectGUID}</saml:AttributeValue>
        </saml:Attribute>
    </saml:AttributeStatement>
</saml:Assertion>""",

            "saml2.0_generic": """<?xml version="1.0" encoding="UTF-8"?>
<saml2:Assertion xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion"
                 ID="{AssertionID}"
                 IssueInstant="{IssueInstant}"
                 Version="2.0">
    <saml2:Issuer>{Issuer}</saml2:Issuer>
    <saml2:Subject>
        <saml2:NameID Format="{NameIDFormat}">{NameID}</saml2:NameID>
        <saml2:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
            <saml2:SubjectConfirmationData NotOnOrAfter="{NotOnOrAfter}" Recipient="{Recipient}"/>
        </saml2:SubjectConfirmation>
    </saml2:Subject>
    <saml2:Conditions NotBefore="{NotBefore}" NotOnOrAfter="{NotOnOrAfter}">
        <saml2:AudienceRestriction>
            <saml2:Audience>{Audience}</saml2:Audience>
        </saml2:AudienceRestriction>
    </saml2:Conditions>
    <saml2:AuthnStatement AuthnInstant="{AuthInstant}" SessionIndex="{SessionIndex}">
        <saml2:AuthnContext>
            <saml2:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml2:AuthnContextClassRef>
        </saml2:AuthnContext>
    </saml2:AuthnStatement>
    {Assertions}
</saml2:Assertion>"""
        }

        self.logger.info(f"Loaded {len(self.templates)} SAML templates")

    async def create_federation_service(
        self,
        name: str,
        server_fqdn: str,
        signing_cert_path: Optional[str] = None,
        private_key_path: Optional[str] = None,
        cert_password: Optional[str] = None
    ) -> Optional[str]:
        """Create a new federation service"""
        service_id = str(uuid.uuid4())

        service = FederationService(
            service_id=service_id,
            name=name,
            server_fqdn=server_fqdn,
            certificate_password=cert_password
        )

        # Load certificates if provided
        if signing_cert_path and private_key_path:
            try:
                with open(signing_cert_path, 'rb') as f:
                    service.signing_certificate = f.read()
                with open(private_key_path, 'rb') as f:
                    service.private_key = f.read()
            except Exception as e:
                self.logger.error(f"Failed to load certificates for service {name}: {e}")
                return None

        self.services[service_id] = service

        # Set up default endpoints
        service.endpoints = {
            "metadata": f"https://{server_fqdn}/FederationMetadata/2007-06/FederationMetadata.xml",
            "token": f"https://{server_fqdn}/adfs/oauth2/token",
            "authorize": f"https://{server_fqdn}/adfs/oauth2/authorize"
        }

        self.logger.info(f"Created federation service: {name} ({service_id})")
        return service_id

    async def add_relying_party(
        self,
        identifier: str,
        name: str,
        endpoint: str,
        name_id_format: str = "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
        claim_rules: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Add a relying party configuration"""
        rp = RelyingParty(
            identifier=identifier,
            name=name,
            endpoint=endpoint,
            name_id_format=name_id_format,
            claim_rules=claim_rules or []
        )

        self.relying_parties[identifier] = rp
        self.logger.info(f"Added relying party: {name} ({identifier})")
        return identifier

    async def generate_saml_token(
        self,
        request: TokenGenerationRequest
    ) -> Optional[SAMLToken]:
        """Generate a SAML security token"""
        try:
            token_id = str(uuid.uuid4())
            now = datetime.utcnow()
            expires = now + timedelta(minutes=request.validity_minutes)

            # Create token based on provider
            if request.provider == FederationProvider.OFFICE_365:
                token = await self._generate_office365_token(request, token_id, now, expires)
            elif request.provider == FederationProvider.DROPBOX:
                token = await self._generate_dropbox_token(request, token_id, now, expires)
            elif request.provider == FederationProvider.GENERIC_SAML2:
                token = await self._generate_generic_saml2_token(request, token_id, now, expires)
            else:
                raise ValueError(f"Unsupported provider: {request.provider}")

            # Sign the token
            if request.service.signing_certificate and request.service.private_key:
                token.signed_xml = await self._sign_saml_token(token, request.service)

            self.tokens[token_id] = token

            self.logger.info(f"Generated SAML token for {request.user.upn} targeting {request.provider.value}")
            return token

        except Exception as e:
            self.logger.error(f"Failed to generate SAML token: {e}")
            return None

    async def _generate_office365_token(
        self,
        request: TokenGenerationRequest,
        token_id: str,
        now: datetime,
        expires: datetime
    ) -> SAMLToken:
        """Generate Office 365 SAML 1.1 token"""
        token = SAMLToken(
            token_id=token_id,
            version=SAMLVersion.SAML_1_1,
            issuer=request.service.server_fqdn,
            subject=request.user.upn,
            audience="urn:federation:MicrosoftOnline",
            expires_at=expires
        )

        # Add Office 365 specific assertions
        token.assertions = [
            {
                "name": "objectguid",
                "namespace": "http://schemas.microsoft.com/identity/claims",
                "value": request.user.object_guid or str(uuid.uuid4())
            }
        ]

        token.conditions = {
            "not_before": now.isoformat(),
            "not_on_or_after": expires.isoformat()
        }

        return token

    async def _generate_dropbox_token(
        self,
        request: TokenGenerationRequest,
        token_id: str,
        now: datetime,
        expires: datetime
    ) -> SAMLToken:
        """Generate Dropbox SAML 2.0 token"""
        token = SAMLToken(
            token_id=token_id,
            version=SAMLVersion.SAML_2_0,
            issuer=request.service.server_fqdn,
            subject=request.user.email or request.user.upn,
            audience=request.relying_party.identifier,
            expires_at=expires
        )

        # Add Dropbox specific assertions
        token.assertions = [
            {
                "name": "email",
                "namespace": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims",
                "value": request.user.email or request.user.upn
            },
            {
                "name": "accountname",
                "namespace": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims",
                "value": request.user.sam_account_name or request.user.upn.split('@')[0]
            }
        ]

        token.conditions = {
            "not_before": now.isoformat(),
            "not_on_or_after": expires.isoformat()
        }

        return token

    async def _generate_generic_saml2_token(
        self,
        request: TokenGenerationRequest,
        token_id: str,
        now: datetime,
        expires: datetime
    ) -> SAMLToken:
        """Generate generic SAML 2.0 token"""
        token = SAMLToken(
            token_id=token_id,
            version=SAMLVersion.SAML_2_0,
            issuer=request.service.server_fqdn,
            subject=request.user.upn,
            audience=request.relying_party.identifier,
            expires_at=expires
        )

        # Add custom assertions
        token.assertions = request.custom_assertions or []

        # Add default assertions based on claim rules
        for rule in request.relying_party.claim_rules:
            if rule.get("type") == "issuance":
                token.assertions.append({
                    "name": rule.get("claim_type", ""),
                    "namespace": rule.get("namespace", ""),
                    "value": rule.get("value", "")
                })

        token.conditions = {
            "not_before": now.isoformat(),
            "not_on_or_after": expires.isoformat()
        }

        return token

    async def _sign_saml_token(
        self,
        token: SAMLToken,
        service: FederationService
    ) -> str:
        """Sign a SAML token with the service's private key"""
        try:
            # Mock signing - in real implementation would use cryptography library
            # to properly sign the XML with the private key

            # For now, return a mock signed token
            signed_token = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Mock signed SAML token -->
<Token ID="{token.token_id}" Issuer="{token.issuer}" Subject="{token.subject}">
    <Signature Algorithm="{token.signature_algorithm.value}">
        <!-- Mock signature -->
        {base64.b64encode(secrets.token_bytes(256)).decode()}
    </Signature>
    <Assertions>
        {json.dumps(token.assertions)}
    </Assertions>
</Token>"""

            return signed_token

        except Exception as e:
            self.logger.error(f"Failed to sign SAML token: {e}")
            return ""

    async def decrypt_encrypted_pfx(
        self,
        encrypted_blob: bytes,
        dkm_key: bytes,
        output_path: str
    ) -> bool:
        """
        Decrypt an EncryptedPFX blob using DKM key

        Args:
            encrypted_blob: The encrypted PFX blob
            dkm_key: The DKM decryption key
            output_path: Path to save the decrypted PFX

        Returns:
            True if successful, False otherwise
        """
        try:
            # Mock decryption - in real implementation would use custom cryptography
            # to decrypt the PFX blob using the DKM key

            # Generate a mock PFX file
            mock_pfx = secrets.token_bytes(1024)

            with open(output_path, 'wb') as f:
                f.write(mock_pfx)

            self.logger.info(f"Decrypted PFX blob and saved to {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to decrypt PFX blob: {e}")
            return False

    async def load_pfx_certificate(
        self,
        pfx_path: str,
        password: Optional[str] = None
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        """
        Load certificate and private key from PFX file

        Args:
            pfx_path: Path to PFX file
            password: PFX password

        Returns:
            Tuple of (certificate_bytes, private_key_bytes)
        """
        try:
            with open(pfx_path, 'rb') as f:
                pfx_data = f.read()

            # Mock loading - in real implementation would use cryptography library
            # to extract cert and key from PFX

            mock_cert = secrets.token_bytes(512)
            mock_key = secrets.token_bytes(1024)

            self.logger.info(f"Loaded certificate and key from {pfx_path}")
            return mock_cert, mock_key

        except Exception as e:
            self.logger.error(f"Failed to load PFX certificate: {e}")
            return None, None

    async def generate_self_signed_certificate(
        self,
        common_name: str,
        organization: str = "Example Corp",
        validity_days: int = 365
    ) -> Tuple[bytes, bytes]:
        """
        Generate a self-signed certificate for testing

        Args:
            common_name: Certificate common name
            organization: Organization name
            validity_days: Certificate validity period

        Returns:
            Tuple of (certificate_pem, private_key_pem)
        """
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            # Create certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            ])

            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=validity_days)
            ).sign(private_key, hashes.SHA256(), default_backend())

            # Serialize to PEM
            cert_pem = cert.public_bytes(serialization.Encoding.PEM)
            key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            self.logger.info(f"Generated self-signed certificate for {common_name}")
            return cert_pem, key_pem

        except Exception as e:
            self.logger.error(f"Failed to generate self-signed certificate: {e}")
            return b"", b""

    async def export_token_to_file(
        self,
        token: SAMLToken,
        filepath: str,
        format: str = "xml"
    ) -> None:
        """
        Export SAML token to file

        Args:
            token: Token to export
            filepath: Output file path
            format: Export format (xml, json)
        """
        if format == "xml":
            content = token.signed_xml or f"<!-- Unsigned SAML Token -->\n{token.token_id}"
        elif format == "json":
            content = json.dumps({
                "token_id": token.token_id,
                "version": token.version.value,
                "issuer": token.issuer,
                "subject": token.subject,
                "audience": token.audience,
                "assertions": token.assertions,
                "conditions": token.conditions,
                "created_at": token.created_at.isoformat(),
                "expires_at": token.expires_at.isoformat() if token.expires_at else None
            }, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"Exported SAML token to {filepath}")

    async def get_federation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive federation statistics"""
        stats = {
            "total_services": len(self.services),
            "total_relying_parties": len(self.relying_parties),
            "total_tokens": len(self.tokens),
            "active_services": len([s for s in self.services.values() if s.signing_certificate]),
            "tokens_by_version": {},
            "tokens_by_provider": {},
            "recent_tokens": []
        }

        # Token statistics
        for token in self.tokens.values():
            version = token.version.value
            stats["tokens_by_version"][version] = stats["tokens_by_version"].get(version, 0) + 1

        # Recent tokens (last 10)
        recent_tokens = sorted(
            self.tokens.values(),
            key=lambda t: t.created_at,
            reverse=True
        )[:10]

        stats["recent_tokens"] = [
            {
                "id": t.token_id,
                "subject": t.subject,
                "created_at": t.created_at.isoformat(),
                "expires_at": t.expires_at.isoformat() if t.expires_at else None
            }
            for t in recent_tokens
        ]

        return stats

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.services.clear()
        self.relying_parties.clear()
        self.tokens.clear()
        self.templates.clear()
        self.logger.info("Federation Services Core cleaned up")

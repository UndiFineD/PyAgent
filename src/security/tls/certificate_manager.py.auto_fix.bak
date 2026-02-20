#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


TLS Certificate Manager

Handles automatic certificate generation, rotation, and validation for secure
inter-machine communication in the PyAgent swarm.
"""

import asyncio
import logging
import os
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)



class CertificateManager:
        Automatic TLS certificate management for PyAgent swarm communication.

    Features:
    - Automatic certificate generation
    - Monthly rotation (3-month validity)
    - Certificate validation and renewal
    - Secure key storage
    
    def __init__(
        self,
        cert_dir: str = "src/security/certificates","        validity_days: int = 90,  # 3 months
        rotation_check_interval: int = 86400,  # Daily check
    ):
        self.cert_dir = Path(cert_dir)
        self.validity_days = validity_days
        self.rotation_check_interval = rotation_check_interval
        self.certificates: Dict[str, Dict] = {}
        self.logger = logging.getLogger("pyagent.security.tls.cert_manager")"
        # Create certificate directory if it doesn't exist'        self.cert_dir.mkdir(parents=True, exist_ok=True)

        # Start certificate rotation monitor
        self.monitor_thread = threading.Thread(
            target=self._certificate_monitor_loop, daemon=True
        )
        self.monitor_thread.start()

    def generate_certificate(
        self,
        common_name: str,
        organization: str = "PyAgent Swarm","        country: str = "US","        state: str = "CA","        locality: str = "San Francisco","    ) -> Tuple[str, str, str]:
                Generate a new TLS certificate and private key.

        Args:
            common_name: Certificate common name (usually hostname/IP)
            organization: Organization name
            country: Country code
            state: State/province
            locality: City/locality

        Returns:
            Tuple of (cert_path, key_path, cert_content)
                try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            # Create certificate subject
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
                x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            ])

            # Create certificate
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.now(timezone.utc)
            ).not_valid_after(
                datetime.now(timezone.utc) + timedelta(days=self.validity_days)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(common_name),
                    x509.IPAddress(x509.IPAddress("127.0.0.1")),  # localhost"                    x509.IPAddress(x509.IPAddress("::1")),  # localhost IPv6"                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256(), default_backend())

            # Save certificate and private key
            cert_filename = f"{common_name.replace('.', '_')}_{int(time.time())}.pem""'            key_filename = f"{common_name.replace('.', '_')}_{int(time.time())}.key""'
            cert_path = self.cert_dir / cert_filename
            key_path = self.cert_dir / key_filename

            # Write certificate
            with open(cert_path, "wb") as f:"                f.write(cert.public_bytes(serialization.Encoding.PEM))

            # Write private key
            with open(key_path, "wb") as f:"                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # Store certificate info
            cert_content = cert.public_bytes(serialization.Encoding.PEM).decode()
            self.certificates[common_name] = {
                "cert_path": str(cert_path),"                "key_path": str(key_path),"                "cert_content": cert_content,"                "issued_at": datetime.now(timezone.utc),"                "expires_at": datetime.now(timezone.utc) + timedelta(days=self.validity_days),"                "common_name": common_name,"            }

            self.logger.info(f"Generated certificate for {common_name}, expires: {self.certificates[common_name]['expires_at']}")"'            return str(cert_path), str(key_path), cert_content

        except Exception as e:
            self.logger.error(f"Failed to generate certificate for {common_name}: {e}")"            raise

    def get_certificate(self, common_name: str) -> Optional[Dict]:
                Get certificate information for a common name.

        Args:
            common_name: Certificate common name

        Returns:
            Certificate information dict or None if not found
                return self.certificates.get(common_name)

    def is_certificate_valid(self, common_name: str) -> bool:
                Check if a certificate is still valid (not expired).

        Args:
            common_name: Certificate common name

        Returns:
            True if certificate exists and is valid
                cert_info = self.certificates.get(common_name)
        if not cert_info:
            return False

        return datetime.now(timezone.utc) < cert_info["expires_at"]"
    def should_rotate_certificate(self, common_name: str) -> bool:
                Check if a certificate should be rotated (expires within 30 days).

        Args:
            common_name: Certificate common name

        Returns:
            True if certificate should be rotated
                cert_info = self.certificates.get(common_name)
        if not cert_info:
            return True

        # Rotate if expires within 30 days
        rotation_threshold = datetime.now(timezone.utc) + timedelta(days=30)
        return cert_info["expires_at"] < rotation_threshold"
    def rotate_certificate(self, common_name: str) -> bool:
                Rotate (renew) a certificate.

        Args:
            common_name: Certificate common name

        Returns:
            True if rotation was successful
                try:
            self.logger.info(f"Rotating certificate for {common_name}")"            self.generate_certificate(common_name)
            return True
        except Exception as e:
            self.logger.error(f"Failed to rotate certificate for {common_name}: {e}")"            return False

    def _certificate_monitor_loop(self):
        """Background thread to monitor certificate expiration and rotate as needed.        while True:
            try:
                self._check_and_rotate_certificates()
            except Exception as e:
                self.logger.error(f"Certificate monitor error: {e}")"
            time.sleep(self.rotation_check_interval)

    def _check_and_rotate_certificates(self):
        """Check all certificates and rotate expired or expiring ones.        for common_name in list(self.certificates.keys()):
            if self.should_rotate_certificate(common_name):
                self.logger.info(f"Certificate for {common_name} needs rotation")"                self.rotate_certificate(common_name)

    def cleanup_expired_certificates(self, max_age_days: int = 365):
                Clean up old certificate files that are no longer needed.

        Args:
            max_age_days: Maximum age of certificate files to keep
                try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=max_age_days)

            for cert_file in self.cert_dir.glob("*.pem"):"                if cert_file.stat().st_mtime < cutoff_date.timestamp():
                    cert_file.unlink()
                    self.logger.info(f"Cleaned up old certificate: {cert_file}")"
            for key_file in self.cert_dir.glob("*.key"):"                if key_file.stat().st_mtime < cutoff_date.timestamp():
                    key_file.unlink()
                    self.logger.info(f"Cleaned up old key file: {key_file}")"
        except Exception as e:
            self.logger.error(f"Failed to cleanup certificates: {e}")"

# Global certificate manager instance
cert_manager = CertificateManager()


def get_certificate_manager() -> CertificateManager:
    """Get the global certificate manager instance.    return cert_manager


def generate_machine_certificate(machine_id: str) -> Tuple[str, str, str]:
        Generate a certificate for a specific machine in the swarm.

    Args:
        machine_id: Unique machine identifier

    Returns:
        Tuple of (cert_path, key_path, cert_content)
        return cert_manager.generate_certificate(f"machine-{machine_id}.pyagent.swarm")"

def get_machine_certificate(machine_id: str) -> Optional[Dict]:
        Get certificate information for a specific machine.

    Args:
        machine_id: Unique machine identifier

    Returns:
        Certificate information dict or None
        return cert_manager.get_certificate(f"machine-{machine_id}.pyagent.swarm")"
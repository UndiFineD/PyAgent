# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\core\cert_manager.py
import datetime
import hashlib
import ipaddress
import logging
import os
import socket
import ssl

import certifi
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID, ObjectIdentifier


class CertManager:
    def __init__(
        self, cert_dir=os.path.join(os.getcwd(), "certs"), ca_common_name="VPN Root CA"
    ):
        self.cert_dir = cert_dir
        os.makedirs(cert_dir, exist_ok=True)
        self.ca_common_name = ca_common_name
        self.server_thumbprint = {}
        self.dns_name = os.getenv("SERVER_FQDN", socket.gethostname())
        self.ip_address = os.getenv(
            "EXTERNAL_IP", socket.gethostbyname(socket.gethostname())
        )

    def setup(self):
        """Setup the certificates and load the SSL context"""
        self.load_ca_certificate()
        self.load_dns_certificate()
        self.load_ip_certificate()
        self.create_ssl_context()

        # server thumbprint is a dictionary with sha1 and md5 hashes of the DNS cert
        self.server_thumbprint = self.get_cert_thumbprint(self.dns_cert_path)

    def create_ssl_context(self):
        """Create SSL context with SNI support and proper TLS configuration"""
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        def sni_callback(sslsocket, sni_name, sslcontext):
            try:
                if not sni_name:
                    sslsocket.context = self.ssl_context
                    return None

                logging.debug(f"SNI hostname requested: {sni_name}")

                # Create a new context for this connection
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

                if sni_name == self.dns_name:
                    ctx.load_cert_chain(self.dns_cert_path, self.dns_key_path)
                else:
                    ctx.load_cert_chain(self.ip_cert_path, self.ip_key_path)

                # Set the new context
                sslsocket.context = ctx

            except Exception as e:
                logging.error(f"Error in SNI callback: {e}")
            return None

        # Set the SNI callback
        self.ssl_context.sni_callback = sni_callback

        # Load default certificate (IP cert)
        self.ssl_context.load_cert_chain(
            certfile=self.ip_cert_path, keyfile=self.ip_key_path
        )

        return self.ssl_context

    def load_ip_certificate(self):
        """Load or generate a certificate for the server's external IP address"""
        self.ip_cert_path = os.path.join(self.cert_dir, f"server-ip.crt")
        self.ip_key_path = os.path.join(self.cert_dir, f"server-ip.key")
        if (
            os.path.exists(self.ip_cert_path)
            and os.path.exists(self.ip_key_path)
            and self.cert_is_valid(self.ip_cert_path, self.ip_address)
        ):
            logging.info(f"Using existing certificate for: {self.ip_address}")
            return self.ip_cert_path, self.ip_key_path
        else:
            logging.info(f"Generating new certificate for: {self.ip_address}")
        return self.generate_server_certificate(
            self.ip_cert_path,
            self.ip_key_path,
            self.ip_address,
            additional_ekus=[ObjectIdentifier("1.3.6.1.5.5.7.3.5")],
            additional_sans=[
                x509.IPAddress(ipaddress.IPv4Address(self.ip_address)),
                x509.DNSName(self.dns_name),
            ],
        )

    def load_dns_certificate(self):
        """Load or generate a certificate for the server's DNS name"""
        # this certificate may be volume mounted (e.g. when using certbot outside of the container)
        self.dns_cert_path = os.path.join(self.cert_dir, f"server-dns.crt")
        self.dns_key_path = os.path.join(self.cert_dir, f"server-dns.key")
        if (
            os.path.exists(self.dns_cert_path)
            and os.path.exists(self.dns_key_path)
            and self.cert_is_valid(self.dns_cert_path, self.dns_name)
        ):
            logging.info(f"Using existing certificate for: {self.dns_name}")
            return self.dns_cert_path, self.dns_key_path
        else:
            logging.info(f"Generating new certificate for: {self.dns_name}")
        return self.generate_server_certificate(
            self.dns_cert_path,
            self.dns_key_path,
            self.dns_name,
            additional_sans=[x509.DNSName(self.dns_name)],
        )

    def load_ca_certificate(self):
        """Load or generate the CA certificate"""
        self.ca_cert_path = os.path.join(self.cert_dir, "ca.crt")
        self.ca_key_path = os.path.join(self.cert_dir, "ca.key")
        if os.path.exists(self.ca_cert_path) and os.path.exists(self.ca_key_path):
            with open(self.ca_cert_path, "rb") as f:
                self.ca_cert = x509.load_pem_x509_certificate(
                    f.read(), default_backend()
                )
            with open(self.ca_key_path, "rb") as f:
                self.ca_key = serialization.load_pem_private_key(
                    f.read(), password=None, backend=default_backend()
                )
            return self.ca_cert_path, self.ca_key_path
        else:
            return self.generate_ca_certificate()

    def cert_is_valid(self, cert_path, common_name):
        """Check if the certificate is valid"""

        # skip certificate validation if we're overriding the thumbprint or retrieving it dynamically from the server
        # this allows us to keep serving our origin certificate while advertising the proxy thumbprint
        # this is needed for certain proxies which require the origin has a valid certificate
        # if we didn't do this, the cert manager would detect a mismatch and re-generate the certificate
        if (
            os.getenv("USE_DYNAMIC_SERVER_THUMBPRINT", "false").lower() == "true"
            or os.getenv("SERVER_SHA1_THUMBPRINT", "") != ""
            or os.getenv("SERVER_MD5_THUMBPRINT", "") != ""
        ):
            return True

        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())

        date_valid = (
            cert.not_valid_before_utc
            <= datetime.datetime.now(datetime.timezone.utc)
            <= cert.not_valid_after_utc
        )

        if not date_valid:
            logging.error(f"Certificate for {common_name} is expired")
            return False

        cert_common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[
            0
        ].value
        name_valid = cert_common_name == common_name

        if not name_valid:
            logging.error(
                f"Certificate for {cert_common_name} is not valid for {common_name}"
            )
            return False

        # check if the issuer Common Name matches our self-signed CA
        # if the issuer name matches, but the cert is not validly signed by the current CA, return False
        # this helps to identify stale certificates when the CA certificate has been re-generated
        if (
            cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            == self.ca_common_name
        ):
            try:
                self.ca_cert.public_key().verify(
                    cert.signature,
                    cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    cert.signature_hash_algorithm,
                )
                logging.info(
                    f"Certificate is validly signed by our CA. Will not re-generate."
                )
            except Exception as e:
                logging.warning(
                    f"Certificate is not validly signed by the current CA: {e}. Will re-generate."
                )
                return False
        else:
            # if the cert wasn't issued by our CA, then it's probably been signed by a public CA,
            # such as Let's Encrypt, and we should not re-generate it.
            # TODO: we may wish to check that the cert chains to a trusted root CA in the future,
            # but it doesn't really matter for our use case
            logging.warning(
                f"Certificate was not issued by our CA. Will not re-generate."
            )
            return True

        return True

    def get_thumbprint_from_server(self, server_address):
        """Get the certificate thumbprint from a server"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((server_address, 443), timeout=5) as sock:
                with context.wrap_socket(
                    sock, server_hostname=server_address
                ) as wrapped_sock:
                    der_cert = wrapped_sock.getpeercert(binary_form=True)
                    thumbprint_sha1 = hashlib.sha1(der_cert).hexdigest().upper()
                    thumbprint_md5 = hashlib.md5(der_cert).hexdigest().upper()
                    return {"sha1": thumbprint_sha1, "md5": thumbprint_md5}
        except (socket.timeout, ssl.SSLError, ssl.CertificateError, OSError) as e:
            logging.error(f"Error getting thumbprint from server {server_address}: {e}")
            return None

    def get_cert_thumbprint(self, cert_path):
        """Calculate the certificate thumbprint"""
        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())

        der_cert = cert.public_bytes(serialization.Encoding.DER)
        thumbprint_sha1 = hashlib.sha1(der_cert).hexdigest().upper()
        thumbprint_md5 = hashlib.md5(der_cert).hexdigest().upper()

        # allow overriding the thumbprint for fronting scenarios
        thumbprint_sha1 = os.getenv("SERVER_SHA1_THUMBPRINT", thumbprint_sha1)
        thumbprint_md5 = os.getenv("SERVER_MD5_THUMBPRINT", thumbprint_md5)

        return {"sha1": thumbprint_sha1, "md5": thumbprint_md5}

    def generate_server_certificate(
        self,
        cert_path,
        key_path,
        common_name="*",
        additional_ekus=[],
        additional_sans=[],
    ):
        """Generate a server certificate"""
        # Get CA cert
        if not self.ca_cert or not self.ca_key:
            self.load_ca_certificate()

        # Generate server private key
        cert_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Build server certificate signed by CA
        subject = x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            ]
        )

        # list of SANs
        san_list = additional_sans

        # list of EKUs
        eku_list = [
            ExtendedKeyUsageOID.SERVER_AUTH,
            ExtendedKeyUsageOID.CLIENT_AUTH,
        ] + additional_ekus

        key_usage = x509.KeyUsage(
            digital_signature=True,
            key_encipherment=False,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False,
            key_cert_sign=False,
            crl_sign=False,
        )

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(self.ca_cert.subject)
            .public_key(cert_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName(san_list),
                critical=False,
            )
            .add_extension(
                x509.ExtendedKeyUsage(eku_list),
                critical=True,
            )
            .add_extension(
                key_usage,
                critical=True,
            )
            .sign(self.ca_key, hashes.SHA256(), default_backend())
        )

        # Convert certificate and key to PEM format
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        key_pem = cert_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        with open(cert_path, "wb") as cert_file:
            cert_file.write(
                cert_pem + self.ca_cert.public_bytes(serialization.Encoding.PEM)
            )

        with open(key_path, "wb") as key_file:
            key_file.write(key_pem)

        return cert_path, key_path

    def generate_ca_certificate(self):
        self.ca_key_path = os.path.join(self.cert_dir, "ca.key")
        self.ca_cert_path = os.path.join(self.cert_dir, "ca.crt")

        # Check if CA cert already exists
        if os.path.exists(self.ca_cert_path) and os.path.exists(self.ca_key_path):
            logging.info("Loading existing CA certificate")
            with open(self.ca_cert_path, "rb") as f:
                self.ca_cert = x509.load_pem_x509_certificate(
                    f.read(), default_backend()
                )
            with open(self.ca_key_path, "rb") as f:
                self.ca_key = serialization.load_pem_private_key(
                    f.read(), password=None, backend=default_backend()
                )
            return self.ca_key_path, self.ca_cert_path

        logging.info("Generating new CA certificate")
        # Generate CA private key
        self.ca_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Build CA certificate
        subject = x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, self.ca_common_name),
                # x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.ca_common_name),
            ]
        )

        self.ca_cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(self.ca_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(
                datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=1)
            )
            .not_valid_after(
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=3650)
            )
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None), critical=True
            )
            .add_extension(
                x509.SubjectKeyIdentifier.from_public_key(self.ca_key.public_key()),
                critical=False,
            )
            .add_extension(
                x509.AuthorityKeyIdentifier.from_issuer_public_key(
                    self.ca_key.public_key()
                ),
                critical=False,
            )
            .sign(self.ca_key, hashes.SHA256(), default_backend())
        )

        # Save CA cert and key
        with open(self.ca_cert_path, "wb") as f:
            f.write(self.ca_cert.public_bytes(serialization.Encoding.PEM))

        with open(self.ca_key_path, "wb") as f:
            f.write(
                self.ca_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        return self.ca_key_path, self.ca_cert_path

    def generate_codesign_certificate(
        self, common_name, pfx_path=None, cert_path=None, key_path=None
    ):
        if not self.ca_cert or not self.ca_key:
            self.load_ca_certificate()

        if pfx_path is None:
            pfx_path = os.path.join(self.cert_dir, "codesign.pfx")
        if cert_path is None:
            cert_path = os.path.join(self.cert_dir, "codesign.cer")
        if key_path is None:
            key_path = os.path.join(self.cert_dir, "codesign.key")

        if (
            os.path.exists(cert_path)
            and os.path.exists(key_path)
            and os.path.exists(pfx_path)
            and self.cert_is_valid(cert_path, common_name)
        ):
            logging.info(f"Loading existing codesigning certificate for: {common_name}")
            return pfx_path
        else:
            logging.info(f"Generating new codesigning certificate for: {common_name}")

        # Generate a private key for the code signing certificate
        codesign_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Create the code signing certificate
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])

        eku_list = [
            ExtendedKeyUsageOID.CODE_SIGNING,
        ]

        key_usage = x509.KeyUsage(
            digital_signature=True,
            key_encipherment=False,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False,
            key_cert_sign=False,
            crl_sign=False,
        )

        builder = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(self.ca_cert.subject)
            .public_key(codesign_private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(
                datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=1)
            )
            .not_valid_after(
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=365)
            )
            .add_extension(
                x509.ExtendedKeyUsage(eku_list),
                critical=True,
            )
            .add_extension(
                key_usage,
                critical=True,
            )
        )

        # Sign the certificate with the CA private key
        codesign_certificate = builder.sign(
            self.ca_key, hashes.SHA256(), default_backend()
        )

        # Save the new certificate to a file
        with open(cert_path, "wb") as f:
            f.write(codesign_certificate.public_bytes(serialization.Encoding.PEM))

        with open(key_path, "wb") as f:
            f.write(
                codesign_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Convert to pkcs12 and save to codesign.pfx
        logging.info(f"Saving codesigning certificate to {pfx_path}")
        with open(pfx_path, "wb") as f:
            f.write(
                serialization.pkcs12.serialize_key_and_certificates(
                    b"codesign",
                    codesign_private_key,
                    codesign_certificate,
                    None,
                    serialization.NoEncryption(),
                )
            )

        return pfx_path

    def generate_apple_certificate(
        self, common_name="Developer ID Installer", cert_path=None, key_path=None
    ):
        """Generate an Apple code signing certificate"""
        if cert_path is None:
            cert_path = os.path.join(self.cert_dir, "apple.cer")
        if key_path is None:
            key_path = os.path.join(self.cert_dir, "apple.key")

        # Generate a private key
        apple_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Create Apple signing certificate
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])

        # list of EKUs
        eku_list = [
            ExtendedKeyUsageOID.CODE_SIGNING,
            ObjectIdentifier(
                "1.2.840.113635.100.6.1.14"
            ),  # Apple Developer ID Installer
            ObjectIdentifier("1.2.840.113635.100.4.13"),  # Apple Package Signing
            ObjectIdentifier("1.2.840.113635.100.6.1.14"),  # Apple Extension Signing
        ]

        key_usage = x509.KeyUsage(
            digital_signature=True,
            key_encipherment=False,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False,
            key_cert_sign=False,
            crl_sign=False,
        )

        builder = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(self.ca_cert.subject)
            .public_key(apple_private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.ExtendedKeyUsage(eku_list),
                critical=True,
            )
            .add_extension(
                key_usage,
                critical=True,
            )
        )

        # Sign the certificate with the CA private key
        apple_certificate = builder.sign(
            self.ca_key, hashes.SHA256(), default_backend()
        )

        # Save the new certificate to a file
        with open(cert_path, "wb") as f:
            f.write(apple_certificate.public_bytes(serialization.Encoding.PEM))

        # Save the private key
        with open(key_path, "wb") as f:
            f.write(
                apple_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        return cert_path, key_path

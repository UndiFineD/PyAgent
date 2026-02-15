
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

"""
DNS Takeover Signatures
Source: 0xSojalSec-can-i-take-over-dns (https://github.com/indianajson/can-i-take-over-dns)
"""

DNS_TAKEOVER_SIGNATURES = {
    "000Domains": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["ns1.000domains.com", "ns2.000domains.com", "fwns1.000domains.com", "fwns2.000domains.com"]
    },
    "AWS Route 53": {
        "status": "Not Vulnerable",
        "fingerprints": ["awsdns-"]
    },
    "Azure (Microsoft)": {
        "status": "Edge Case",
        "fingerprints": ["azure-dns.com", "azure-dns.net", "azure-dns.org", "azure-dns.info"]
    },
    "Bizland": {
        "status": "Vulnerable",
        "fingerprints": ["ns1.bizland.com", "ns2.bizland.com", "clickme.click2site.com", "clickme2.click2site.com"]
    },
    "Cloudflare": {
        "status": "Edge Case",
        "fingerprints": ["ns.cloudflare.com"]
    },
    "Digital Ocean": {
        "status": "Vulnerable",
        "fingerprints": ["ns1.digitalocean.com", "ns2.digitalocean.com", "ns3.digitalocean.com"]
    },
    "DNSMadeEasy": {
        "status": "Vulnerable",
        "fingerprints": ["dnsmadeeasy.com"]
    },
    "DNSimple": {
        "status": "Vulnerable",
        "fingerprints": ["ns1.dnsimple.com", "ns2.dnsimple.com", "ns3.dnsimple.com", "ns4.dnsimple.com"]
    },
    "Domain.com": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["ns1.domain.com", "ns2.domain.com"]
    },
    "DomainPeople": {
        "status": "Not Vulnerable",
        "fingerprints": ["ns1.domainpeople.com", "ns2.domainpeople.com"]
    },
    "Dotster": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["ns1.dotster.com", "ns2.dotster.com", "ns1.nameresolve.com", "ns2.nameresolve.com"]
    },
    "EasyDNS": {
        "status": "Vulnerable",
        "fingerprints": ["dns1.easydns.com", "dns2.easydns.net", "dns3.easydns.org", "dns4.easydns.info"]
    },
    "Gandi.net": {
        "status": "Not Vulnerable",
        "fingerprints": ["dns.gandi.net"]
    },
    "Google Cloud": {
        "status": "Vulnerable",
        "fingerprints": ["googledomains.com"]
    },
    "Hostinger": {
        "status": "Not Vulnerable",
        "fingerprints": ["ns1.hostinger.com", "ns2.hostinger.com"]
    },
    "Hover": {
        "status": "Not Vulnerable",
        "fingerprints": ["ns1.hover.com", "ns2.hover.com"]
    },
    "Hurricane Electric": {
        "status": "Vulnerable",
        "fingerprints": ["he.net"]
    },
    "Linode": {
        "status": "Vulnerable",
        "fingerprints": ["ns1.linode.com", "ns2.linode.com"]
    },
    "MediaTemple": {
        "status": "Not Vulnerable",
        "fingerprints": ["ns1.mediatemple.net", "ns2.mediatemple.net"]
    },
    "MyDomain": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["ns1.mydomain.com", "ns2.mydomain.com"]
    },
    "Name.com": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["name.com"]
    },
    "Namecheap": {
        "status": "Not Vulnerable",
        "fingerprints": ["namecheaphosting.com", "registrar-servers.com"]
    },
    "Network Solutions": {
        "status": "Not Vulnerable",
        "fingerprints": ["worldnic.com"]
    },
    "NS1": {
        "status": "Vulnerable",
        "fingerprints": ["nsone.net"]
    },
    "TierraNet": {
        "status": "Vulnerable",
        "fingerprints": ["ns1.domaindiscover.com", "ns2.domaindiscover.com"]
    },
    "Reg.ru": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["ns1.reg.ru", "ns2.reg.ru"]
    },
    "UltraDNS": {
        "status": "Not Vulnerable",
        "fingerprints": ["ultradns.com"]
    },
    "Yahoo Small Business": {
        "status": "Vulnerable (w/ purchase)",
        "fingerprints": ["yns1.yahoo.com", "yns2.yahoo.com"]
    }
}

PRIVATE_DNS_SIGNATURES = {
    "Activision": "activision.com",
    "Adobe": "adobe.com",
    "Apple": "apple.com",
    "Automattic": "automattic.com",
    "Capital One": "capitalone.com",
    "Disney": ["twdcns.com", "twdcns.info", "twdcns.co.uk"],
    "Google": "google.com",
    "Lowe's": "lowes.com",
    "T-Mobile": ["tmobileus.com", "tmobileus.net"]
}

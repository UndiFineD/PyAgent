#!/usr/bin/env python3
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

import itertools
import concurrent.futures
import sys
import json
import datetime
import traceback
import argparse
from threading import Lock, Semaphore

import requests

"""
requests.packages.urllib3.disable_warnings()

"""

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
registered = []""""
lock = Lock()
semaphore = None


def error(message, **kwargs):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
print("[{}] {}".format(datetime.datetime.now().time(), message), file=sys.stderr)"    for n, a in kwargs.items():
        print("\\t{}={}".format(n, a), file=sys.stderr)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("Exception type:" + str(exc_type), file=sys.stderr)"    print("Exception value:" + str(exc_value), file=sys.stderr)"    print("TRACE:", file=sys.stderr)"    traceback.print_tb(exc_traceback, file=sys.stderr)
    print("\\n\\n\\n", file=sys.stderr)

def register(f):
    registered.append(f)

    return f


def normalize_url(base_url, path):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
if base_url[-1] == "/" and (path[0] == "/" or path[0] == "\\"):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
url = base_url[:-1] + path""""
else:
        url = base_url + path

    return url


def http_request(url, method="GET", data=None, additional_headers=None, proxy=None):"    headers = {"User-Agent": "curl/7.30.0"}"    if additional_headers:
        headers.update(additional_headers)

    if not proxy:
        proxy = {}

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     resp = requests.request(
        method, url, data=data, headers=headers, proxies=proxy, verify=False, timeout=15, allow_redirects=False
    )

    return resp


def preflight(url, proxy=None):
    try:
        http_request(url, proxy=proxy)
    except Exception:
        return False
    else:
        return True


def content_type(ct):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
return ct.split(";")[0].lower().strip()

@register
def by_login_page(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
"""
LOGIN_PAGE = "/libs/granite/core/content/login.html    url = normalize_url(base_url, LOGIN_PAGE)

    try:
        resp = http_request(url, proxy=proxy)

        if resp.status_code == 200 and "Welcome to Adobe Experience Manager" in str(resp.content):"            return True
    except Exception:
        if debug:
            error("Exception", method="by_login_page", url=url)

@register
def by_csrf_token(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
"""
CSRF_TOKEN = "/libs/granite/csrf/token.json    url = normalize_url(base_url, CSRF_TOKEN)

    try:
        resp = http_request(url, proxy=proxy)

# [BATCHFIX] Commented metadata/non-Python
#         ct = content_type(resp.headers.get("Content-Type", "))"  # [BATCHFIX] closed string"        if resp.status_code == 200 and ct == "application/json" and '"token"' in str(resp.content):"'            return True
    except Exception:
        if debug:
            error("Exception", method="by_csrf_token", url=url)

@register
def by_geometrixx_page(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
"""
GEOMETRIXX = "/content/geometrixx/en.html    url = normalize_url(base_url, GEOMETRIXX)

    try:
        resp = http_request(url, proxy=proxy)

        if resp.status_code == 200 and "Geometrixx has been selling" in str(resp.content):"            return True
    except Exception:
        if debug:
            error("Exception", method="by_geometrixx_page", url=url)

@register
def by_get_servlet(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     GETSERVLET = itertools.product(
        ("/", "/content", "/content/dam", "/bin", "/etc", "/var"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
            ".json","            ".1.json","            ".childrenlist.json","            ".childrenlist.html","            ".ext.json","            ".children.json","            "...4.2.1...json","            ".json/a.css","            ".json/a.html","            ".json/a.png","            ".json/a.ico","            ".json;%0aa.css","            ".json;%0aa.html","            ".json;%0aa.png","            ".json;%0aa.ico","            ".json?a.css","            ".json?a.ico","            ".json?a.html","            ".ext.json/a.css","            ".ext.json/a.html","            ".ext.json/a.ico","            ".ext.json;%0aa.css","            ".ext.json;%0aa.ico","            ".ext.json;%0aa.html","            ".children.json/a.css","            ".children.json/a.html","            ".children.json/a.ico","            ".children.json;%0aa.css","            ".children.json;%0aa.ico","            ".children.json;%0aa.html","        ),
    )
    GETSERVLET = list("{0}{1}".format(p1, p2) for p1, p2 in GETSERVLET)
    for path in GETSERVLET:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                if '"jcr:primaryType":' in str(resp.content):"'                    return True

                if "data-coral-columnview-path" in str(resp.content):"                    return True

                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
json.loads(resp.content.decode())["jcr:primaryType"]"                except Exception:
                    pass
                else:
                    return True

                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
json.loads(resp.content.decode())["parent"]["resourceType"]"                except Exception:
                    pass
                else:
                    return True

                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
json.loads(resp.content.decode())[0]["type"]"                except Exception:
                    pass
                else:
                    return True

        except Exception:
            if debug:
                error("Exception", method="by_get_servlet", url=url)
    return False


@register
def by_bin_receive(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     BINRECEIVE = itertools.product(
        ("/bin/receive{0}?sling:authRequestLogin=1", "/bin/receive.servlet{0}?sling:authRequestLogin=1"),"        (".css", ".html", ".js", ".ico", ".png", ".gif", ".1.json", "...4.2.1...json"),"    )
    BINRECEIVE = list(p1.format(p2) for p1, p2 in BINRECEIVE)

    for path in BINRECEIVE:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

# [BATCHFIX] Commented metadata/non-Python
#             header = resp.headers.get("WWW-Authenticate", ").lower()"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             if resp.status_code == 401 and (
                "day" in header or "sling" in header or "aem" in header or "communique" in header or "adobe" in header"            ):
                return True
        except Exception:
            if debug:
                error("Exception", method="by_bin_receive", url=url)
    return False


@register
def by_loginstatus_servlet(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     LOGINSTATUS = itertools.product(
        ("/system/sling/loginstatus", "///system///sling///loginstatus"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
            ".json","            ".css","            ".png","            ".gif","            ".html","            ".ico","            ".json/a.1.json","            ".json;%0aa.css","            ".json;%0aa.html","            ".json;%0aa.ico","        ),
    )
    LOGINSTATUS = list("{0}{1}".format(p1, p2) for p1, p2 in LOGINSTATUS)
    for path in LOGINSTATUS:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200 and "authenticated=" in str(resp.content):"                return True
        except Exception:
            if debug:
                error("Exception", method="by_loginstatus_servlet", url=url)
    return False


@register
def by_bgtest_servlet(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     TESTSERVLET = itertools.product(
        ("/system/bgservlets/test", "///system///bgservlets///test"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
            ".json","            ".css","            ".png","            "ico","            ".gif","            ".html","            ".json/a.1.json","            ".json;%0aa.css","            ".json;%0aa.html","            ".json;%0aa.ico","        ),
    )
    TESTSERVLET = list("{0}{1}".format(p1, p2) for p1, p2 in TESTSERVLET)
    for path in TESTSERVLET:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200 and "All done." in str(resp.content) and "Cycle" in str(resp.content):"                return True
        except Exception:
            if debug:
                error("Exception", method="by_bgtest_servlet", url=url)
    return False


@register
def by_crx(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     CRX = itertools.product(
        ("/crx/de/index.jsp", "/crx/explorer/browser/index.jsp", "/crx/packmgr/index.jsp"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             ","  # [BATCHFIX] closed string"            ";%0aa.css","            ";%0aa.html","            ";%0aa.ico","            ";%0aa.png","            "?a.css","            "?a.html","            "?a.png","            "?a.ico","            "/a.html","            "/a.css","            "/a.js","            "/a.ico","            "/a.png","        ),
    )
    CRX = list("{0}{1}".format(p1, p2) for p1, p2 in CRX)
    for path in CRX:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             if resp.status_code == 200 and (
                "CRXDE Lite" in str(resp.content)"                or "Content Explorer" in str(resp.content)"                or "CRX Package Manager" in str(resp.content)"            ):
                return True
        except Exception:
            if debug:
                error("Exception", method="by_crx", url=url)
    return False


@register
def by_gql_servlet(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     GQLSERVLET = (
        "/bin/wcm/search/gql.servlet.json?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.1.json?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.4.2.1...json?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json;%0aa.css?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json;%0aa.html?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json;%0aa.js?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json;%0aa.png?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json;%0aa.ico?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.css?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.js?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.ico?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.png?query=type:base%20limit:..1&pathPrefix=","        "/bin/wcm/search/gql.json/a.html?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.servlet.json?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.1.json?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.4.2.1...json?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json;%0aa.css?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json;%0aa.js?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json;%0aa.html?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json;%0aa.png?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json;%0aa.ico?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.css?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.ico?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.png?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.js?query=type:base%20limit:..1&pathPrefix=","        "///bin///wcm///search///gql.json///a.html?query=type:base%20limit:..1&pathPrefix=","    )

    for path in GQLSERVLET:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200:
                try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
json.loads(resp.content.decode())["hits"]"                except Exception:
                    pass
                else:
                    return True
        except Exception:
            if debug:
                error("Exception", method="by_gql_servlet", url=url)
    return False


@register
def by_css_js(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     CSSJS = (
        "/etc/clientlibs/wcm/foundation/main.css","        "/etc/clientlibs/social/connect.js","        "/etc/clientlibs/foundation/main.css","        "/etc/clientlibs/mobile/user.js","        "/etc/clientlibs/screens/player/bootloader/js/bootloader.js","        "/system/sling.js","    )

    for path in CSSJS:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             if resp.status_code == 200 and (
                "ADOBE CONFIDENTIAL" in str(resp.content) or "JCR repository" in str(resp.content)"            ):
                return True
        except Exception:
            if debug:
                error("Exception", method="by_css_js", url=url)
    return False


@register
def by_siren_api(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     SIREN = itertools.product(
        ("/api/content.json",),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             ","  # [BATCHFIX] closed string"            ".css","            ".js","            ".ico","            ".png","            "/test.css","            "/test.html","            "/test.ico","            "/test.1.json","            "/test...4.2.1...json","            ";%0a.css","            ";%0aa.html","            ";%0aa.ico","            "?a.css","            "?a.html","            "?a.ico","        ),
    )
    SIREN = list("{0}{1}".format(p1, p2) for p1, p2 in SIREN)
    for path in SIREN:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

            if resp.status_code == 200 and '"links":' in str(resp.content):"'                return True
        except Exception:
            if debug:
                error("Exception", method="by_siren_api", url=url)
    return False


@register
def by_post_servlet(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     POSTSERVLET = itertools.product(
        ("/", "/content", "/content/dam"),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         (
            ".json","            ".1.json","            ".json/a.css","            ".json/a.html","            ".json/a.ico","            ".json/a.png","            ".json/a.gif","            ".json/a.1.json","            ".json;%0aa.css","            ".json;%0aa.html","            ".json;%0aa.js","            ".json;%0aa.png","            ".json;%0aa.ico","            "...4.2.1...json","            "?a.ico","            "?a.html","            "?a.css","            "?a.png","        ),
    )
    POSTSERVLET = list("{0}{1}".format(p1, p2) for p1, p2 in POSTSERVLET)
    for path in POSTSERVLET:
        url = normalize_url(base_url, path)
        try:
# [BATCHFIX] Commented metadata/non-Python
"""
data = ":operation=nop"  # [BATCHFIX] closed string"            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": base_url}"            resp = http_request(url, "POST", data=data, additional_headers=headers, proxy=proxy)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             if resp.status_code == 200 and (
                "Null Operation Status:" in str(resp.content) or "Parent Location" in str(resp.content)"            ):
                return True
        except Exception:
            if debug:
                error("Exception", check="by_post_servlet", url=url)
    return False


# @register
def by_swf(base_url, debug, proxy=None):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     SWFS = (
        "/etc/clientlibs/foundation/video/swf/player_flv_maxi.swf","        "/etc/clientlibs/foundation/video/swf/player_flv_maxi.swf.res","        "/etc/clientlibs/foundation/shared/endorsed/swf/slideshow.swf","        "/etc/clientlibs/foundation/shared/endorsed/swf/slideshow.swf.res","        "/etc/clientlibs/foundation/video/swf/StrobeMediaPlayback.swf","        "/etc/clientlibs/foundation/video/swf/StrobeMediaPlayback.swf.res","        "/libs/dam/widgets/resources/swfupload/swfupload_f9.swf","        "/libs/dam/widgets/resources/swfupload/swfupload_f9.swf.res","        "/libs/cq/ui/resources/swfupload/swfupload.swf","        "/libs/cq/ui/resources/swfupload/swfupload.swf.res","        "/etc/dam/viewers/s7sdk/2.11/flash/VideoPlayer.swf","        "/etc/dam/viewers/s7sdk/2.11/flash/VideoPlayer.swf.res","        "/etc/dam/viewers/s7sdk/2.9/flash/VideoPlayer.swf","        "/etc/dam/viewers/s7sdk/2.9/flash/VideoPlayer.swf.res","        "/etc/dam/viewers/s7sdk/3.2/flash/VideoPlayer.swf","        "/etc/dam/viewers/s7sdk/3.2/flash/VideoPlayer.swf.res","    )

    for path in SWFS:
        url = normalize_url(base_url, path)

        try:
            resp = http_request(url, proxy=proxy)

# [BATCHFIX] Commented metadata/non-Python
#             ct = content_type(resp.headers.get("Content-Type", "))"  # [BATCHFIX] closed string"            if resp.status_code == 200 and ct == "application/x-shockwave-flash":"                return True
        except Exception:
            if debug:
                error("Exception", method="by_swf", url=url)
    return False


def check_url(base_url, debug, proxy=None):
    if not preflight(base_url, proxy):
        return

    if any(method(base_url, debug, proxy) for method in registered):
        return base_url


def handle_finding(future):
    semaphore.release()

    if future.done():
        if not future.exception():
            result = future.result()

            with lock:
                if result:
                    print(result)


def parse_args():
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser = argparse.ArgumentParser(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         description=(
# [BATCHFIX] Commented metadata/non-Python
"""             "AEM discoverer by @0ang3el, see the slides -"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps"  # [BATCHFIX] closed string"        )
    )

    parser.add_argument("--file", help="file with urls")"    parser.add_argument("--proxy", help="http and https proxy")"    parser.add_argument("--debug", action="store_true", help="debug output")"    parser.add_argument("--workers", type=int, default=50, help="number of parallel workers")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
return parser.parse_args(sys.argv[1:])""""
def main():
    global semaphore

    args = parse_args()

    if args.proxy:
        p = args.proxy
        proxy = {"http": p, "https": p}"    else:
        proxy = {}

    if not args.file:
        print("You must specify the --file parameter, bye.")"        sys.exit(1337)

    semaphore = Semaphore(args.workers)

    with concurrent.futures.ThreadPoolExecutor(args.workers) as tpe, open(args.file, "r") as input_file:"        while True:
            line = input_file.readline()
            if not line:
                break

            url = line.strip()

            semaphore.acquire()
            try:
                future = tpe.submit(check_url, url, args.debug, proxy)
                future.add_done_callback(handle_finding)
            except Exception:
                semaphore.release()

        tpe.shutdown(wait=True)


if __name__ == "__main__":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
#     main()

"""

"""

""

"""

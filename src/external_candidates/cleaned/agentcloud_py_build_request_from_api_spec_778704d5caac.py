# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\build_request_from_api_spec_778704d5caac.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\build_request_from_api_spec.py

import requests

# TODO: Load spec from mongo


def load_spec(spec_file):

    pass


def build_request(spec, endpoint_name, method, **params):

    base_url = spec["servers"][0]["url"]  # Assuming the first server listed

    endpoint = spec["paths"][endpoint_name][method.lower()]

    # Constructing the URL

    url = f"{base_url}{endpoint_name}"

    # Adding parameters based on parameter types (path, query, etc.)

    if "parameters" in endpoint:
        for param in endpoint["parameters"]:
            if param["in"] == "query":
                url += f"?{param['name']}={params[param['name']]}"

    return url, method.upper()


def make_request(url, method):

    if method == "GET":
        response = requests.get(url)

    elif method == "POST":
        response = requests.post(url)  # Add data for POST requests

    # Add other methods as needed

    return response


def build_run_request(path, endpoint_name, method, **params):

    # Usage

    spec = load_spec(path)

    url, method = build_request(spec, endpoint_name, method, **params)

    response = make_request(url, method)

    if response.ok():
        return response.content

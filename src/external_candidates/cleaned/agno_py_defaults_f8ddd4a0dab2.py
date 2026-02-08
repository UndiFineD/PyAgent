# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\defaults_f8ddd4a0dab2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\defaults.py

# Don't import anything which may lead to circular imports


def get_default_ns_name(app_name: str) -> str:
    return "{}-ns".format(app_name)


def get_default_ctx_name(app_name: str) -> str:
    return "{}-ctx".format(app_name)


def get_default_sa_name(app_name: str) -> str:
    return "{}-sa".format(app_name)


def get_default_cr_name(app_name: str) -> str:
    return "{}-cr".format(app_name)


def get_default_crb_name(app_name: str) -> str:
    return "{}-crb".format(app_name)


def get_default_pod_name(app_name: str) -> str:
    return "{}-pod".format(app_name)


def get_default_container_name(app_name: str) -> str:
    return "{}-container".format(app_name)


def get_default_service_name(app_name: str) -> str:
    return "{}-svc".format(app_name)


def get_default_ingress_name(app_name: str) -> str:
    return "{}-ingress".format(app_name)


def get_default_deploy_name(app_name: str) -> str:
    return "{}-deploy".format(app_name)


def get_default_configmap_name(app_name: str) -> str:
    return "{}-cm".format(app_name)


def get_default_secret_name(app_name: str) -> str:
    return "{}-secret".format(app_name)


def get_default_volume_name(app_name: str) -> str:
    return "{}-volume".format(app_name)


def get_default_pvc_name(app_name: str) -> str:
    return "{}-pvc".format(app_name)

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-HomeDockOS\pymodules\hd_UIDashboard.py
"""
hd_UIDashboard.py
Copyright © 2023-2025 Banshee, All Rights Reserved
https://www.banshee.pro
"""

from flask import g, render_template, session
from flask_login import login_required
from pymodules.hd_FunctionsConfig import read_config
from pymodules.hd_FunctionsGlobals import current_year, version, version_hash
from pymodules.hd_FunctionsMain import (
    actual_uptime,
    get_active_containers,
    get_active_network_interface,
    get_configured_external_drives,
    get_cpu_cores,
    get_cpu_max_speed,
    get_server_uptime,
    get_total_containers,
    get_total_disk,
    get_total_external_disk,
    get_total_ram,
)
from pymodules.hd_FunctionsNetwork import internet_ip, local_ip
from pymodules.hd_LogCPUTemp import get_cpu_temp
from pymodules.hd_LogCPUUsage import get_cpu_usage
from pymodules.hd_LogDiskUsage import get_disk_usage
from pymodules.hd_LogExternalDiskUsage import get_external_disk_usage
from pymodules.hd_LogNetworkUsage import get_download_data, get_upload_data
from pymodules.hd_LogRAMUsage import get_ram_usage


@login_required
def dashboard():
    config = read_config()
    user_name = config["user_name"]
    interface_name = get_active_network_interface()
    external_disk_device = get_configured_external_drives()
    external_path = external_disk_device[0] if external_disk_device else None
    selected_theme = config["selected_theme"]
    selected_back = config["selected_back"]

    return render_template(
        "dashboard.html",
        user_name=user_name,
        local_ip=local_ip,
        internet_ip=internet_ip,
        version=version,
        version_hash=version_hash,
        n_total_containers=get_total_containers(),
        n_active_containers=get_active_containers(),
        uptime_data=actual_uptime(),
        start_time=get_server_uptime(),
        cpu_temp=get_cpu_temp(),
        cpu_usage=get_cpu_usage(),
        cpu_cores=get_cpu_cores(),
        ram_usage=get_ram_usage(),
        total_ram=get_total_ram(),
        year=current_year,
        get_cpu_max_speed=get_cpu_max_speed(),
        interface_name=interface_name,
        vdownload=get_download_data(interface_name)["received"],
        vupload=get_upload_data(interface_name)["sent"],
        hard_disk_usage=get_disk_usage(),
        hard_disk_total=get_total_disk(),
        selected_theme=selected_theme,
        selected_back=selected_back,
        external_disk_usage=get_external_disk_usage(),
        external_disk_total=get_total_external_disk(),
        external_default_disk=get_configured_external_drives(),
        external_path=external_path,
        nonce=g.get("nonce", ""),
    )

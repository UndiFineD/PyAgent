# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-HomeDockOS\pymodules\hd_UIControlHubUploadFile.py
"""
hd_UIControlHubUploadFile.py
Copyright © 2023-2025 Banshee, All Rights Reserved
https://www.banshee.pro
"""

import os

from flask import jsonify, request
from flask_login import login_required
from pymodules.hd_FunctionsGlobals import compose_upload_folder
from werkzeug.utils import secure_filename


@login_required
def upload_compose_file():
    if "compose_file" not in request.files:
        return jsonify(message="No file part in the request."), 400
    file = request.files["compose_file"]

    if file.filename == "":
        return jsonify(message="No selected file."), 400

    if not file.filename.endswith(".yml"):
        return jsonify(message="Invalid file type."), 400

    container_name = request.form.get("container_name")
    if not container_name:
        return jsonify(message="No container name specified."), 400

    filename = secure_filename(container_name + ".yml")
    file.save(os.path.join(compose_upload_folder, filename))

    return jsonify(message="Compose file uploaded successfully."), 200

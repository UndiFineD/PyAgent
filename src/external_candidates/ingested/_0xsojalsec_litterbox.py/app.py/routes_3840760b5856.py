# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LitterBox\app\routes.py
# app/routes.py
import datetime
import glob
import hashlib
import math
import mimetypes
import os
import shutil

import pefile
import psutil
from flask import jsonify, render_template, request
from oletools.olevba import VBA_Parser
from werkzeug.utils import secure_filename

from .analyzers.manager import AnalysisManager


def allowed_file(filename, config):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config["upload"]["allowed_extensions"]
    )


def save_uploaded_file(file, upload_folder):
    file_content = file.read()
    file.close()
    md5_hash = hashlib.md5(file_content).hexdigest()
    sha256_hash = hashlib.sha256(file_content).hexdigest()

    original_filename = secure_filename(file.filename)
    extension = os.path.splitext(original_filename)[1].lower()
    filename = f"{md5_hash}_{original_filename}"

    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    with open(filepath, "wb") as f:
        f.write(file_content)

    file_info = {
        "original_name": original_filename,
        "md5": md5_hash,
        "sha256": sha256_hash,
        "size": len(file_content),
        "extension": extension,
        "mime_type": mimetypes.guess_type(original_filename)[0]
        or "application/octet-stream",
        "upload_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entropy": calculate_entropy(file_content),
    }

    # Add specific file type information for PE files
    if extension in [".exe", ".dll", ".sys"]:
        file_info.update(get_pe_info(filepath))

    # Add specific file type information for Office documents
    if extension in [".docx", ".xlsx", ".doc", ".xls", ".xlsm", ".docm"]:
        office_result = get_office_info(filepath)
        if "error" in office_result:
            print(f"Warning: {office_result['error']}")
        file_info.update(office_result)

    return file_info


def calculate_entropy(data):
    """Calculate Shannon entropy of data"""
    if len(data) == 0:
        return 0

    # Convert to bytes if not already
    if isinstance(data, str):
        data = data.encode()

    # Count byte frequencies
    byte_counts = {}
    for byte in data:
        byte_counts[byte] = byte_counts.get(byte, 0) + 1

    # Calculate entropy
    entropy = 0
    for count in byte_counts.values():
        p_x = count / len(data)
        entropy += -p_x * math.log2(p_x)

    return round(entropy, 2)


def get_pe_info(filepath):
    """Get PE file information"""
    try:
        pe = pefile.PE(filepath)
        info = {
            "file_type": (
                "PE32+ executable"
                if pe.PE_TYPE == pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS
                else "PE32 executable"
            ),
            "machine_type": pefile.MACHINE_TYPE[pe.FILE_HEADER.Machine].replace(
                "IMAGE_FILE_MACHINE_", ""
            ),
            "compile_time": datetime.datetime.fromtimestamp(
                pe.FILE_HEADER.TimeDateStamp
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "subsystem": pefile.SUBSYSTEM_TYPE[pe.OPTIONAL_HEADER.Subsystem].replace(
                "IMAGE_SUBSYSTEM_", ""
            ),
            "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "sections": [
                section.Name.decode().rstrip("\x00") for section in pe.sections
            ],
            "imports": list(
                set(
                    entry.dll.decode()
                    for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", [])
                )
            ),
        }
        pe.close()
        return {"pe_info": info}
    except Exception as e:
        print(f"Error analyzing PE file: {e}")
        return {"pe_info": None}


def get_office_info(filepath):
    """Get Office document information"""
    try:
        vbaparser = VBA_Parser(filepath)
        info = {
            "file_type": "Microsoft Office Document",
            "has_macros": vbaparser.detect_vba_macros(),
            "macro_info": (
                vbaparser.analyze_macros() if vbaparser.detect_vba_macros() else None
            ),
        }
        vbaparser.close()  # Release the VBA Parser resource
        return {"office_info": info}
    except Exception as e:
        print(f"Error analyzing Office file: {e}")
        return {"office_info": None}


def find_file_by_hash(file_hash, upload_folder):
    for filename in os.listdir(upload_folder):
        if filename.startswith(file_hash):
            return os.path.join(upload_folder, filename)
    return None


def check_tool(tool_path):
    """Check if a tool is accessible and presumably executable."""
    return os.path.isfile(tool_path) and os.access(tool_path, os.X_OK)


def validate_pid(pid):
    """
    Validate if a PID exists and is accessible.

    Args:
        pid (int): Process ID to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        pid = int(pid)
        if pid <= 0:
            return False, "Invalid PID: must be a positive integer"

        # Check if process exists
        if not psutil.pid_exists(pid):
            return False, f"Process with PID {pid} does not exist"

        # Try to get process info to check accessibility
        try:
            process = psutil.Process(pid)
            process.name()  # Try to access process name to verify permissions
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return False, f"Cannot access process {pid}: {str(e)}"

        return True, None

    except ValueError:
        return False, "Invalid PID: must be a number"
    except Exception as e:
        return False, f"Error validating PID: {str(e)}"


def register_routes(app):
    analysis_manager = AnalysisManager(app.config)

    @app.route("/")
    def index():
        return render_template("upload.html")

    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename, app.config):
            try:
                file_info = save_uploaded_file(
                    file, app.config["upload"]["upload_folder"]
                )
                return (
                    jsonify(
                        {
                            "message": "File uploaded successfully",
                            "file_info": file_info,
                        }
                    ),
                    200,
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        return jsonify({"error": "File type not allowed"}), 400

    @app.route("/validate/<pid>", methods=["POST"])
    def validate_process(pid):
        """Endpoint just for PID validation"""
        is_valid, error_msg = validate_pid(pid)
        if not is_valid:
            return jsonify({"error": error_msg}), 404
        return jsonify({"status": "valid"}), 200

    @app.route("/analyze/<analysis_type>/<target>", methods=["GET", "POST"])
    def analyze_file(analysis_type, target):
        try:
            is_pid = False
            file_path = None

            # Check if this is a PID-based analysis
            if analysis_type == "dynamic" and target.isdigit():
                is_pid = True
                # Validate PID before proceeding
                is_valid, error_msg = validate_pid(target)
                if not is_valid:
                    return jsonify({"error": error_msg}), 404
            else:
                # Look for file as before
                file_path = find_file_by_hash(
                    target, app.config["upload"]["upload_folder"]
                )
                if not file_path:
                    return jsonify({"error": "File not found"}), 404
            if request.method == "GET":
                return render_template(
                    "results.html", analysis_type=analysis_type, file_hash=target
                )

            # POST request - perform analysis
            if analysis_type == "static":
                if is_pid:
                    return (
                        jsonify({"error": "Cannot perform static analysis on PID"}),
                        400,
                    )
                results = analysis_manager.run_static_analysis(file_path)
            elif analysis_type == "dynamic":
                target_for_analysis = target if is_pid else file_path
                results = analysis_manager.run_dynamic_analysis(
                    target_for_analysis, is_pid
                )
            else:
                return jsonify({"error": "Invalid analysis type"}), 400

            return jsonify({"status": "success", "results": results})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/cleanup", methods=["POST"])
    def cleanup():
        try:
            results = {"uploads_cleaned": 0, "analysis_cleaned": 0, "errors": []}

            # Clean uploads folder
            upload_folder = app.config["upload"]["upload_folder"]
            if os.path.exists(upload_folder):
                try:
                    files = os.listdir(upload_folder)
                    for f in files:
                        file_path = os.path.join(upload_folder, f)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                                results["uploads_cleaned"] += 1
                        except Exception as e:
                            results["errors"].append(f"Error deleting {f}: {str(e)}")
                except Exception as e:
                    results["errors"].append(
                        f"Error accessing uploads folder: {str(e)}"
                    )

            # Clean analysis folders
            analysis_path = os.path.join(".", "Scanners", "PE-Sieve", "Analysis")
            if os.path.exists(analysis_path):
                try:
                    # Find all process_* folders
                    process_folders = glob.glob(
                        os.path.join(analysis_path, "process_*")
                    )
                    for folder in process_folders:
                        try:
                            shutil.rmtree(folder)
                            results["analysis_cleaned"] += 1
                        except Exception as e:
                            results["errors"].append(
                                f"Error deleting {folder}: {str(e)}"
                            )
                except Exception as e:
                    results["errors"].append(
                        f"Error accessing analysis folder: {str(e)}"
                    )

            # Determine status based on whether there were any errors
            status = "warning" if results["errors"] else "success"
            message = (
                "Cleanup completed with some errors"
                if results["errors"]
                else "Cleanup completed successfully"
            )

            return jsonify(
                {"status": status, "message": message, "details": results}
            ), (
                200 if status == "success" else 207
            )  # 207 Multi-Status for partial success

        except Exception as e:
            return (
                jsonify(
                    {"status": "error", "message": "Cleanup failed", "error": str(e)}
                ),
                500,
            )

    @app.route("/health", methods=["GET"])
    def health_check():
        try:
            # Get configurations
            config = app.config
            upload_config = config.get("upload", {})
            analysis_config = config.get("analysis", {})

            # We'll gather any health issues in a list
            issues = []

            # Check upload folder accessibility
            upload_folder = upload_config.get("upload_folder")

            # Check both upload and temp folders
            folders_to_check = {
                "upload_folder": upload_folder,
            }

            for folder_name, folder_path in folders_to_check.items():
                if not folder_path:
                    issues.append(f"{folder_name} path is not configured")
                elif not os.path.isdir(folder_path):
                    issues.append(f"{folder_name} does not exist: {folder_path}")
                elif not os.access(folder_path, os.W_OK):
                    issues.append(f"{folder_name} is not writable: {folder_path}")

            # Function to check tool configuration and availability
            def check_analysis_tool(section, tool_name):
                tool_config = section.get(tool_name, {})
                if tool_config.get("enabled", False):
                    tool_path = tool_config.get("tool_path")
                    if not tool_path:
                        issues.append(f"{tool_name}: tool path not configured")
                    elif not os.path.isfile(tool_path):
                        issues.append(f"{tool_name}: tool not found at {tool_path}")
                    elif not os.access(tool_path, os.X_OK):
                        issues.append(
                            f"{tool_name}: tool not executable at {tool_path}"
                        )

                    # Check rules file if applicable
                    rules_path = tool_config.get("rules_path")
                    if rules_path and not os.path.isfile(rules_path):
                        issues.append(f"{tool_name}: rules not found at {rules_path}")

            # Check static analysis tools
            static_config = analysis_config.get("static", {})
            for tool in ["yara", "threatcheck"]:
                check_analysis_tool(static_config, tool)

            # Check dynamic analysis tools
            dynamic_config = analysis_config.get("dynamic", {})
            for tool in ["yara", "pe_sieve", "moneta", "patriot", "hsb"]:
                check_analysis_tool(dynamic_config, tool)

            # Determine overall status
            status = "ok" if not issues else "degraded"
            http_code = 200 if status == "ok" else 503

            health_status = {
                "status": status,
                "timestamp": datetime.datetime.now().isoformat(),
                "upload_folder_accessible": (
                    os.path.isdir(upload_folder) and os.access(upload_folder, os.W_OK)
                    if upload_folder
                    else False
                ),
                "issues": issues,
                "configuration": {
                    "static_analysis": {
                        tool: static_config.get(tool, {}).get("enabled", False)
                        for tool in ["yara", "threatcheck"]
                    },
                    "dynamic_analysis": {
                        tool: dynamic_config.get(tool, {}).get("enabled", False)
                        for tool in ["yara", "pe_sieve", "moneta"]
                    },
                },
            }

            return jsonify(health_status), http_code

        except Exception as e:
            return (
                jsonify(
                    {
                        "status": "error",
                        "timestamp": datetime.datetime.now().isoformat(),
                        "issues": [str(e)],
                    }
                ),
                500,
            )

    return app

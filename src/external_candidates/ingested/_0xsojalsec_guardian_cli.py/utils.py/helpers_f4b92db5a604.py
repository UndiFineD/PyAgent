# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\utils\helpers.py
"""
Common utility functions for Guardian
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_config(config_path: str = "config/guardian.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        return {}


def save_json(data: Any, filepath: Path):
    """Save data as JSON"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: Path) -> Any:
    """Load JSON file"""
    with open(filepath, "r") as f:
        return json.load(f)


def is_valid_domain(domain: str) -> bool:
    """Validate domain name format"""
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


def is_valid_ip(ip: str) -> bool:
    """Validate IP address format"""
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(pattern, ip))


def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r"^https?://(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|(?:[0-9]{1,3}\.){3}[0-9]{1,3})(?::[0-9]{1,5})?(?:/.*)?$"
    return bool(re.match(pattern, url))


def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL"""
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        return parsed.hostname or parsed.netloc
    except:
        return None


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for reports"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe"""
    # Remove/replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(". ")
    # Limit length
    return filename[:200]


def parse_severity(severity: str) -> int:
    """Convert severity string to numeric value for sorting"""
    severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
    return severity_map.get(severity.lower(), 0)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def ensure_dir(path: Path):
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)


def color_severity(severity: str) -> str:
    """Return rich markup color for severity"""
    colors = {
        "critical": "bold red",
        "high": "red",
        "medium": "yellow",
        "low": "blue",
        "info": "cyan",
    }
    return colors.get(severity.lower(), "white")

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\evidences.py\apps_7e0d3d00473d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\evidences\apps.py

from django.apps import AppConfig


class EvidencesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "evidences"

    def ready(self):
        import evidences.signals

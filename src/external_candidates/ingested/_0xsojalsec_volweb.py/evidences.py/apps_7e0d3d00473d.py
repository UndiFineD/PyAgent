# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\evidences\apps.py
from django.apps import AppConfig


class EvidencesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "evidences"

    def ready(self):
        import evidences.signals

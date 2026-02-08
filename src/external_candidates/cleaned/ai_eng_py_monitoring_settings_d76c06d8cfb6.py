# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\definition.py\monitoring_settings_d76c06d8cfb6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\definition\monitoring_settings.py

from feathr.definition.materialization_settings import MaterializationSettings

# it's completely the same as MaterializationSettings. But we renamed it to improve usability.

# In the future, we may want to rely a separate system other than MaterializationSettings to generate stats.

class MonitoringSettings(MaterializationSettings):

    """Settings about monitoring features."""


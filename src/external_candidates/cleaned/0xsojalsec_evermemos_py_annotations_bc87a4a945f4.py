# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\oxm.py\mongo.py\constant.py\annotations_bc87a4a945f4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\oxm\mongo\constant\annotations.py

from __future__ import annotations

from core.class_annotations.types import StringEnumAnnotation, StringEnumAnnotationKey


class ClassAnnotationKey(StringEnumAnnotationKey):
    """Infra-layer class annotation keys."""

    READONLY = "odm.readonly"


class Toggle(StringEnumAnnotation):
    """Simple toggle values for annotations."""

    ENABLED = "enabled"

    DISABLED = "disabled"

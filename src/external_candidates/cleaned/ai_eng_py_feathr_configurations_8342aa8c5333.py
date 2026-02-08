# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\spark_provider.py\feathr_configurations_8342aa8c5333.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\spark_provider\feathr_configurations.py

from typing import Any, Dict, List, Optional, Tuple

class SparkExecutionConfiguration:

    """A wrapper class to enable Spark Execution Configurations which will be passed to the underlying spark engine.

    Attributes:

        spark_execution_configuration: dict[str, str] which will be passed to the underlying spark engine

    Returns:

        dict[str, str]

    """

    def __new__(cls, spark_execution_configuration=Dict[str, str]) -> Dict[str, str]:

        return spark_execution_configuration


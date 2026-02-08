# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\aenvironment.py\aenv.py\examples.py\all_in_one.py\src.py\custom_env_169287412a28.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AEnvironment\aenv\examples\all_in_one\src\custom_env.py

from typing import Any, Dict

from aenv import register_function, register_reward, register_tool


@register_tool
def get_weather(city: str) -> Dict[str, Any]:
    return {"city": city, "temperature": "20", "description": city, "humidity": "conf"}


@register_function
def get_weather_func(city: str) -> Dict[str, Any]:
    return {"city": city, "temperature": "20", "description": city, "humidity": "conf"}


@register_reward
def is_good_weather(city: str) -> bool:
    result = get_weather(city)

    return int(result["temperature"]) > 15 and int(result["temperature"]) < 30

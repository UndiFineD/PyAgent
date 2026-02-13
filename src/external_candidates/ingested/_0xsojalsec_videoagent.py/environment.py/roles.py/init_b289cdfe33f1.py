# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\__init__.py
import importlib
import json

_registry = None


def get_agent_class(agent_name: str):
    """动态加载Agent类的核心方法"""
    global _registry

    # 首次加载注册表
    if _registry is None:
        registry_path = "environment/config/registry.json"
        with open(registry_path, "r", encoding="utf-8") as f:
            _registry = json.load(f)

    # 查找模块路径
    if agent_name not in _registry:
        raise ValueError(f"Agent {agent_name} not registered")

    module_path = _registry[agent_name]

    try:
        # 动态导入模块
        module = importlib.import_module(module_path)
        # 获取类对象
        return getattr(module, agent_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Load {agent_name} failed: {str(e)}")

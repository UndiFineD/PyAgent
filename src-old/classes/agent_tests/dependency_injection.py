#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.dependency_injection import *  # type: ignore
except Exception:

    class DependencyInjector:
        pass


__all__ = ["DependencyInjector"]

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\database\cache_clearing.py
from typing import Sequence, Type

from ovo.core.database.base_db import DBEngine, T
from ovo.core.database.models import Base

CLEAR_FUNCTIONS = {}


def clear_when_modified(*models):
    assert models, "At least one model must be provided"
    # NOTE this can sometimes fail locally due to live reload, restarting the app will solve the issue
    assert issubclass(models[0], Base), (
        f"Expected model, got {type(models[0])} - usage: clear_when_modified(Project, Design) - do not wrap in list"
    )

    def decorator(func):
        CLEAR_FUNCTIONS[func.__name__] = (func, models)
        return func

    return decorator


class CacheClearingEngine(DBEngine):
    def save(self, obj: Base):
        if isinstance(obj, list):
            raise ValueError("Use save_all() for saving multiple objects, got list in save()")
        self._clear_all_cache(type(obj))

    def save_all(self, objs: Sequence[Base]):
        for type_ in set(type(obj) for obj in objs):
            self._clear_all_cache(type_)

    def remove(self, model: Type[T], *id_args, **kwargs):
        self._clear_all_cache(model)

    def save_value(self, model: Type[T], column: str, value, **kwargs):
        self._clear_all_cache(model)

    def _clear_all_cache(self, model_to_clear: Type[T]):
        for func_name, (func, models) in CLEAR_FUNCTIONS.items():
            for model in models:
                if issubclass(model_to_clear, model):
                    if not hasattr(func, "clear"):
                        raise ValueError(
                            f"Incorrect decorator order: "
                            f"Use @clear_when_modified before @st.cache_data - missing clear method on {func}"
                        )
                    func.clear()

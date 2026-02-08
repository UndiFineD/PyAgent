# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\util\handler_spec.py
import inspect
from typing import Callable, get_type_hints

from aio_pika import Message
from pydantic import BaseModel

from ..schema.result import Result

MUST_PARAM_ORDER_NAMES = ["body", "message"]
MUST_PARAM_TYPES = {"message": Message}
MUST_PARAM_SUB_TYPES = {"body": BaseModel}


def check_handler_function_sanity(func: Callable) -> Result[None]:
    type_hints = get_type_hints(func)

    # Get function signature
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    for i, n in enumerate(MUST_PARAM_ORDER_NAMES):
        if params[i].name != n:
            return Result.reject(f"{i}th Parameter order mismatch: {params[i].name} != {n}")
    for k, v in MUST_PARAM_TYPES.items():
        if type_hints[k] is not v:
            return Result.reject(f"Parameter type mismatch {k}:{type_hints[k]} != {v}")

    for k, v in MUST_PARAM_SUB_TYPES.items():
        if not issubclass(type_hints[k], v):
            return Result.reject(f"Parameter sub type mismatch {k}:{type_hints[k]} is not subclass of {v}")
    return Result.resolve(None)


def get_handler_body_type(func: Callable) -> BaseModel | None:
    type_hints = get_type_hints(func)
    return type_hints["body"]

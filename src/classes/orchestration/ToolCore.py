import inspect
from typing import Dict, List, Any, Callable, Optional
from pydantic import BaseModel

class ToolMetadata(BaseModel):
    """Metadata for a registered tool."""
    name: str
    description: str
    parameters: Dict[str, Any]
    owner: str # Name of the agent providing this tool
    category: str = "general"

class ToolCore:
    """
    Pure logic for tool registration and invocation.
    Handles parameter introspection and argument filtering.
    """

    def extract_metadata(self, owner_name: str, func: Callable, category: str) -> ToolMetadata:
        """Extracts ToolMetadata from a function signature."""
        name: str = func.__name__
        doc: str = func.__doc__ or "No description provided."
        
        # Simple parameter extraction
        sig = inspect.signature(func)
        params: Dict[str, str] = {}
        for p_name, param in sig.parameters.items():
            if p_name == 'self': continue # Skip self
            params[p_name] = str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
            
        return ToolMetadata(
            name=name,
            description=doc.split('\n')[0].strip(),
            parameters=params,
            owner=owner_name,
            category=category
        )

    def filter_arguments(self, func: Callable, args_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Filters input dictionary to only include keys supported by the function."""
        sig = inspect.signature(func)
        has_kwargs: bool = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        
        if has_kwargs:
            return args_dict
            
        return {
            k: v for k, v in args_dict.items()
            if k in sig.parameters
        }

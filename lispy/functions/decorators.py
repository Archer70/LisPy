"""
Decorators for LisPy function registration.
Provides clean, declarative way to register functions and documentation.
"""

from typing import Any, Callable, Dict, Optional

# Global registries that decorators populate
_lispy_functions: Dict[str, Callable] = {}
_lispy_documentation: Dict[str, Callable] = {}
_web_unsafe_functions: Dict[str, str] = {}


def lispy_function(name: str, web_safe: bool = True, reason: Optional[str] = None):
    """
    Decorator to register a Python function as a LisPy built-in function.

    Args:
        name: The LisPy function name (e.g., "my-function", "+", "is-nil?")
        web_safe: Whether this function is safe for web environments (default: True)
        reason: If web_safe=False, explanation of why it's unsafe

    Example:
        @lispy_function("+")
        def builtin_add(args, env):
            # Implementation

        @lispy_function("http-get", web_safe=False, reason="Network access")
        def builtin_http_get(args, env):
            # Implementation
    """

    def decorator(func: Callable) -> Callable:
        # Register the function
        _lispy_functions[name] = func

        # Register web safety information
        if not web_safe:
            if not reason:
                raise ValueError(
                    f"web_safe=False requires a reason for function '{name}'"
                )
            _web_unsafe_functions[name] = reason

        # Store metadata on the function itself for introspection
        func._lispy_name = name
        func._lispy_web_safe = web_safe
        func._lispy_unsafe_reason = reason if not web_safe else None

        return func

    return decorator


def lispy_documentation(name: str):
    """
    Decorator to register documentation for a LisPy function.

    Args:
        name: The LisPy function name this documentation is for

    Example:
        @lispy_documentation("+")
        def documentation_add() -> str:
            return "Function: +\\nDescription: Adds numbers..."
    """

    def decorator(func: Callable) -> Callable:
        # Register the documentation function
        _lispy_documentation[name] = func

        # Store metadata on the function itself
        func._lispy_doc_for = name

        return func

    return decorator


def get_registered_functions() -> Dict[str, Callable]:
    """Get all functions registered via @lispy_function decorator."""
    return _lispy_functions.copy()


def get_registered_documentation() -> Dict[str, Callable]:
    """Get all documentation registered via @lispy_documentation decorator."""
    return _lispy_documentation.copy()


def get_web_unsafe_functions() -> Dict[str, str]:
    """Get all functions marked as web-unsafe with their reasons."""
    return _web_unsafe_functions.copy()


def clear_registries():
    """Clear all registries. Useful for testing."""
    global _lispy_functions, _lispy_documentation, _web_unsafe_functions
    _lispy_functions.clear()
    _lispy_documentation.clear()
    _web_unsafe_functions.clear()


def function_info(func: Callable) -> Dict[str, Any]:
    """Get LisPy metadata for a decorated function."""
    return {
        "lispy_name": getattr(func, "_lispy_name", None),
        "web_safe": getattr(func, "_lispy_web_safe", None),
        "unsafe_reason": getattr(func, "_lispy_unsafe_reason", None),
        "doc_for": getattr(func, "_lispy_doc_for", None),
    }

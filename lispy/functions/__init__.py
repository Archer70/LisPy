# lispy_project/lispy/functions/__init__.py

from ..environment import Environment
from .function_registry import get_function_registry

# Import documentation system
from .doc import register_documentation
from ..special_forms import setup_special_form_documentation

# Import all subpackages to trigger decorator registration
# This ensures that all @lispy_function decorated functions get registered
from . import math
from . import logical  
from . import collection
from . import list
from . import map
from . import type_check
from . import string
from . import typing
from . import io
from . import promises
from . import json
from . import http
from . import web
from . import bdd_assertions

# Legacy special forms lists (to be migrated to decorators)
WEB_UNSAFE_SPECIAL_FORMS = {
    'import': 'Module loading with filesystem access - can load arbitrary modules',
    'export': 'Module export functionality - not needed without import',
    'throw': 'Exception throwing mechanism - could be misused for flow control attacks'
}

WEB_UNSAFE_BDD_FORMS = {
    'describe': 'BDD testing framework - not needed in production',
    'it': 'BDD test definition - not needed in production',
    'given': 'BDD test setup - not needed in production',
    'then': 'BDD test assertion - not needed in production',
    'action': 'BDD test action - not needed in production',
    'assert-raises?': 'BDD exception testing - not needed in production'
}


def create_global_env() -> Environment:
    """Creates and returns the global environment with built-in functions."""
    env = Environment()
    
    # Get the function registry and register all discovered functions
    registry = get_function_registry()
    registry.register_functions_in_environment(env)
    
    # Set up documentation registry
    setup_documentation_registry()
    
    return env


def create_web_safe_env() -> Environment:
    """
    Creates a web-safe environment excluding potentially dangerous functions.
    
    This environment is suitable for server-side execution where security is
    critical. It excludes functions that could:
    - Read or write files from the filesystem
    - Access interactive input/output
    - Load arbitrary modules
    - Potentially interfere with server operations
    
    Returns:
        Environment: A new environment with only safe functions
    """
    # Start with a full global environment
    env = create_global_env()

    # Store web-safe special form handlers in the environment
    # This allows the evaluator to use different handlers for different environments
    from ..special_forms import web_safe_special_form_handlers
    env._special_form_handlers = web_safe_special_form_handlers

    # Get web-unsafe functions from the registry (decorator-based + legacy)
    registry = get_function_registry()
    web_unsafe_functions = registry.get_web_unsafe_functions()
    
    # Remove unsafe functions from the environment
    for func_name in web_unsafe_functions.keys():
        try:
            # Directly remove from environment's internal store
            if func_name in env.store:
                del env.store[func_name]
        except Exception:
            # Function might not exist in environment, that's okay
            pass

    return env


def get_web_unsafe_functions():
    """
    Returns a dictionary of functions excluded from web-safe environments.
    
    Returns:
        dict: Mapping of function names to reason for exclusion
    """
    # Get web-unsafe functions from decorator-based registry
    registry = get_function_registry()
    return registry.get_web_unsafe_functions()


def get_web_unsafe_special_forms():
    """
    Returns a dictionary of special forms excluded from web-safe environments.
    
    Returns:
        dict: Mapping of special form names to reason for exclusion
    """
    return WEB_UNSAFE_SPECIAL_FORMS.copy()


def get_web_unsafe_bdd_forms():
    """
    Returns a dictionary of BDD forms that might be excluded from web-safe environments.
    
    Returns:
        dict: Mapping of BDD form names to reason for exclusion
    """
    return WEB_UNSAFE_BDD_FORMS.copy()


def setup_documentation_registry():
    """Register all documentation functions with their corresponding function names."""
    # Get the function registry and register all discovered documentation
    registry = get_function_registry()
    registry.register_documentation(register_documentation)
    
    # Register special form documentation
    setup_special_form_documentation()


# Create a single global environment instance when the module is loaded.
global_env = create_global_env()

# Maintain backward compatibility by providing access to the registry
def get_discovered_functions():
    """Get all discovered functions for debugging/introspection."""
    return get_function_registry().get_discovered_functions()

__all__ = [
    "create_global_env",
    "create_web_safe_env", 
    "get_web_unsafe_functions",
    "get_web_unsafe_special_forms", 
    "get_web_unsafe_bdd_forms",
    "global_env",
    "get_discovered_functions",
]

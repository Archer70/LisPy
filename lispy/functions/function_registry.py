"""
Auto-discovery system for LisPy built-in functions.
Automatically scans function modules and registers them with their documentation.
Uses decorator-based registration for clean function discovery.
"""

import os
import importlib
from typing import Dict, Any, Tuple, Set
from ..environment import Environment


class FunctionDiscovery:
    """Handles discovery of functions in packages and modules."""
    
    def __init__(self):
        self.discovered_modules: Set[str] = set()
    
    def discover_in_package(self, package_path: str, package_name: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """
        Discover all functions in a package and its subpackages by importing modules
        to trigger decorator registration.
        
        Returns:
            Tuple of (functions_dict, documentation_dict, web_unsafe_dict)
        """
        # Import all modules in the package to trigger decorator registration
        self._import_all_modules(package_path, package_name)
        
        # Get decorator-registered functions
        return self._get_decorator_registered()
    
    def _import_all_modules(self, package_path: str, package_name: str):
        """Import all Python modules in a package to trigger decorator registration."""
        for item in os.listdir(package_path):
            item_path = os.path.join(package_path, item)
            
            if self._should_skip_item(item):
                continue
                
            if self._is_python_package(item_path):
                # Recursively import subpackages
                subpackage_name = f"{package_name}.{item}"
                self._import_all_modules(item_path, subpackage_name)
                
            elif self._is_python_module(item):
                # Import individual module to trigger decorators
                module_name = f"{package_name}.{item[:-3]}"  # Remove .py extension
                self._import_module(module_name)
    
    def _import_module(self, module_name: str):
        """Import a module to trigger decorator registration."""
        if module_name in self.discovered_modules:
            return
            
        try:
            importlib.import_module(module_name)
            self.discovered_modules.add(module_name)
        except ImportError as e:
            print(f"Warning: Could not import module {module_name}: {e}")
    
    def _get_decorator_registered(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """Get functions registered via decorators."""
        try:
            from .decorators import get_registered_functions, get_registered_documentation, get_web_unsafe_functions
            
            functions = get_registered_functions()
            documentation = get_registered_documentation()
            web_unsafe = get_web_unsafe_functions()
            
            return functions, documentation, web_unsafe
        except ImportError:
            # Decorators module not available yet
            return {}, {}, {}
    
    def _should_skip_item(self, item: str) -> bool:
        """Check if an item should be skipped during discovery."""
        return item == '__pycache__' or item.startswith('.') or item == 'decorators.py'
    
    def _is_python_package(self, path: str) -> bool:
        """Check if a path is a Python package."""
        return os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py'))
    
    def _is_python_module(self, item: str) -> bool:
        """Check if an item is a Python module."""
        return item.endswith('.py') and item != '__init__.py'


class FunctionRegistry:
    """Coordinates function discovery and handles registration."""
    
    def __init__(self):
        self.discovery = FunctionDiscovery()
        self.functions: Dict[str, Any] = {}
        self.documentation: Dict[str, Any] = {}
        self.web_unsafe: Dict[str, str] = {}
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure the registry has been initialized with discovered functions."""
        if not self._initialized:
            # Discover functions in the current package
            functions_package_path = os.path.dirname(__file__)
            self.functions, self.documentation, self.web_unsafe = self.discovery.discover_in_package(
                functions_package_path, 
                'lispy.functions'
            )
            self._initialized = True
    
    def register_functions_in_environment(self, env: Environment):
        """Register all discovered functions in the given environment."""
        self._ensure_initialized()
        for lispy_name, function in self.functions.items():
            env.define(lispy_name, function)
    
    def register_documentation(self, register_doc_function):
        """Register all discovered documentation."""
        self._ensure_initialized()
        for lispy_name, doc_func_or_string in self.documentation.items():
            register_doc_function(lispy_name, doc_func_or_string)
    
    def get_function_count(self) -> int:
        """Return the number of discovered functions."""
        self._ensure_initialized()
        return len(self.functions)
    
    def get_documentation_count(self) -> int:
        """Return the number of discovered documentation strings."""
        self._ensure_initialized()
        return len(self.documentation)
    
    def get_discovered_functions(self) -> dict:
        """Return the discovered functions for debugging."""
        self._ensure_initialized()
        return self.functions.copy()
    
    def get_web_unsafe_functions(self) -> dict:
        """Return functions marked as web-unsafe with their reasons."""
        self._ensure_initialized()
        return self.web_unsafe.copy()


# Global registry instance
_function_registry = None

def get_function_registry() -> FunctionRegistry:
    """Get or create the global function registry."""
    global _function_registry
    if _function_registry is None:
        _function_registry = FunctionRegistry()
    
    return _function_registry 
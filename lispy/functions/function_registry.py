"""
Auto-discovery system for LisPy built-in functions.
Automatically scans function modules and registers them with their documentation.
Supports both legacy pattern-based discovery and new decorator-based registration.
"""

import os
import importlib
import inspect
from typing import Dict, Any, Tuple, Optional, Set
from ..environment import Environment


class NameMapper:
    """Handles conversion between Python attribute names and LisPy function names."""
    
    def __init__(self):
        # Special mappings that don't follow standard patterns (legacy system)
        self.special_mappings = {
            'add': '+',
            'subtract': '-', 
            'multiply': '*',
            'divide': '/',
            'modulo': '%',
            'equals': '=',
            'less_than': '<',
            'less_than_or_equal': '<=',
            'greater_than': '>',
            'greater_than_or_equal': '>=',
            'equal_q': 'equal?',
            'not_fn': 'not',
            'http_get': 'http-get',
            'http_post': 'http-post', 
            'http_put': 'http-put',
            'http_delete': 'http-delete',
            'http_request': 'http-request',
            'json_encode': 'json-encode',
            'json_decode': 'json-decode',
            'web_app': 'web-app',
            'start_server': 'start-server',
            'stop_server': 'stop-server',
            'read_line': 'read-line',
            'print_doc': 'print-doc',
            'hash_map': 'hash-map',
            'promise_all': 'promise-all',
            'promise_race': 'promise-race',
            'promise_any': 'promise-any',
            'promise_all_settled': 'promise-all-settled',
            'promise_then': 'promise-then',
            'on_reject': 'on-reject',
            'on_complete': 'on-complete',
            'with_timeout': 'with-timeout',
            'async_map': 'async-map',
            'async_filter': 'async-filter', 
            'async_reduce': 'async-reduce',
            'to_str': 'to-str',
            'to_int': 'to-int',
            'to_float': 'to-float',
            'to_bool': 'to-bool',
        }
    
    def get_lispy_name_from_attribute(self, attr_name: str) -> Optional[str]:
        """
        Convert Python attribute name to LisPy function name (legacy pattern-based).
        
        Examples:
            builtin_add -> +
            builtin_is_nil_q -> is-nil?
            append_fn -> append
            to_str_fn -> to-str
        """
        if attr_name.startswith('builtin_'):
            python_name = attr_name[8:]  # Remove 'builtin_' prefix
            return self.python_name_to_lispy(python_name)
            
        elif attr_name.endswith('_fn'):
            python_name = attr_name[:-3]  # Remove '_fn' suffix
            return self.python_name_to_lispy(python_name)
            
        return None
    
    def python_name_to_lispy(self, python_name: str) -> str:
        """Convert Python function name to LisPy naming convention (legacy)."""
        if python_name in self.special_mappings:
            return self.special_mappings[python_name]
        
        # Convert underscores to hyphens
        lispy_name = python_name.replace('_', '-')
        
        # Convert _q suffix to ? suffix
        if lispy_name.endswith('-q'):
            lispy_name = lispy_name[:-2] + '?'
            
        return lispy_name
    
    def get_documentation_attribute_name(self, function_attr_name: str) -> str:
        """Get the expected documentation attribute name for a function (legacy)."""
        if function_attr_name.startswith('builtin_'):
            base_name = function_attr_name[8:]  # Remove 'builtin_'
            return f'documentation_{base_name}'
        elif function_attr_name.endswith('_fn'):
            base_name = function_attr_name[:-3]  # Remove '_fn'
            return f'documentation_{base_name}'
        else:
            return f'documentation_{function_attr_name}'


class FunctionDiscovery:
    """Handles discovery of functions in packages and modules."""
    
    def __init__(self, name_mapper: NameMapper):
        self.name_mapper = name_mapper
        self.discovered_modules: Set[str] = set()
    
    def discover_in_package(self, package_path: str, package_name: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """
        Discover all functions in a package and its subpackages.
        
        Returns:
            Tuple of (functions_dict, documentation_dict, web_unsafe_dict)
        """
        functions = {}
        documentation = {}
        web_unsafe = {}
        
        for item in os.listdir(package_path):
            item_path = os.path.join(package_path, item)
            
            if self._should_skip_item(item):
                continue
                
            if self._is_python_package(item_path):
                # Recursively discover in subpackages
                subpackage_name = f"{package_name}.{item}"
                sub_functions, sub_docs, sub_unsafe = self.discover_in_package(item_path, subpackage_name)
                functions.update(sub_functions)
                documentation.update(sub_docs)
                web_unsafe.update(sub_unsafe)
                
            elif self._is_python_module(item):
                # Discover functions in individual module
                module_name = f"{package_name}.{item[:-3]}"  # Remove .py extension
                mod_functions, mod_docs, mod_unsafe = self._discover_in_module(module_name)
                functions.update(mod_functions)
                documentation.update(mod_docs)
                web_unsafe.update(mod_unsafe)
        
        # Handle special module patterns (legacy)
        special_functions, special_docs = self._handle_special_modules(package_name)
        functions.update(special_functions)
        documentation.update(special_docs)
        
        # Discover decorator-registered functions
        decorator_functions, decorator_docs, decorator_unsafe = self._discover_decorator_registered()
        functions.update(decorator_functions)
        documentation.update(decorator_docs)
        web_unsafe.update(decorator_unsafe)
        
        return functions, documentation, web_unsafe
    
    def _discover_decorator_registered(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """Discover functions registered via decorators."""
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
        return item == '__pycache__' or item.startswith('.')
    
    def _is_python_package(self, path: str) -> bool:
        """Check if a path is a Python package."""
        return os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py'))
    
    def _is_python_module(self, item: str) -> bool:
        """Check if an item is a Python module."""
        return item.endswith('.py') and item != '__init__.py'
    
    def _discover_in_module(self, module_name: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """Discover functions in a specific module (legacy pattern-based)."""
        if module_name in self.discovered_modules:
            return {}, {}, {}
            
        functions = {}
        documentation = {}
        
        try:
            module = importlib.import_module(module_name)
            self.discovered_modules.add(module_name)
            
            # Get all attributes from the module
            for attr_name in dir(module):
                if attr_name.startswith('_'):
                    continue
                    
                attr_value = getattr(module, attr_name)
                
                # Check for function patterns (legacy)
                lispy_name = self.name_mapper.get_lispy_name_from_attribute(attr_name)
                if lispy_name and callable(attr_value):
                    functions[lispy_name] = attr_value
                    
                    # Look for corresponding documentation
                    doc_attr_name = self.name_mapper.get_documentation_attribute_name(attr_name)
                    if hasattr(module, doc_attr_name):
                        doc_value = getattr(module, doc_attr_name)
                        documentation[lispy_name] = doc_value
                        
        except ImportError as e:
            print(f"Warning: Could not import module {module_name}: {e}")
        
        return functions, documentation, {}  # No web_unsafe from legacy discovery
    
    def _handle_special_modules(self, package_name: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle special modules that don't follow standard patterns (legacy)."""
        functions = {}
        documentation = {}
        
        # Handle BDD assertions which use a dictionary mapping
        if package_name == 'lispy.functions':
            try:
                bdd_module = importlib.import_module(f"{package_name}.bdd_assertions")
                if hasattr(bdd_module, 'bdd_assertion_functions'):
                    bdd_functions = getattr(bdd_module, 'bdd_assertion_functions')
                    if isinstance(bdd_functions, dict):
                        for lispy_name, function in bdd_functions.items():
                            functions[lispy_name] = function
                            
                            # Look for documentation
                            doc_attr_name = f"documentation_{lispy_name.replace('-', '_').replace('?', '_q')}"
                            if hasattr(bdd_module, doc_attr_name):
                                doc_func = getattr(bdd_module, doc_attr_name)
                                documentation[lispy_name] = doc_func
            except ImportError:
                pass
        
        return functions, documentation


class FunctionRegistry:
    """Coordinates function discovery and handles registration."""
    
    def __init__(self):
        self.name_mapper = NameMapper()
        self.discovery = FunctionDiscovery(self.name_mapper)
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
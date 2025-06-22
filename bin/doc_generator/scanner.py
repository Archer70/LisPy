"""
Documentation scanning functionality.
"""

import sys
from pathlib import Path
from typing import List, Dict
from .models import FunctionDoc
from .parser import DocumentationParser


class DocumentationScanner:
    """Scan the codebase for documentation using module imports."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.parser = DocumentationParser()
        
        # Add the project root to Python path for imports
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
    
    def scan_specific_functions(self, function_names: List[str]) -> Dict[str, FunctionDoc]:
        """Scan only specific functions."""
        all_docs = self.scan_functions()
        return {name: doc for name, doc in all_docs.items() if name in function_names}
    
    def scan_functions(self) -> Dict[str, FunctionDoc]:
        """Scan functions and special forms using module imports."""
        docs = {}
        
        # Import the modules to get their __all__ exports
        try:
            # Import functions module
            from lispy.functions import __all__ as functions_all
            docs.update(self.scan_function_docs(functions_all))
            
            # Import special forms module  
            from lispy.special_forms import __all__ as special_forms_all
            docs.update(self.scan_special_form_docs(special_forms_all))
            
        except ImportError as e:
            print(f"Error importing modules: {e}")
            
        return docs
    
    def scan_function_docs(self, function_exports: List[str]) -> Dict[str, FunctionDoc]:
        """Scan function documentation using the functions module __all__ exports."""
        docs = {}
        
        # Import the documentation registry to get documentation functions
        try:
            from lispy.functions.doc import DOCUMENTATION_REGISTRY
            
            # Get all available function symbols from the global environment
            from lispy.functions import global_env
            
            # Get all function names from the environment
            function_symbols = []
            for symbol in global_env.store.keys():
                # Skip special characters that aren't functions
                if symbol not in ['nil', 'true', 'false'] and not symbol.startswith('__'):
                    function_symbols.append(symbol)
            
            # Extract documentation for each function
            for symbol in function_symbols:
                try:
                    if symbol in DOCUMENTATION_REGISTRY:
                        doc_function = DOCUMENTATION_REGISTRY[symbol]
                        doc_string = doc_function()
                        
                        # Determine category from documentation function's module path
                        category = self.get_category_from_doc_function(doc_function)
                        
                        func_doc = self.parser.parse_function_doc(
                            doc_string,
                            symbol,
                            category,
                            f"lispy/functions/{category}"
                        )
                        docs[symbol] = func_doc
                        
                except Exception as e:
                    print(f"Warning: Could not get documentation for function '{symbol}': {e}")
                    
        except ImportError as e:
            print(f"Error importing documentation registry: {e}")
            
        return docs
    
    def get_category_from_doc_function(self, doc_function) -> str:
        """Extract category from documentation function's module path."""
        try:
            # Get the module path of the documentation function
            module_path = doc_function.__module__
            
            # Expected format: lispy.functions.category.function_name
            # Example: lispy.functions.math.add -> category = 'math'
            path_parts = module_path.split('.')
            
            if len(path_parts) >= 3 and path_parts[0] == 'lispy' and path_parts[1] == 'functions':
                category = path_parts[2]
                return category
            
            # Fallback for unexpected module paths
            return 'other'
            
        except Exception:
            # If anything goes wrong, return default category
            return 'other'
    
    def scan_special_form_docs(self, special_form_exports: List[str]) -> Dict[str, FunctionDoc]:
        """Scan special form documentation using the special_forms module __all__ exports."""
        docs = {}
        
        try:
            from lispy.functions.doc import DOCUMENTATION_REGISTRY
            from lispy.special_forms import special_form_handlers
            
            # Extract documentation for each special form
            for symbol in special_form_handlers.keys():
                try:
                    if symbol in DOCUMENTATION_REGISTRY:
                        doc_function = DOCUMENTATION_REGISTRY[symbol]
                        doc_string = doc_function()
                        
                        func_doc = self.parser.parse_function_doc(
                            doc_string,
                            symbol,
                            'special-forms',
                            f"lispy/special_forms/{symbol.replace('-', '_')}_form.py",
                            doc_type="special-form"
                        )
                        docs[symbol] = func_doc
                        
                except Exception as e:
                    print(f"Warning: Could not get documentation for special form '{symbol}': {e}")
                    
        except ImportError as e:
            print(f"Error importing special forms: {e}")
            
        return docs
    
    def categorize_function(self, symbol: str) -> str:
        """Categorize a function based on its symbol name."""
        # This method is now deprecated - use get_category_from_doc_function instead
        # Keeping it as fallback for any edge cases
        return 'other' 
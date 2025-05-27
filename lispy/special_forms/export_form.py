from ..exceptions import EvaluationError
from ..types import Symbol
from ..module_system import get_current_module


def export_form(expression, env, evaluate):
    """
    Handle the export special form.
    Syntax: (export symbol1 symbol2 ...)
    
    Adds the specified symbols to the current module's export list.
    The symbols must be defined in the module for the export to be meaningful.
    """
    if len(expression) < 2:
        raise EvaluationError("SyntaxError: 'export' requires at least one symbol")
    
    # Get the current module context
    current_module = get_current_module(env)
    if current_module is None:
        raise EvaluationError("SyntaxError: 'export' can only be used within a module")
    
    # Extract symbol names to export
    symbols_to_export = expression[1:]  # Skip the 'export' symbol itself
    
    for symbol_expr in symbols_to_export:
        if not isinstance(symbol_expr, Symbol):
            raise EvaluationError(f"SyntaxError: 'export' expects symbols, got {type(symbol_expr).__name__}")
        
        symbol_name = symbol_expr.name
        
        # Add to module's export list
        current_module.add_export(symbol_name)
    
    # Return nil (export is a side-effect operation)
    return None 
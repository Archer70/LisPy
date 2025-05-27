from typing import List, Any, Callable

from ..types import Symbol
from ..exceptions import EvaluationError
from ..environment import Environment
from ..closure import Function # For creating Function instances

def handle_fn_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Function:
    """Handles the (fn (params...) body1 ...) special form."""
    # evaluate_fn is not directly used here for fn *creation*,
    # but would be if we had macros that transform fn, or for validation. It's kept for consistency.
    if len(expression) < 3:
        raise EvaluationError("SyntaxError: 'fn' requires a parameter list and at least one body expression. Usage: (fn (params...) body1 ...)")
    
    params_list = expression[1]
    if not isinstance(params_list, list):
        # Check if it's LispyList as well, since parser produces LispyList for (...) part of (fn (...) ...)
        # However, the structure is (fn SYMBOL_PARAMS_LIST BODY), so params_list here should be the actual list of symbols.
        # The test `test_lambda_syntax_error_params_not_list` uses a Symbol directly, so `list` is the correct check for the internal structure.
        raise EvaluationError(f"SyntaxError: Parameter list for 'fn' must be a list, got {type(params_list).__name__}")
    
    for p in params_list:
        if not isinstance(p, Symbol):
            raise EvaluationError(f"SyntaxError: All parameters in 'fn' parameter list must be symbols, got {type(p).__name__}: '{p}'")
    
    body_expressions = expression[2:]
    if not body_expressions: # Should be caught by len(expression) < 3, but good for clarity
        raise EvaluationError("SyntaxError: 'fn' must have at least one expression in its body.")
    
    return Function(params_list, body_expressions, env) # Create and return the closure 
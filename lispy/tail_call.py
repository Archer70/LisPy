"""
Tail Call Optimization support for LisPy.

This module provides the TailCall class and utilities for implementing
tail call optimization in the LisPy interpreter.
"""

from typing import List, Any
from .closure import Function
from .exceptions import EvaluationError


class TailCall:
    """
    Represents a tail call that should be optimized.

    Instead of making a recursive function call that would consume stack space,
    the evaluator returns a TailCall object that contains the function to call
    and its arguments. The trampoline loop then handles the call iteratively.
    """

    def __init__(self, function: Function, args: List[Any]):
        """
        Initialize a tail call.

        Args:
            function: The Function object to call
            args: List of evaluated arguments to pass to the function
        """
        self.function = function
        self.args = args

    def __repr__(self) -> str:
        return f"TailCall({self.function}, {self.args})"


def is_tail_position(expr_index: int, body_length: int) -> bool:
    """
    Check if an expression is in tail position within a function body.

    An expression is in tail position if it's the last expression in the
    function body, meaning its value will be the return value of the function.

    Args:
        expr_index: Index of the expression in the body
        body_length: Total number of expressions in the body

    Returns:
        True if the expression is in tail position
    """
    return expr_index == body_length - 1


def is_function_call(expr: Any) -> bool:
    """
    Check if an expression represents a function call.

    Args:
        expr: The expression to check

    Returns:
        True if the expression is a non-empty list (function call form)
    """
    return isinstance(expr, (list, type([]))) and len(expr) > 0


def is_recursive_call(expr: Any, current_function: Function, env) -> bool:
    """
    Check if a function call is recursive (calls the same function).

    Args:
        expr: The expression to check (should be a function call)
        current_function: The function currently being executed
        env: The environment to resolve symbols in

    Returns:
        True if this is a recursive call to current_function
    """
    if not is_function_call(expr):
        return False

    try:
        from .types import Symbol

        operator = expr[0]
        if isinstance(operator, Symbol):
            # Look up the symbol in the environment
            resolved_function = env.lookup(operator.name)
            return resolved_function is current_function
        # Could also handle direct function references, but symbols are most common
    except (EvaluationError, AttributeError):
        # If lookup fails or any other error, assume not recursive
        pass

    return False

# lispy_project/lispy/utils.py

from lispy.evaluator import evaluate
from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.types import Symbol, Vector, LispyList

# from lispy.environment import Environment # For type hinting if desired later
# from typing import Any # For type hinting if desired later


def run_lispy_string(code_string: str, env):
    """
    Tokenizes, parses, and evaluates a string of LisPy code in the given environment.
    Returns the result of the evaluation.
    """
    tokens = tokenize(code_string)
    if (
        not tokens and not code_string.strip()
    ):  # Handle empty or whitespace-only strings gracefully
        return None  # Or raise a specific error, or let parse handle it if it does

    parsed_expr = parse(tokens)
    result = evaluate(parsed_expr, env)
    return result


def format_lispy_value_for_display(value):
    """
    Format a LisPy value for consistent display in REPL and other output contexts.
    
    This function handles the proper representation of nil, booleans, and other
    LisPy values to match the language's conventions.
    
    Args:
        value: Any LisPy value to format
        
    Returns:
        str: Properly formatted string representation
    """
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        # For strings, we want to show them with quotes in REPL display
        return f'"{value}"'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, Symbol):
        return value.name
    elif isinstance(value, Vector):
        # Use the Vector's __repr__ method which gives "[1 2 3]" format
        return repr(value)
    elif isinstance(value, LispyList):
        # Use the LispyList's __repr__ method which gives "(1 2 3)" format  
        return repr(value)
    elif isinstance(value, dict):
        # For hash maps, create a simple representation
        items = []
        for k, v in value.items():
            if isinstance(k, Symbol):
                key_str = k.name
            else:
                key_str = format_lispy_value_for_display(k)
            val_str = format_lispy_value_for_display(v)
            items.append(f"{key_str} {val_str}")
        return "{" + " ".join(items) + "}"
    else:
        # Fallback to Python's str() for any other types
        return str(value)

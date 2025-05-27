# lispy_project/lispy/utils.py

from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
# from lispy.environment import Environment # For type hinting if desired later
# from typing import Any # For type hinting if desired later

def run_lispy_string(code_string: str, env):
    """
    Tokenizes, parses, and evaluates a string of LisPy code in the given environment.
    Returns the result of the evaluation.
    """
    tokens = tokenize(code_string)
    if not tokens and not code_string.strip(): # Handle empty or whitespace-only strings gracefully
        return None # Or raise a specific error, or let parse handle it if it does
    
    parsed_expr = parse(tokens)
    result = evaluate(parsed_expr, env)
    return result 
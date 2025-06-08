from lispy.exceptions import EvaluationError
from lispy.types import Vector


def split_fn(args, env):
    """Split a string into a vector of substrings.
    
    Usage: (split string separator)
    
    Args:
        string: The string to split
        separator: The separator to split on
        
    Returns:
        A vector of substrings
        
    Examples:
        (split "a,b,c" ",") => ["a" "b" "c"]
        (split "hello world" " ") => ["hello" "world"]
        (split "one-two-three" "-") => ["one" "two" "three"]
        (split "hello" "") => ["h" "e" "l" "l" "o"]  ; Split into characters
        (split "" ",") => [""]  ; Empty string gives vector with one empty string
    """
    if len(args) != 2:
        raise EvaluationError(f"SyntaxError: 'split' expects 2 arguments, got {len(args)}.")
    
    string, separator = args
    
    # Validate string is a string
    if not isinstance(string, str):
        raise EvaluationError(f"TypeError: 'split' first argument must be a string, got {type(string)}.")
    
    # Validate separator is a string
    if not isinstance(separator, str):
        raise EvaluationError(f"TypeError: 'split' second argument (separator) must be a string, got {type(separator)}.")
    
    # Handle special case of empty separator (split into characters)
    if separator == "":
        return Vector(list(string))
    
    # Split the string
    parts = string.split(separator)
    return Vector(parts) 
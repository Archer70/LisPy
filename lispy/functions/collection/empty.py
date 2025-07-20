from typing import List, Any
from lispy.types import Vector  # For type checking
from lispy.exceptions import EvaluationError
from lispy.environment import Environment  # Added Environment import
from lispy.functions.decorators import lispy_function, lispy_documentation


@lispy_function("empty?")
def empty_q(args: List[Any], env: Environment) -> bool:  # Added env parameter
    """Checks if a collection (list, vector, map, string) or nil is empty. (empty? collection)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'empty?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    if arg is None:  # nil
        return True
    elif isinstance(arg, (list, Vector, str, dict)):
        return not bool(arg)  # len(arg) == 0 works for these types
    else:
        type_name = type(arg).__name__
        # Special handling for Function type name for clarity in error
        if hasattr(arg, "__class__") and arg.__class__.__name__ == "Function":
            type_name = "Function"
        raise EvaluationError(
            f"TypeError: 'empty?' expects a list, vector, map, string, or nil. Got {type_name}"
        )


@lispy_documentation("empty?")
def empty_q_documentation() -> str:
    """Returns documentation for the empty? function."""
    return """Function: empty?
Arguments: (empty? collection)
Description: Tests whether a collection, string, or nil is empty.

Examples:
  (empty? [])                   ; => true
  (empty? [1 2 3])              ; => false
  (empty? '())                  ; => true
  (empty? '(a b))               ; => false
  (empty? {})                   ; => true
  (empty? {:a 1})               ; => false
  (empty? "")                   ; => true
  (empty? "hello")              ; => false
  (empty? nil)                  ; => true

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, maps, strings, and nil
  - Returns true for empty collections/strings or nil
  - Returns false for non-empty collections/strings
  - nil is considered empty (returns true)
  - Essential for conditional logic on collection states
  - Useful for validation and flow control
  - Complement of checking collection size/length"""

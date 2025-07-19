from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("empty?")
def empty_q(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'empty?' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Handle nil case - nil is considered empty
    if collection is None:
        return True

    # Check if collection is empty
    if isinstance(collection, (list, str, dict)):
        return len(collection) == 0
    else:
        raise EvaluationError(
            f"TypeError: 'empty?' expects a collection (list, vector, map, or string), got {type(collection).__name__}: '{collection}'"
        )


@lispy_documentation("empty?")
def empty_q_documentation() -> str:
    return """Function: empty?
Arguments: (empty? collection)
Description: Tests whether a collection is empty.

Examples:
  (empty? [])                   ; => true
  (empty? '())                  ; => true
  (empty? {})                   ; => true
  (empty? "")                   ; => true
  (empty? nil)                  ; => true
  (empty? [1 2 3])              ; => false
  (empty? "hello")              ; => false
  (empty? {:a 1})               ; => false

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, maps, and strings
  - nil is considered empty
  - Returns true only if collection has zero elements
  - Useful for conditional logic and validation
  - Complement of checking count > 0
  - Essential for control flow in collection processing"""

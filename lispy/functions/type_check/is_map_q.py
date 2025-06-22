# lispy_project/lispy/functions/type_check/is_map_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_map_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a map, false otherwise. (is-map? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-map?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, dict)


def documentation_is_map_q() -> str:
    """Returns documentation for the is-map? function."""
    return """Function: is-map?
Arguments: (is-map? value)
Description: Tests whether a value is a map (hash map/dictionary).

Examples:
  (is-map? {})              ; => true
  (is-map? {:a 1 :b 2})     ; => true
  (is-map? (hash-map 'a 1)) ; => true
  (is-map? {:x {:y 2}})     ; => true (nested map)
  (is-map? [1 2 3])         ; => false (vector)
  (is-map? '(1 2 3))        ; => false (list)
  (is-map? "hello")         ; => false
  (is-map? 42)              ; => false
  (is-map? nil)             ; => false

Notes:
  - Returns true for hash maps/dictionaries
  - Empty map {} returns true
  - Works with nested maps and mixed value types
  - Essential for distinguishing maps from other collection types
  - Maps provide key-value associations
  - Requires exactly one argument"""

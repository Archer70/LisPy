# lispy_project/lispy/functions/type_check/is_map_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-map?")
def is_map(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-map?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, dict)


@lispy_documentation("is-map?")
def is_map_documentation() -> str:
    return """Function: is-map?
Arguments: (is-map? value)
Description: Tests whether a value is a map (hash map).

Examples:
  (is-map? {:a 1 :b 2})     ; => true
  (is-map? {})              ; => true (empty map)
  (is-map? (hash-map :a 1)) ; => true
  (is-map? [1 2 3])         ; => false (vector)
  (is-map? '(1 2 3))        ; => false (list)
  (is-map? 42)              ; => false (number)
  (is-map? "hello")         ; => false (string)
  (is-map? nil)             ; => false

Notes:
  - Returns true only for map values (key-value collections)
  - Maps are created with curly braces {} or (hash-map ...)
  - Useful for type validation before map operations
  - Different from other collection types
  - Requires exactly one argument"""

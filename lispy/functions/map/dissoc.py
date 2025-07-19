from lispy.types import Symbol
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any


def builtin_dissoc(args: List[Any], env: Environment):
    """Removes keys from a map.
    (dissoc map key & keys)
    Behaves like Clojure's dissoc.
    """
    if not args:
        raise EvaluationError(
            "SyntaxError: 'dissoc' expects at least 1 argument (map), got 0."
        )

    target_map, *keys = args

    if target_map is None:
        return None

    if not isinstance(target_map, dict):
        raise EvaluationError(
            f"TypeError: First argument to 'dissoc' must be a map or nil, got {type(target_map)}."
        )

    if not keys:
        return target_map.copy()

    new_map = target_map.copy()
    for key_to_remove in keys:
        # Keys can be symbols, strings, numbers, booleans, or nil
        if not isinstance(key_to_remove, (Symbol, str, int, float, bool, type(None))):
            raise EvaluationError(
                f"TypeError: Keys to 'dissoc' must be symbols, strings, numbers, booleans, or nil, got {type(key_to_remove)}."
            )
        if key_to_remove in new_map:
            del new_map[key_to_remove]
    return new_map


def documentation_dissoc() -> str:
    """Returns documentation for the dissoc function."""
    return """Function: dissoc
Arguments: (dissoc map key1 key2 ...)
Description: Removes keys from a map, returning a new map without those keys.

Examples:
  (dissoc {:a 1 :b 2 :c 3} ':b)         ; => {:a 1 :c 3}
  (dissoc {:a 1 :b 2} ':a ':b)          ; => {}
  (dissoc {} ':missing)                 ; => {} (missing keys ignored)
  (dissoc {:a 1 :b 2} ':c)              ; => {:a 1 :b 2} (key not present)
  (dissoc nil ':a)                      ; => nil
  (dissoc {:a 1})                       ; => {:a 1} (no keys to remove)

Notes:
  - Requires at least 1 argument (the map)
  - First argument must be a map or nil
  - All key arguments must be symbols
  - If no keys provided, returns copy of original map
  - Missing keys are silently ignored
  - nil maps return nil
  - Returns new map, original is not modified
  - Essential for removing unwanted map entries
  - Mirrors Clojure's dissoc function"""

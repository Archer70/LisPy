from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError

from ..decorators import lispy_documentation, lispy_function


@lispy_function("merge")
def merge(args: List[Any], env: Environment):
    """Merge multiple hash maps into a single hash map.

    Usage: (merge map1 map2 ...)

    Args:
        map1, map2, ...: Hash maps to merge

    Returns:
        A new hash map containing all key-value pairs from the input maps.
        Later arguments override earlier ones for duplicate keys.

    Examples:
        (merge {:a 1} {:b 2}) => {:a 1 :b 2}
        (merge {:a 1} {:a 2 :b 3}) => {:a 2 :b 3}  ; Later :a overrides
        (merge) => {}  ; Empty merge returns empty map
    """
    if len(args) == 0:
        # Empty merge returns empty hash map
        return {}

    # Validate all arguments are hash maps
    for i, arg in enumerate(args):
        if not isinstance(arg, dict):
            raise EvaluationError(
                f"TypeError: 'merge' arguments must be hash maps, got {type(arg)} at position {i}."
            )

    # Merge all maps, with later ones overriding earlier ones
    result_map = {}
    for hash_map in args:
        result_map.update(hash_map)

    return result_map


@lispy_documentation("merge")
def merge_doc() -> str:
    """Returns documentation for the merge function."""
    return """Function: merge
Arguments: (merge map1 map2 ...)
Description: Merges multiple hash maps into a single new hash map.

Examples:
  (merge)                       ; => {}
  (merge {:a 1})                ; => {:a 1}
  (merge {:a 1} {:b 2})         ; => {:a 1 :b 2}
  (merge {:a 1} {:a 2 :b 3})    ; => {:a 2 :b 3} (later overrides)
  (merge {:a 1} {} {:b 2})      ; => {:a 1 :b 2}
  (merge {:x 1} {:y 2} {:z 3})  ; => {:x 1 :y 2 :z 3}

Notes:
  - Accepts zero or more hash map arguments
  - All arguments must be hash maps
  - Returns a new hash map, does not modify originals
  - Later maps override earlier maps for duplicate keys
  - Empty merge returns empty map {}
  - Empty maps are ignored in the merge"""

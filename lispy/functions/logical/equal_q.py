from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Symbol, Vector


@lispy_function("equal?")
def equal_q(args: List[Any], env: Environment) -> bool:
    if len(args) < 2:
        raise EvaluationError(
            "SyntaxError: 'equal?' requires at least 2 arguments, got {}.".format(
                len(args)
            )
        )

    first_item = args[0]

    for i in range(1, len(args)):
        if not _are_equal(first_item, args[i]):
            return False

    return True


def _are_equal(a: Any, b: Any) -> bool:
    """Helper function to determine structural equality between two values."""

    # Handle None/nil case
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False

    # Check if types are different (strict type checking)
    if type(a) != type(b):
        # Special case: numbers (int and float can be equal, but not bool)
        if (
            isinstance(a, (int, float))
            and isinstance(b, (int, float))
            and not isinstance(a, bool)
            and not isinstance(b, bool)
        ):
            return a == b
        return False

    # Primitive types: direct comparison
    if isinstance(a, (int, float, str, bool)):
        return a == b

    # Symbol comparison
    if isinstance(a, Symbol):
        return a == b

    # Vector comparison (order matters)
    if isinstance(a, Vector):
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if not _are_equal(a[i], b[i]):
                return False
        return True

    # List comparison (order matters)
    if isinstance(a, list):
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if not _are_equal(a[i], b[i]):
                return False
        return True

    # Map/dict comparison (order doesn't matter)
    if isinstance(a, dict):
        if len(a) != len(b):
            return False

        # Check all keys and values
        for key in a:
            if key not in b:
                return False
            if not _are_equal(a[key], b[key]):
                return False

        return True

    # For any other types, fall back to Python's equality
    return a == b


@lispy_documentation("equal?")
def equal_q_documentation() -> str:
    return """Function: equal?
Arguments: (equal? value1 value2 ...)
Description: Tests if all values are structurally equal (deep equality).

Examples:
  (equal? 5 5)                    ; => true
  (equal? 5 5.0)                  ; => true
  (equal? "hello" "hello")        ; => true
  (equal? [1 2 3] [1 2 3])       ; => true
  (equal? {:a 1 :b 2} {:b 2 :a 1}) ; => true (order independent)
  (equal? '(1 2) '(1 2))         ; => true
  (equal? [[1 2] {:a 3}] [[1 2] {:a 3}]) ; => true (deep equality)
  (equal? 5 "5")                  ; => false (different types)
  (equal? [1 2] '(1 2))          ; => false (different collection types)
  (equal? 5 5 5 5)               ; => true (all equal)
  (equal? 5 5 6 5)               ; => false (one different)

Notes:
  - Requires at least 2 arguments
  - Returns true only if ALL arguments are equal
  - Performs deep structural comparison for collections
  - Numbers: 5 and 5.0 are considered equal
  - Strings: case-sensitive comparison
  - Vectors: order matters, [1 2] ≠ [2 1]
  - Maps: order doesn't matter, {:a 1 :b 2} = {:b 2 :a 1}
  - Lists: order matters, same as vectors
  - Cross-type comparison always returns false
  - Supports nested structures recursively"""

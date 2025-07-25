from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import AssertionFailure, EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function


@lispy_function("assert-equal?")
def assert_equal_q(args: List[Any], env: Environment) -> bool:
    """(assert-equal? expected actual)
    Asserts that `actual` is equal to `expected`.
    Raises AssertionFailure if they are not equal. Returns true if equal.
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'assert-equal?' expects 2 arguments (expected actual), got {len(args)}."
        )

    expected = args[0]
    actual = args[1]

    # Using LisPy's equality logic if available, otherwise Python's `==`
    # For now, let's assume standard Python equality is sufficient for most LisPy types.
    # This might need to be revisited if LisPy has custom equality for its types (e.g. vectors, lists).
    if expected != actual:
        raise AssertionFailure(
            f"Assertion Failed: Expected [{expected}] (type: {type(expected).__name__}) but got [{actual}] (type: {type(actual).__name__})."
        )

    return True  # Assertion passed


@lispy_documentation("assert-equal?")
def assert_equal_q_doc() -> str:
    """Returns documentation for the assert-equal? function."""
    return """Function: assert-equal?
Arguments: (assert-equal? expected actual)
Description: BDD assertion that verifies two values are equal.

Examples:
  (assert-equal? 5 5)           ; => true (assertion passes)
  (assert-equal? "hello" "hello") ; => true (strings equal)
  (assert-equal? [1 2] [1 2])   ; => true (vectors equal)
  (assert-equal? nil nil)       ; => true (nil values equal)
  
  ; Assertion failures raise AssertionFailure:
  (assert-equal? 5 6)           ; => AssertionFailure: Expected [5] but got [6]
  (assert-equal? "5" 5)         ; => AssertionFailure: Different types
  (assert-equal? true false)    ; => AssertionFailure: Expected [true] but got [false]

Notes:
  - Requires exactly 2 arguments (expected, actual)
  - Uses Python's equality semantics (==)
  - Returns true if assertion passes
  - Raises AssertionFailure with detailed message if values differ
  - Error message includes both values and their types
  - Essential for BDD testing workflows
  - Used within 'then' steps for test verification
  - Supports all LisPy data types (numbers, strings, lists, vectors, maps, etc.)"""

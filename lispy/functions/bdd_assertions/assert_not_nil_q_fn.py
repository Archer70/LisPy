from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure
from ...environment import Environment


def bdd_assert_not_nil_q(args: List[Any], env: Environment) -> bool:
    """(assert-not-nil? expr)
    Asserts that the expression `expr` does not evaluate to nil (None).
    Raises AssertionFailure if it is nil. Returns true if the assertion passes.
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'assert-not-nil?' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    if value is None:  # Check if it IS nil
        raise AssertionFailure(
            "Assertion Failed: Expected a non-nil value but got [nil]."
        )

    return True  # Assertion passed, value is not nil


def documentation_assert_not_nil_q() -> str:
    """Returns documentation for the assert-not-nil? function."""
    return """Function: assert-not-nil?
Arguments: (assert-not-nil? expression)
Description: BDD assertion that verifies an expression does not evaluate to nil.

Examples:
  (assert-not-nil? 0)           ; => true (0 is not nil)
  (assert-not-nil? false)       ; => true (false is not nil)
  (assert-not-nil? "")          ; => true (empty string is not nil)
  (assert-not-nil? [])          ; => true (empty vector is not nil)
  (assert-not-nil? {})          ; => true (empty map is not nil)
  (assert-not-nil? (+ 1 2))     ; => true (3 is not nil)
  
  ; Assertion failures raise AssertionFailure:
  (assert-not-nil? nil)         ; => AssertionFailure: Expected non-nil but got [nil]
  (assert-not-nil? (get {} ':a)) ; => AssertionFailure: Missing key returns nil
  (assert-not-nil? (first '())) ; => AssertionFailure: first of empty is nil

Notes:
  - Requires exactly 1 argument
  - Accepts any value except nil (Python None)
  - Returns true if assertion passes (value is not nil)
  - Raises AssertionFailure if value is nil
  - Essential for BDD testing workflows
  - Used within 'then' steps to verify presence of values
  - Useful for testing required data and function return values
  - Complements assert-nil? for comprehensive nil testing"""

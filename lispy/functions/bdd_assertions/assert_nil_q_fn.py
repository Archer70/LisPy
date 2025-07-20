from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure
from lispy.environment import Environment
from lispy.functions.decorators import lispy_function, lispy_documentation


@lispy_function("assert-nil?")
def assert_nil_q(args: List[Any], env: Environment) -> bool:
    """(assert-nil? expr)
    Asserts that the expression `expr` evaluates to nil (None).
    Raises AssertionFailure if it is not nil. Returns true if the assertion passes.
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'assert-nil?' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    if value is not None:
        raise AssertionFailure(
            f"Assertion Failed: Expected [nil] but got [{value}] (type: {type(value).__name__})."
        )

    return True  # Assertion passed


@lispy_documentation("assert-nil?")
def assert_nil_q_doc() -> str:
    """Returns documentation for the assert-nil? function."""
    return """Function: assert-nil?
Arguments: (assert-nil? expression)
Description: BDD assertion that verifies an expression evaluates to nil.

Examples:
  (assert-nil? nil)             ; => true (assertion passes)
  (assert-nil? (get {:a 1} ':b)) ; => true (missing key returns nil)
  (assert-nil? (first '()))     ; => true (first of empty list is nil)
  (assert-nil? (rest [1]))      ; => true (rest of single element is nil)
  
  ; Assertion failures raise AssertionFailure:
  (assert-nil? 0)               ; => AssertionFailure: Expected [nil] but got [0]
  (assert-nil? false)           ; => AssertionFailure: Expected [nil] but got [False]
  (assert-nil? "")              ; => AssertionFailure: Expected [nil] but got [""]
  (assert-nil? [])              ; => AssertionFailure: Expected [nil] but got [[]]

Notes:
  - Requires exactly 1 argument
  - Only accepts the literal nil value (Python None)
  - Not based on LisPy falsiness - requires actual nil value
  - Returns true if assertion passes
  - Raises AssertionFailure with detailed message for any non-nil value
  - Essential for BDD testing workflows
  - Used within 'then' steps for nil verification
  - Useful for testing optional values and missing data"""

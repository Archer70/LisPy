from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("assert-false?")
def assert_false_q(args: List[Any], env: Environment) -> bool:
    """(assert-false? expr)
    Asserts that the expression `expr` evaluates to false.
    Raises AssertionFailure if it is not false. Returns true if the assertion passes.
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'assert-false?' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    if value is not False:
        raise AssertionFailure(
            f"Assertion Failed: Expected [False] but got [{value}] (type: {type(value).__name__})."
        )

    return True  # Assertion passed


@lispy_documentation("assert-false?")
def assert_false_q_doc() -> str:
    """Returns documentation for the assert-false? function."""
    return """Function: assert-false?
Arguments: (assert-false? expression)
Description: BDD assertion that verifies an expression evaluates to false.

Examples:
  (assert-false? false)         ; => true (assertion passes)
  (assert-false? (= 5 6))       ; => true (inequality check passes)
  (assert-false? (> 5 10))      ; => true (comparison passes)
  (assert-false? (not true))    ; => true (logical operation passes)
  
  ; Assertion failures raise AssertionFailure:
  (assert-false? true)          ; => AssertionFailure: Expected [False] but got [True]
  (assert-false? nil)           ; => AssertionFailure: Expected [False] but got [nil]
  (assert-false? 0)             ; => AssertionFailure: Expected [False] but got [0]
  (assert-false? "")            ; => AssertionFailure: Expected [False] but got [""]

Notes:
  - Requires exactly 1 argument
  - Only accepts the literal boolean false value
  - Not based on LisPy falsiness - requires actual false value
  - Returns true if assertion passes
  - Raises AssertionFailure with detailed message for any non-false value
  - Essential for BDD testing workflows
  - Used within 'then' steps for negative boolean verification
  - Stricter than general falsiness checks"""

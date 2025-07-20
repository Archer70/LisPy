from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import AssertionFailure, EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function


@lispy_function("assert-true?")
def assert_true_q(args: List[Any], env: Environment) -> bool:
    """(assert-true? expr)
    Asserts that the expression `expr` evaluates to true.
    Raises AssertionFailure if it is not true. Returns true if the assertion passes.
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'assert-true?' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    if value is not True:
        raise AssertionFailure(
            f"Assertion Failed: Expected [True] but got [{value}] (type: {type(value).__name__})."
        )

    return True  # Assertion passed


@lispy_documentation("assert-true?")
def assert_true_q_doc() -> str:
    """Returns documentation for the assert-true? function."""
    return """Function: assert-true?
Arguments: (assert-true? expression)
Description: BDD assertion that verifies an expression evaluates to true.

Examples:
  (assert-true? true)           ; => true (assertion passes)
  (assert-true? (= 5 5))        ; => true (equality check passes)
  (assert-true? (> 10 5))       ; => true (comparison passes)
  (assert-true? (not false))    ; => true (logical operation passes)
  
  ; Assertion failures raise AssertionFailure:
  (assert-true? false)          ; => AssertionFailure: Expected [True] but got [False]
  (assert-true? nil)            ; => AssertionFailure: Expected [True] but got [nil]
  (assert-true? 1)              ; => AssertionFailure: Expected [True] but got [1]
  (assert-true? "")             ; => AssertionFailure: Expected [True] but got [""]

Notes:
  - Requires exactly 1 argument
  - Only accepts the literal boolean true value
  - Not based on LisPy truthiness - requires actual true value
  - Returns true if assertion passes
  - Raises AssertionFailure with detailed message for any non-true value
  - Essential for BDD testing workflows
  - Used within 'then' steps for boolean verification
  - Stricter than general truthiness checks"""

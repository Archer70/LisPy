from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure
from ...environment import Environment


def bdd_assert_nil_q(args: List[Any], env: Environment) -> bool:
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

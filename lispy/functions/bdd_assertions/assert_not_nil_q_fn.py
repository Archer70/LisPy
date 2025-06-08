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

    if value is None: # Check if it IS nil
        raise AssertionFailure(
            f"Assertion Failed: Expected a non-nil value but got [nil]."
        )
    
    return True # Assertion passed, value is not nil 
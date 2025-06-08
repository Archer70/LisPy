from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure
from ...environment import Environment

def bdd_assert_false_q(args: List[Any], env: Environment) -> bool:
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
    
    return True # Assertion passed 
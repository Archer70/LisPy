from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure

def bdd_assert_true_q(args: List[Any]) -> bool:
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
    
    return True # Assertion passed 
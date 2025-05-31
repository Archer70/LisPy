from typing import List, Any
from lispy.exceptions import EvaluationError, AssertionFailure

def bdd_assert_equal_q(args: List[Any]) -> bool:
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
    
    return True # Assertion passed 
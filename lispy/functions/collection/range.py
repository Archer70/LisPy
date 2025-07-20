from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Vector


@lispy_function("range")
def range(args: List[Any], env: Environment) -> Vector:
    """Implementation of the (range ...) LisPy function.

    Generates a sequence of numbers as a vector.

    Args:
        args: 1-3 arguments:
            - (range end): 0 to end-1
            - (range start end): start to end-1
            - (range start end step): start to end-1 with step
        env: The current environment

    Returns:
        Vector: A vector containing the generated sequence

    Raises:
        EvaluationError: If incorrect number of arguments or invalid argument types
    """
    if not (1 <= len(args) <= 3):
        raise EvaluationError(
            f"SyntaxError: 'range' expects 1-3 arguments, got {len(args)}."
        )

    # Validate all arguments are integers
    for i, arg in enumerate(args):
        if not isinstance(arg, int):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'range' must be an integer, got {type(arg).__name__}: '{arg}'"
            )

    # Parse arguments based on count
    if len(args) == 1:
        start, end, step = 0, args[0], 1
    elif len(args) == 2:
        start, end, step = args[0], args[1], 1
    else:  # len(args) == 3
        start, end, step = args[0], args[1], args[2]

    # Validate step is not zero
    if step == 0:
        raise EvaluationError("ValueError: 'range' step argument must not be zero.")

    # Generate the sequence
    result = []
    current = start

    if step > 0:
        while current < end:
            result.append(current)
            current += step
    else:  # step < 0
        while current > end:
            result.append(current)
            current += step

    return Vector(result)


@lispy_documentation("range")
def range_documentation() -> str:
    """Returns documentation for the range function."""
    return """Function: range
Arguments: (range end) or (range start end) or (range start end step)
Description: Generates a sequence of numbers as a vector.

Examples:
  ; Single argument - from 0 to end-1
  (range 5)                    ; => [0 1 2 3 4]
  (range 0)                    ; => []
  
  ; Two arguments - from start to end-1
  (range 2 8)                  ; => [2 3 4 5 6 7]
  (range 5 5)                  ; => []
  (range 8 2)                  ; => [] (start >= end with positive step)
  
  ; Three arguments - from start to end-1 with step
  (range 0 10 2)               ; => [0 2 4 6 8]
  (range 1 10 3)               ; => [1 4 7]
  (range 10 0 -1)              ; => [10 9 8 7 6 5 4 3 2 1]
  (range 10 0 -2)              ; => [10 8 6 4 2]
  
  ; Edge cases
  (range 3 10 1)               ; => [3 4 5 6 7 8 9]
  (range 10 3 -1)              ; => [10 9 8 7 6 5 4]

Notes:
  - All arguments must be integers
  - Step cannot be zero
  - Returns a vector (not a lazy sequence)
  - Follows Python range() semantics
  - End value is exclusive (not included in result)
  - Empty range returns empty vector
  - Positive step: start < end required for non-empty result
  - Negative step: start > end required for non-empty result
  - Useful for generating index sequences and numeric ranges
"""

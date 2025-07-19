"""
LisPy range function - Generate sequences of numbers.

Usage:
  (range end)           ; 0 to end-1
  (range start end)     ; start to end-1
  (range start end step); start to end-1 with step

Examples:
  (range 5)        ; => [0 1 2 3 4]
  (range 2 8)      ; => [2 3 4 5 6 7]
  (range 0 10 2)   ; => [0 2 4 6 8]
  (range 10 0 -1)  ; => [10 9 8 7 6 5 4 3 2 1]
"""

from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("range")
def range_func(args: List[Any], env: Environment) -> Vector:
    """(range start end) or (range end)
    Creates a vector containing numbers from start (inclusive) to end (exclusive).
    If only one argument is provided, starts from 0.
    """
    if len(args) < 1 or len(args) > 2:
        raise EvaluationError(
            f"SyntaxError: 'range' expects 1 or 2 arguments, got {len(args)}."
        )

    if len(args) == 1:
        # (range end) - from 0 to end
        start = 0
        end = args[0]
    else:
        # (range start end) - from start to end
        start = args[0]
        end = args[1]

    # Validate arguments are numbers
    if not isinstance(start, (int, float)):
        raise EvaluationError(
            f"TypeError: 'range' start must be a number, got {type(start).__name__}."
        )

    if not isinstance(end, (int, float)):
        raise EvaluationError(
            f"TypeError: 'range' end must be a number, got {type(end).__name__}."
        )

    # Convert to integers for range generation
    start_int = int(start)
    end_int = int(end)

    # Generate the range
    if start_int >= end_int:
        # Empty range if start >= end
        return Vector([])
    
    return Vector(list(range(start_int, end_int)))


@lispy_documentation("range")
def range_doc() -> str:
    """Returns documentation for the range function."""
    return """Function: range
Arguments: (range end) or (range start end)
Description: Creates a vector of numbers from start to end (exclusive).

Examples:
  (range 5)        ; => [0 1 2 3 4]
  (range 2 7)      ; => [2 3 4 5 6]
  (range 0 0)      ; => []
  (range 5 2)      ; => [] (start >= end)
  (range -2 3)     ; => [-2 -1 0 1 2]
  (range 10 15)    ; => [10 11 12 13 14]

Notes:
  - Single argument: range from 0 to argument (exclusive)
  - Two arguments: range from start to end (exclusive)
  - Arguments must be numbers (converted to integers)
  - End is exclusive (not included in result)
  - Returns empty vector if start >= end
  - Useful for generating sequences and loops
  - Result is always a vector of integers"""

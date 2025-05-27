from typing import List, Any
from ..exceptions import EvaluationError


def builtin_equals(args: List[Any]) -> bool:
    """Checks if all arguments are equal. (= item1 item2 ...)
    Requires at least two arguments.
    Currently only supports number comparison.
    """
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '=' requires at least two arguments.")

    first_item = args[0]
    if not isinstance(first_item, (int, float)):
        raise EvaluationError(f"TypeError: Argument 1 to '=' must be a number for comparison, got {type(first_item).__name__}: '{first_item}'")

    for i in range(1, len(args)):
        current_item = args[i]
        if not isinstance(current_item, (int, float)):
            raise EvaluationError(f"TypeError: Argument {i+1} to '=' must be a number for comparison, got {type(current_item).__name__}: '{current_item}'")
        if first_item != current_item:
            return False
    return True 
from lispy.exceptions import EvaluationError
from ..environment import Environment
from typing import List, Any
# from numbers import Number # Not strictly needed as no type check on value itself

def builtin_not(args_list: List[Any], env: Environment) -> bool:
    if len(args_list) != 1:
        raise EvaluationError("TypeError: not requires exactly one argument")
    val = args_list[0]
    # Lisp truthiness: False and None (nil) are false, everything else is true.
    # The not function returns True if the value is falsy, False otherwise.
    is_falsy = (val is False or val is None)
    return is_falsy # This was the bug: it should be True if falsy. 
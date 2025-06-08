# lispy_project/lispy/functions/list.py
from typing import List, Any
from ..environment import Environment
from ..types import LispyList

# No specific exceptions needed for list creation itself beyond argument evaluation


def builtin_list(args: List[Any], env: Environment) -> LispyList:
    """Constructs a list from its arguments. (list item1 item2 ...)"""
    # args is already the list of evaluated arguments
    return LispyList(args)  # Return a LispyList instead of regular Python list

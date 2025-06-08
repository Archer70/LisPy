from lispy.types import LispyList, Vector
from lispy.exceptions import EvaluationError
from ..environment import Environment
from typing import List, Any

def builtin_conj(args: List[Any], env: Environment):
    """Implementation of the (conj coll item ...) LisPy function.
    Adds item(s) to a collection (list or vector).
    - For lists, items are prepended (like cons), effectively reversing the order of added items.
    - For vectors, items are appended.
    - If the first argument is nil, it's treated as an empty list.
    Returns a new collection of the same type.
    Usage: (conj collection item1 [item2 ...])
    """
    if len(args) < 2:
        raise EvaluationError(f"SyntaxError: 'conj' expects at least 2 arguments (collection and item(s)), got {len(args)}.")

    collection = args[0]
    items_to_add = args[1:]

    if collection is None: # Treat nil as an empty list
        # For (conj nil item1 item2), result is (item2 item1)
        return LispyList(list(reversed(items_to_add)))
    elif isinstance(collection, LispyList):
        # Prepend items to a new list. items_to_add are prepended in order,
        # so reverse them to get the desired (item_n ... item1 orig_item1 ...)
        new_list_content = list(reversed(items_to_add)) + list(collection)
        return LispyList(new_list_content)
    elif isinstance(collection, Vector):
        # Append items to a new vector
        new_vector_content = list(collection) + list(items_to_add)
        return Vector(new_vector_content)
    else:
        raise EvaluationError(f"TypeError: 'conj' expects a list, vector, or nil as the first argument, got {type(collection)}.") 
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
        raise EvaluationError(
            f"SyntaxError: 'conj' expects at least 2 arguments (collection and item(s)), got {len(args)}."
        )

    collection = args[0]
    items_to_add = args[1:]

    if collection is None:  # Treat nil as an empty list
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
        raise EvaluationError(
            f"TypeError: 'conj' expects a list, vector, or nil as the first argument, got {type(collection)}."
        )


def documentation_conj() -> str:
    """Returns documentation for the conj function."""
    return """Function: conj
Arguments: (conj collection item1 item2 ...)
Description: Adds items to a collection, returning a new collection of the same type.

Examples:
  ; Lists - items are prepended (like cons):
  (conj '(1 2) 3)               ; => (3 1 2)
  (conj '(1) 2 3)               ; => (3 2 1) (items added in reverse order)
  (conj '() 1 2 3)              ; => (3 2 1)
  
  ; Vectors - items are appended:
  (conj [1 2] 3)                ; => [1 2 3]
  (conj [1] 2 3)                ; => [1 2 3] (items added in order)
  (conj [] 1 2 3)               ; => [1 2 3]
  
  ; Nil treated as empty list:
  (conj nil 1)                  ; => (1)
  (conj nil 1 2 3)              ; => (3 2 1)

Notes:
  - Requires at least 2 arguments (collection and one item)
  - First argument must be a list, vector, or nil
  - For lists: items are prepended, reversing order of multiple items
  - For vectors: items are appended in order
  - Nil is treated as an empty list
  - Returns new collection, original is not modified
  - Essential for building collections incrementally
  - Behavior mirrors Clojure's conj function"""

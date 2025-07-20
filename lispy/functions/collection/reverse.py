from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyList, Vector


@lispy_function("reverse")
def reverse(args, env):
    """Reverse the order of elements in a collection.

    Usage: (reverse collection)

    Args:
        collection: A vector or list to reverse

    Returns:
        A new collection of the same type with elements in reverse order

    Examples:
        (reverse [1 2 3 4]) => [4 3 2 1]
        (reverse '(a b c)) => (c b a)
        (reverse []) => []
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'reverse' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Validate collection type
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: Argument to 'reverse' must be a list or vector, got {type(collection)}."
        )

    # Create reversed copy
    if isinstance(collection, Vector):
        return Vector(collection[::-1])
    else:  # LispyList
        return LispyList(collection[::-1])


@lispy_documentation("reverse")
def reverse_documentation() -> str:
    """Returns documentation for the reverse function."""
    return """Function: reverse
Arguments: (reverse collection)
Description: Returns a new collection with elements in reverse order.

Examples:
  (reverse [1 2 3 4])           ; => [4 3 2 1]
  (reverse '(a b c d))          ; => (d c b a)
  (reverse [])                  ; => []
  (reverse '())                 ; => ()
  (reverse [42])                ; => [42] (single element)
  (reverse ["apple" "banana"])  ; => ["banana" "apple"]
  (reverse [1 "hi" true])       ; => [true "hi" 1] (mixed types)

Notes:
  - Requires exactly one argument
  - Argument must be a vector or list
  - Returns same collection type as input (vector -> vector, list -> list)
  - Original collection is not modified (immutable operation)
  - Empty collections return empty collections
  - Works with any element types including mixed types
  - Useful for processing collections in reverse order
  - Can be chained with other collection functions"""

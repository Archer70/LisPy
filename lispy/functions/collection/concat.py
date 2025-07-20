from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector
from lispy.functions.decorators import lispy_function, lispy_documentation


@lispy_function("concat")
def concat(args, env):
    """Concatenate multiple collections into a single collection.

    Usage: (concat collection1 collection2 ...)

    Args:
        collection1, collection2, ...: Vectors or lists to concatenate

    Returns:
        A new collection of the same type as the first argument containing
        all elements from the input collections in order

    Examples:
        (concat [1 2] [3 4] [5]) => [1 2 3 4 5]
        (concat '(1 2) '(3 4) '(5)) => (1 2 3 4 5)
        (concat [1 2] '(3 4)) => [1 2 3 4]  ; Result type matches first arg
        (concat) => []  ; Empty concat returns empty vector
    """
    if len(args) == 0:
        # Empty concat returns empty vector by convention
        return Vector([])

    # Determine result type from first argument
    first_collection = args[0]

    # Validate that first argument is a collection
    if not isinstance(first_collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'concat' arguments must be lists or vectors, got {type(first_collection)} as first argument."
        )

    # Determine result type
    result_type = Vector if isinstance(first_collection, Vector) else LispyList

    # Collect all elements from all collections
    all_elements = []

    for i, collection in enumerate(args):
        # Validate each argument
        if not isinstance(collection, (LispyList, Vector)):
            raise EvaluationError(
                f"TypeError: 'concat' arguments must be lists or vectors, got {type(collection)} at position {i}."
            )

        # Add all elements from this collection
        all_elements.extend(collection)

    return result_type(all_elements)


@lispy_documentation("concat")
def concat_documentation() -> str:
    """Returns documentation for the concat function."""
    return """Function: concat
Arguments: (concat collection1 collection2 ...)
Description: Concatenates multiple collections into a single collection.

Examples:
  (concat)                      ; => [] (empty returns empty vector)
  (concat [1 2] [3 4])          ; => [1 2 3 4]
  (concat '(1 2) '(3 4))        ; => (1 2 3 4)
  (concat [1] [2 3] [4 5 6])    ; => [1 2 3 4 5 6]
  (concat [1 2] '(3 4) [5])     ; => [1 2 3 4 5] (mixed types)
  (concat [] [1 2] [])          ; => [1 2] (empty collections ignored)
  (concat ["a" "b"] ["c"])      ; => ["a" "b" "c"]

Notes:
  - Accepts zero or more collection arguments
  - All arguments must be vectors or lists
  - Result type matches the type of first argument (vector or list)
  - Empty concat returns empty vector []
  - Original collections are not modified (immutable operation)
  - Mixed collection types allowed, result follows first argument type
  - Empty collections in arguments are simply ignored
  - Essential for building larger collections from smaller parts"""

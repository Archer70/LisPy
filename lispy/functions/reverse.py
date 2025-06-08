from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector


def reverse_fn(args, env):
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

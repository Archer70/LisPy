from lispy.types import LispyList, Vector
from lispy.exceptions import EvaluationError

def builtin_rest(args):
    """Implementation of the (rest coll) LisPy function.
    Returns a new list or vector containing all but the first item.
    Returns an empty collection of the same type if the input is empty or has one element.
    Usage: (rest collection)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'rest' expects 1 argument, got {len(args)}.")

    collection = args[0]

    if isinstance(collection, LispyList):
        if len(collection) <= 1:
            return LispyList([])
        else:
            return LispyList(collection[1:])
    elif isinstance(collection, Vector):
        if len(collection) <= 1:
            return Vector([])
        else:
            return Vector(collection[1:])
    elif collection is None: # (rest nil) should probably return nil or an empty list
        return LispyList([]) # Consistent with (first nil) behavior, (rest nil) is '() for Clojure
    else:
        raise EvaluationError(f"TypeError: 'rest' expects a list, vector, or nil, got {type(collection)}.") # Updated error message 
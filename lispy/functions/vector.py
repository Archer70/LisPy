from lispy.types import Vector
# No EvaluationError needed here as (vector ...) doesn't have argument count restrictions
# or specific type restrictions for its elements beyond what the evaluator provides.

def builtin_vector(args):
    """Implementation of the (vector ...) LisPy function.
    Creates a new vector containing the evaluated arguments.
    Usage: (vector item1 item2 ...)
    """
    # The arguments in 'args' are already evaluated by the evaluator
    # before being passed to a built-in function.
    return Vector(list(args)) # Convert tuple of args to list, then to Vector 
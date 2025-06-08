from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector


def concat_fn(args, env):
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
        raise EvaluationError(f"TypeError: 'concat' arguments must be lists or vectors, got {type(first_collection)} as first argument.")
    
    # Determine result type
    result_type = Vector if isinstance(first_collection, Vector) else LispyList
    
    # Collect all elements from all collections
    all_elements = []
    
    for i, collection in enumerate(args):
        # Validate each argument
        if not isinstance(collection, (LispyList, Vector)):
            raise EvaluationError(f"TypeError: 'concat' arguments must be lists or vectors, got {type(collection)} at position {i}.")
        
        # Add all elements from this collection
        all_elements.extend(collection)
    
    return result_type(all_elements) 
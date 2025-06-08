from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector, Symbol


def str_fn(args, env):
    """Convert a value to its string representation.

    Usage: (str value)

    Args:
        value: The value to convert to a string

    Returns:
        A string representation of the input value

    Examples:
        (str 42) => "42"
        (str 3.14) => "3.14"
        (str true) => "true"
        (str false) => "false"
        (str nil) => "nil"
        (str "hello") => "hello"  ; Pass through
        (str [1 2 3]) => "[1 2 3]"
        (str '(a b c)) => "(a b c)"
        (str ':keyword) => ":keyword"
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'str' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    # Handle different types
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return value  # Pass through strings unchanged
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, Symbol):
        return value.name  # Return the symbol name
    elif isinstance(value, Vector):
        # Use the Vector's __repr__ method which gives "[1 2 3]" format
        return repr(value)
    elif isinstance(value, LispyList):
        # Use the LispyList's __repr__ method which gives "(1 2 3)" format
        return repr(value)
    elif isinstance(value, dict):
        # For hash maps, create a simple representation
        items = []
        for k, v in value.items():
            key_str = str_fn([k], env) if hasattr(k, "name") else str(k)
            val_str = str_fn([v], env)
            items.append(f"{key_str} {val_str}")
        return "{" + " ".join(items) + "}"
    else:
        # Fallback to Python's str() for any other types
        return str(value)

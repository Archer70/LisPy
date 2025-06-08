from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector


def join_fn(args, env):
    """Join a collection of strings with a separator.

    Usage: (join collection separator)

    Args:
        collection: A vector or list of strings to join
        separator: A string to use as separator between elements

    Returns:
        A string with all elements joined by the separator

    Examples:
        (join ["a" "b" "c"] " ") => "a b c"
        (join '("apple" "banana" "cherry") ", ") => "apple, banana, cherry"
        (join ["h" "e" "l" "l" "o"] "") => "hello"
        (join [] "-") => ""  ; Empty collection returns empty string
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'join' expects 2 arguments, got {len(args)}."
        )

    collection, separator = args

    # Validate collection is a list or vector
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'join' first argument must be a list or vector, got {type(collection)}."
        )

    # Validate separator is a string
    if not isinstance(separator, str):
        raise EvaluationError(
            f"TypeError: 'join' second argument (separator) must be a string, got {type(separator)}."
        )

    # Validate all elements in collection are strings
    for i, element in enumerate(collection):
        if not isinstance(element, str):
            raise EvaluationError(
                f"TypeError: All elements in collection must be strings, got {type(element)} at position {i}."
            )

    # Join the strings
    return separator.join(collection)


def documentation_join() -> str:
    """Returns documentation for the join function."""
    return """Function: join
Arguments: (join collection separator)
Description: Joins a collection of strings into a single string using a separator.

Examples:
  (join ["a" "b" "c"] " ")      ; => "a b c"
  (join '("apple" "banana") ", ") ; => "apple, banana"
  (join ["h" "e" "l" "l" "o"] "") ; => "hello"
  (join [] "-")                 ; => "" (empty collection)
  (join ["single"] "|")         ; => "single"
  (join ["1" "2" "3"] "-")      ; => "1-2-3"

Notes:
  - Requires exactly 2 arguments
  - First argument must be a list or vector of strings
  - Second argument must be a string (the separator)
  - All elements in collection must be strings
  - Empty collection returns empty string
  - Single element returns that element (no separator added)
  - Essential for building formatted output strings
  - Useful for CSV generation, path building, etc.
  - Complement of the split function"""

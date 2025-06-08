from lispy.exceptions import EvaluationError


def append_fn(args, env):
    """Append multiple strings into a single string.

    Usage: (append string1 string2 ...)

    Args:
        string1, string2, ...: Strings to concatenate

    Returns:
        A new string containing all input strings concatenated in order

    Examples:
        (append "Hello" " " "World") => "Hello World"
        (append "a" "b" "c") => "abc"
        (append) => ""  ; Empty append returns empty string
        (append "only") => "only"  ; Single string returns itself
    """
    if len(args) == 0:
        # Empty append returns empty string
        return ""

    # Validate all arguments are strings
    for i, arg in enumerate(args):
        if not isinstance(arg, str):
            raise EvaluationError(
                f"TypeError: 'append' arguments must be strings, got {type(arg)} at position {i}."
            )

    # Concatenate all strings
    return "".join(args)

from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("append")
def append_func(args: List[Any], env: Environment) -> str:
    """(append str1 str2 ...)
    Concatenates all arguments as strings.
    With no arguments, returns empty string.
    """
    # Handle empty case
    if len(args) == 0:
        return ""
    
    # Concatenate all arguments as strings
    result = ""
    for arg in args:
        if arg is None:
            # nil contributes nothing (empty string)
            continue
        else:
            # Convert to string and append
            result += str(arg)
    
    return result


@lispy_documentation("append")
def append_documentation() -> str:
    return """Function: append
Arguments: (append [string1 string2 ...])
Description: Concatenates all arguments as strings.

Examples:
  (append)                     ; => ""
  (append "hello")             ; => "hello"
  (append "hello" "world")     ; => "helloworld"
  (append "a" "b" "c" "d")     ; => "abcd"
  (append "Hello" " " "World") ; => "Hello World"
  (append "start" "" "end")    ; => "startend"
  (append 1 2 3)               ; => "123"
  (append "Count: " 42)        ; => "Count: 42"

Notes:
  - Zero arguments returns empty string
  - All arguments are converted to strings before concatenation
  - nil arguments are ignored (contribute nothing)
  - Non-string arguments are converted using str()
  - Useful for building strings dynamically
  - Different from string concatenation operator in some languages"""

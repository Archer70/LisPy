from typing import List, Any, Callable
# from lispy.evaluator import evaluate # Removed to break circular import
from lispy.exceptions import EvaluationError, AssertionFailure
from lispy.environment import Environment

# Forward declaration or a way to access the currently executing evaluate function
# This is tricky. Python's closures and module system usually handle this if not for the circular import.
# One common way is to have lispy.evaluator pass itself (or a reference) if truly needed,
# or to structure calls so this isn't an issue.

# For now, let's assume that when this handler is called by the main `evaluate` function
# in lispy.evaluator, that `evaluate` is in a scope that can be resolved.
# Python's LEGB rule (Local, Enclosing function locals, Global, Built-in)
# If `evaluate` is imported at the top of `lispy.special_forms.bdd` or `lispy.special_forms`
# it might work, but that doesn't solve the circularity with `lispy.evaluator` directly.

# The most direct fix for circular imports of this type is often to move the import
# to be local to the function if it's only used there, or to refactor.
# However, `evaluate` is central. 

# Let's try relying on the fact that `evaluate` is in the global scope of the `lispy.evaluator` module,
# and when `assert_raises_q_form_handler` is executed, that `evaluate` will be found.
# This means the `evaluate` calls inside this function will implicitly refer to `lispy.evaluator.evaluate`.


def assert_raises_q_form_handler(expression: List[Any], env: Environment, evaluate_fn: Callable) -> bool:
    """(assert-raises? <expected-error-message-string> <form-to-execute>)
    Special form. Asserts that evaluating <form-to-execute> in the current environment
    raises an EvaluationError with a message containing <expected-error-message-string>.
    
    `expression` is the full S-expression, e.g. (assert-raises? "msg" (form)).
    `evaluate_fn` is the evaluator's main evaluate function.
    """
    # expression[0] is 'assert-raises?' symbol
    # expression[1] is expected_message_expr
    # expression[2] is form_to_execute
    if len(expression) != 3: # (assert-raises? msg form)
        raise EvaluationError(
            f"SyntaxError: 'assert-raises?' expects 2 arguments (expected-message form), got {len(expression) - 1}."
        )

    expected_message_expr = expression[1]
    try:
        expected_message_str = evaluate_fn(expected_message_expr, env)
    except EvaluationError as ee:
        raise EvaluationError(
            f"SyntaxError: 'assert-raises?' could not evaluate its first argument (expected-message): {ee}"
        ) from ee

    if not isinstance(expected_message_str, str):
        raise EvaluationError(
            f"TypeError: 'assert-raises?' expects its first argument (expected-message) to be a string, "
            f"but it evaluated to type {type(expected_message_str).__name__}."
        )

    form_to_execute = expression[2]

    try:
        evaluate_fn(form_to_execute, env)
        raise AssertionFailure(
            f"Assertion Failed: Expected an EvaluationError with message containing '{expected_message_str}', but no error was raised."
        )
    except EvaluationError as ee:
        actual_message = str(ee)
        if expected_message_str in actual_message:
            return True
        else:
            raise AssertionFailure(
                f"Assertion Failed: Expected EvaluationError message containing '{expected_message_str}', but got '{actual_message}'."
            )
    except AssertionFailure:
        raise
    except Exception as e:
        raise AssertionFailure(
            f"Assertion Failed: Expected an EvaluationError, but a different exception was raised: {type(e).__name__}: {str(e)}"
        )

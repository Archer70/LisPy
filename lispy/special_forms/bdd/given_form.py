# lispy/special_forms/bdd/given_form.py

from lispy.exceptions import EvaluationError
from lispy.bdd import registry
from typing import List as TypingList, Any


def given_form_handler(expression: TypingList[Any], env: Any, evaluate_fn: Any) -> Any:
    """Handles the (given \"description\" ...body) special form."""
    if not registry.is_scenario_context_active():
        raise EvaluationError(
            "SyntaxError: 'given' form can only be used inside an 'it' block."
        )

    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'given' expects at least a description string, got 0 arguments."
        )

    description_str = expression[1]
    if not isinstance(description_str, str):
        raise EvaluationError(
            "SyntaxError: 'given' expects a description string as its first argument."
        )

    # print(f"    [BDD Given]: {description_str}") # For future use

    registry.add_step("Given", description_str)  # Status defaults to "passed"

    last_result = None
    body_expressions = expression[2:]
    if not body_expressions:
        return None  # No body, returns nil (None)

    # If an error occurs here, it will propagate.
    # The test runner will later interpret this as a step failure.
    for expr in body_expressions:
        last_result = evaluate_fn(expr, env)
    return last_result

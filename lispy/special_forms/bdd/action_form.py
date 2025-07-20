from typing import Any
from typing import List as TypingList

from lispy.bdd import registry
from lispy.exceptions import EvaluationError


def action_form_handler(expression: TypingList[Any], env: Any, evaluate_fn: Any) -> Any:
    """Handles the (action \"description\" ...body) special form."""
    if not registry.is_scenario_context_active():
        raise EvaluationError(
            "SyntaxError: 'action' form can only be used inside an 'it' block."
        )

    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'action' expects at least a description string, got 0 arguments."
        )

    description_str = expression[1]
    if not isinstance(description_str, str):
        raise EvaluationError(
            "SyntaxError: 'action' expects a description string as its first argument."
        )

    registry.add_step("Action", description_str)

    last_result = None
    body_expressions = expression[2:]

    if not body_expressions:
        return None

    for expr in body_expressions:
        last_result = evaluate_fn(expr, env)

    return last_result

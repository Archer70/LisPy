from lispy.exceptions import EvaluationError
from lispy.bdd import registry
from typing import List as TypingList, Any


def it_form_handler(expression: TypingList[Any], env: Any, evaluate_fn: Any) -> Any:
    """Handles the (it \"description\" ...body) special form."""
    if not registry.is_feature_context_active():
        raise EvaluationError(
            "SyntaxError: 'it' form can only be used inside a 'describe' block."
        )

    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'it' expects at least a description string, got 0 arguments."
        )

    description_str = expression[1]
    if not isinstance(description_str, str):
        raise EvaluationError(
            "SyntaxError: 'it' expects a description string as its first argument."
        )

    registry.start_scenario(description_str)
    last_result = None
    try:
        body_expressions = expression[2:]
        if not body_expressions:
            return None

        for expr in body_expressions:
            last_result = evaluate_fn(expr, env)

        return last_result
    finally:
        registry.end_scenario()

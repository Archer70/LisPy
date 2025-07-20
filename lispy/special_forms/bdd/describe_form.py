# lispy/special_forms/bdd/describe_form.py

from typing import Any
from typing import List as TypingList

from lispy.bdd import registry
from lispy.exceptions import EvaluationError


def describe_form_handler(
    expression: TypingList[Any], env: Any, evaluate_fn: Any
) -> Any:
    """Handles the (describe \"description\" ...body) special form."""
    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'describe' expects at least a description string, got 0 arguments."
        )

    description_str = expression[1]
    if not isinstance(description_str, str):
        raise EvaluationError(
            "SyntaxError: 'describe' expects a description string as its first argument."
        )

    registry.start_feature(description_str)
    last_result = None
    try:
        body_expressions = expression[2:]
        if not body_expressions:
            return None

        for expr in body_expressions:
            last_result = evaluate_fn(expr, env)

        return last_result
    finally:
        registry.end_feature()

from lispy.exceptions import EvaluationError, AssertionFailure
from lispy.bdd import registry
from typing import List as TypingList, Any


def then_form_handler(expression: TypingList[Any], env: Any, evaluate_fn: Any) -> Any:
    """Handles the (then \"description\" ...body) special form."""
    if not registry.is_scenario_context_active():
        raise EvaluationError(
            "SyntaxError: 'then' form can only be used inside an 'it' block."
        )

    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'then' expects at least a description string, got 0 arguments."
        )

    description_str = expression[1]
    if not isinstance(description_str, str):
        raise EvaluationError(
            "SyntaxError: 'then' expects a description string as its first argument."
        )
    
    # print(f"    [BDD Then]: {description_str}") # For future use

    # Add step initially. If body evaluation fails, exception propagates.
    # The runner will mark this step as failed based on the exception.
    registry.add_step("Then", description_str) # Added, status defaults to "passed"

    last_result = None
    body_expressions = expression[2:]
    if not body_expressions:
        # A `then` block usually should have a body (assertions).
        # We could make this an error, or the runner could flag it.
        # For now, allow it to be 'passed' if empty.
        return None 

    try:
        for expr in body_expressions:
            last_result = evaluate_fn(expr, env)
        return last_result
    except AssertionFailure as af:
        registry.mark_last_step_status("failed", str(af))
        return None # Indicates handled assertion failure
    except EvaluationError as ee:
        registry.mark_last_step_status("failed", f"Step error: {str(ee)}")
        return None
    except Exception as e:
        registry.mark_last_step_status("failed", f"Unexpected critical error: {str(e)}")
        raise # Re-raise other critical errors

# Removed the final unreachable: return last_result 
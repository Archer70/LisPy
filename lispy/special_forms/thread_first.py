from ..types import Symbol, LispyList, Vector
from ..exceptions import EvaluationError

def handle_thread_first(expression, env, evaluate_fn):
    """Handles the (-> initial_value step1 step2 ...) special form.

    Args:
        expression: The full (-> ...) Lisp expression (a LispyList).
        env: The current environment for evaluation.
        evaluate_fn: The main evaluate function to call for evaluating sub-expressions.

    Returns:
        The result of the pipeline.
    """
    if len(expression) < 2:
        raise EvaluationError("SyntaxError: '->' special form expects at least an initial value.")

    # The first element is '->', the second is the initial value.
    # The rest are the steps in the pipeline.
    initial_value_expr = expression[1]
    pipeline_steps = expression[2:]

    # Evaluate the initial value
    current_value = evaluate_fn(initial_value_expr, env)

    # Sequentially apply each step in the pipeline
    for step_form in pipeline_steps:
        # If current_value is a data structure that would be re-evaluated as code, 
        # we need to protect it with a quote
        if isinstance(current_value, (LispyList, list)) and current_value:
            # Wrap in quote to prevent re-evaluation
            protected_value = LispyList([Symbol('quote'), current_value])
        else:
            # Safe to use directly (primitives, vectors, etc.)
            protected_value = current_value
            
        if isinstance(step_form, Symbol):
            # If the step is a symbol, it's a function call with no other arguments.
            # Construct (function_symbol current_value)
            new_expr_to_eval = LispyList([step_form, protected_value])
        elif isinstance(step_form, LispyList):
            # If the step is a list (func arg1 arg2 ...),
            # insert current_value as the first argument to that function call.
            # (func current_value arg1 arg2 ...)
            if not step_form: # Empty list in pipeline is invalid
                raise EvaluationError("SyntaxError: Invalid empty list () found in '->' pipeline.")
            
            new_expr_to_eval = LispyList([step_form[0]] + [protected_value] + step_form[1:])
        else:
            # The step is not a recognized form (Symbol or List for a function call)
            raise EvaluationError(
                f"TypeError: Invalid form in '->' pipeline. Expected function or (function ...), got {type(step_form)}: {step_form}"
            )
        
        # Evaluate the newly constructed expression
        current_value = evaluate_fn(new_expr_to_eval, env)
        
    return current_value 
"""
Thread-last special form for data pipeline processing.

The thread-last form (->>)  threads values through a series of function calls,
inserting the value as the LAST argument to each function call.

Usage: (->> initial_value step1 step2 ...)

Examples:
    (->> [1 2 3 4]
         (conj 5)
         (conj 6))
    ; => [1 2 3 4 5 6]

    (->> 10
         (- 100)
         (* 2))
    ; => (* 2 (- 100 10)) => (* 2 90) => 180
"""

from ..types import Symbol, LispyList
from ..exceptions import EvaluationError


def documentation_thread_last():
    """Returns documentation for the '->>' special form."""
    return """Special Form: ->>
Arguments: (->> initial-value step1 step2 ...)
Description: Thread-last macro - pipes initial value as last argument through function calls.

Examples:
  (->> 5 (- 10) (* 2))            ; Returns 10: (* 2 (- 10 5))
  (->> [1 2] (conj 3) (conj 4))   ; Returns [1 2 3 4] (last arg threading)
  (->> "world" (str "hello "))    ; Returns "hello world"
  (->> {:a 1} (merge {:b 2}))     ; Returns {:a 1 :b 2}
  (->> items (filter odd?) (map inc))  ; Chain collection operations

Step Forms:
  Symbol:     (->> x f)           ; Becomes (f x)
  List:       (->> x (f a b))     ; Becomes (f a b x)

Notes:
  - Threads value as LAST argument to each function
  - Ideal for collection processing pipelines
  - Each step receives the result of the previous step
  - Particularly useful with functions expecting collections as last arg

See Also: ->, map, filter"""


def handle_thread_last(expression, env, evaluate_fn):
    """Handles the (->> initial_value step1 step2 ...) special form.

    Args:
        expression: The full (->> ...) Lisp expression (a LispyList).
        env: The current environment for evaluation.
        evaluate_fn: The main evaluate function to call for evaluating sub-expressions.

    Returns:
        The result of the pipeline.
    """
    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: '->>' special form expects at least an initial value."
        )

    # The first element is '->>', the second is the initial value.
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
            protected_value = LispyList([Symbol("quote"), current_value])
        else:
            # Safe to use directly (primitives, vectors, etc.)
            protected_value = current_value

        if isinstance(step_form, Symbol):
            # If the step is a symbol, it's a function call with no other arguments.
            # Construct (function_symbol current_value)
            new_expr_to_eval = LispyList([step_form, protected_value])
        elif isinstance(step_form, LispyList):
            # If the step is a list (func arg1 arg2 ...),
            # append current_value as the LAST argument to that function call.
            # (func arg1 arg2 ... current_value)
            if not step_form:  # Empty list in pipeline is invalid
                raise EvaluationError(
                    "SyntaxError: Invalid empty list () found in '->>' pipeline."
                )

            # Thread as last argument: [func, arg1, arg2, ...] + [current_value]
            new_expr_to_eval = LispyList(list(step_form) + [protected_value])
        else:
            # The step is not a recognized form (Symbol or List for a function call)
            raise EvaluationError(
                f"TypeError: Invalid form in '->>' pipeline. Expected function or (function ...), got {type(step_form)}: {step_form}"
            )

        # Evaluate the newly constructed expression
        current_value = evaluate_fn(new_expr_to_eval, env)

    return current_value

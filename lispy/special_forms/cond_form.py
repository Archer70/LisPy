from lispy.exceptions import EvaluationError


def documentation_cond():
    """Returns documentation for the 'cond' special form."""
    return """Special Form: cond
Arguments: (cond test1 result1 test2 result2 ... testN resultN)
Description: Multi-way conditional that evaluates test-result pairs in order.

Examples:
  (cond 
    (< x 0) "negative"
    (= x 0) "zero" 
    (> x 0) "positive")              ; Returns based on x value
  (cond 
    (empty? lst) "empty"
    (= (count lst) 1) "single"
    true "multiple")                 ; Use 'true' as catch-all
  (cond 
    (> grade 90) "A"
    (> grade 80) "B"
    (> grade 70) "C"
    true "F")                        ; Grade assignment

Notes:
  - Evaluates test-result pairs from left to right
  - Returns result of first truthy test
  - If no test is truthy, returns nil
  - Must have even number of arguments (test-result pairs)
  - Use 'true' or other truthy value as final catch-all test
  - More readable than nested 'if' statements

See Also: if, when, case"""


def handle_cond(expression, env, evaluate_fn):
    """Handle the cond special form for multi-way conditionals.

    Usage: (cond test1 result1 test2 result2 ... testN resultN)

    Evaluates test expressions in order until one is truthy,
    then returns the corresponding result expression.
    If no test matches, returns None.

    Examples:
        (cond
          (< x 0) "negative"
          (= x 0) "zero"
          (> x 0) "positive")

        (cond
          (empty? coll) "empty collection"
          (= (count coll) 1) "single item"
          :else "multiple items")  ; :else is always truthy
    """
    # expression is ['cond', test1, result1, test2, result2, ...]
    args = expression[1:]  # Skip the 'cond' symbol

    # Check that we have an even number of arguments (test-result pairs)
    if len(args) % 2 != 0:
        raise EvaluationError(
            "SyntaxError: 'cond' requires an even number of arguments (test-result pairs)."
        )

    if len(args) == 0:  # Need at least one test-result pair
        raise EvaluationError(
            "SyntaxError: 'cond' requires at least one test-result pair."
        )

    # Process test-result pairs
    for i in range(0, len(args), 2):
        test_expr = args[i]
        result_expr = args[i + 1]

        # Evaluate the test expression
        test_value = evaluate_fn(test_expr, env)

        # Check if test is truthy (anything except False and None is truthy)
        if test_value is not False and test_value is not None:
            # Test passed, evaluate and return the result expression
            return evaluate_fn(result_expr, env)

    # No test matched, return None
    return None

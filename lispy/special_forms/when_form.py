from lispy.exceptions import EvaluationError


def documentation_when():
    """Returns documentation for the 'when' special form."""
    return """Special Form: when
Arguments: (when test-expr body-expr1 body-expr2 ...)
Description: Conditional execution - evaluates body expressions only if test is truthy.

Examples:
  (when (> x 0) (print "positive"))     ; Prints only if x > 0
  (when debug-mode (log "debug info"))  ; Conditional logging
  (when (> x 0) 
    (print "x is positive") 
    (* x 2))                           ; Returns (* x 2) if x > 0, else nil
  (when false (print "never"))          ; Returns nil, doesn't print

Notes:
  - Returns nil if test is falsy (false or nil)
  - If test is truthy, evaluates all body expressions in sequence
  - Returns the value of the last body expression
  - If no body expressions and test is truthy, returns the test value
  - Like 'if' but for multiple expressions without an else clause

See Also: if, cond"""


def handle_when_form(expression, env, evaluate_fn):
    """Handle the when special form for conditional execution of multiple expressions.

    Usage: (when test expr1 expr2 ... exprN)

    If test is truthy, evaluates all expressions in sequence and returns
    the value of the last expression. If test is falsy, returns None
    without evaluating any expressions.

    Examples:
        (when (> x 0)
          (println "x is positive")
          (increment-counter)
          x)

        (when debug-mode
          (log "Debug info")
          (dump-state))
    """
    # expression is ['when', test, expr1, expr2, ...]
    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'when' requires at least a test expression."
        )

    test_expr = expression[1]
    body_exprs = expression[2:]  # All expressions after the test

    # Evaluate the test expression
    test_value = evaluate_fn(test_expr, env)

    # Check if test is truthy (anything except False and None is truthy)
    if test_value is not False and test_value is not None:
        # Test is truthy, evaluate all body expressions in sequence
        if not body_exprs:
            # No body expressions, just return the test value
            return test_value

        result = None
        for expr in body_exprs:
            result = evaluate_fn(expr, env)
        return result  # Return the value of the last expression
    else:
        # Test is falsy, return None without evaluating body
        return None

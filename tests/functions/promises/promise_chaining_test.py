import unittest
from lispy.evaluator import evaluate
from lispy.parser import parse
from lispy.functions import global_env
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


def run_lispy_string(code_string, env=None):
    """Helper function to parse and evaluate LisPy code."""
    if env is None:
        env = global_env
    from lispy.lexer import tokenize

    tokens = tokenize(code_string)
    parsed_expr = parse(tokens)
    return evaluate(parsed_expr, env)


class TestPromiseChainingFunctions(unittest.TestCase):
    """Test cases for promise chaining functions: then, on-reject, on-complete."""

    def setUp(self):
        """Set up test environment."""
        self.env = global_env

    def test_then_basic_transformation(self):
        """Test basic value transformation with promise-then."""
        # Test with resolved promise
        result = run_lispy_string(
            "(promise-then (resolve 10) (fn [x] (* x 2)))", self.env
        )
        self.assertIsInstance(result, LispyPromise)

        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 20)

    def test_then_chaining_multiple(self):
        """Test chaining multiple promise-then operations."""
        code = """
        (-> (resolve 5)
            (promise-then (fn [x] (+ x 3)))
            (promise-then (fn [x] (* x 2)))
            (promise-then (fn [x] (- x 1))))
        """
        result = run_lispy_string(code, self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        # ((5 + 3) * 2) - 1 = 15
        self.assertEqual(result.value, 15)

    def test_then_with_rejected_promise(self):
        """Test that promise-then is not called when promise is rejected."""
        result = run_lispy_string(
            '(promise-then (reject "error") (fn [x] (* x 2)))', self.env
        )
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")

    def test_then_argument_validation(self):
        """Test promise-then function argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(promise-then (resolve 42))", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-then' expects 2 arguments (promise callback), got 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(promise-then (resolve 42) (fn [x] x) "extra")', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-then' expects 2 arguments (promise callback), got 3.",
        )

        # First argument not a promise
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(promise-then 42 (fn [x] x))", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' first argument must be a promise, got int.",
        )

        # Second argument not a function
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(promise-then (resolve 42) "not-a-function")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' second argument must be a function, got str.",
        )

    def test_on_reject_basic_error_handling(self):
        """Test basic error handling with on-reject."""
        result = run_lispy_string(
            '(on-reject (reject "error") (fn [err] (append "Handled: " (str err))))',
            self.env,
        )
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "Handled: error")

    def test_on_reject_with_resolved_promise(self):
        """Test that on-reject is not called when promise resolves."""
        result = run_lispy_string(
            '(on-reject (resolve 42) (fn [err] "not called"))', self.env
        )
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

    def test_on_reject_chaining_with_then(self):
        """Test chaining on-reject with promise-then operations."""
        code = """
        (-> (reject "network-error")
            (on-reject (fn [err] "fallback-data"))
            (promise-then (fn [data] (append "Result: " (str data)))))
        """
        result = run_lispy_string(code, self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "Result: fallback-data")

    def test_on_reject_argument_validation(self):
        """Test on-reject function argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-reject (reject "error"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-reject' expects 2 arguments (promise error-callback), got 1.",
        )

        # First argument not a promise
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-reject "not-promise" (fn [x] x))', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' first argument must be a promise, got str.",
        )

        # Second argument not a function
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-reject (reject "error") 42)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' second argument must be a function, got int.",
        )

    def test_on_complete_with_resolved_promise(self):
        """Test on-complete with a resolved promise."""
        # Note: This test is tricky because on-complete is for side effects
        # We'll test that the promise resolves with the original value
        result = run_lispy_string("(on-complete (resolve 42) (fn [p] nil))", self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

    def test_on_complete_with_rejected_promise(self):
        """Test on-complete with a rejected promise."""
        result = run_lispy_string(
            '(on-complete (reject "error") (fn [p] nil))', self.env
        )
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")

    def test_on_complete_argument_validation(self):
        """Test on-complete function argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(on-complete (resolve 42))", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-complete' expects 2 arguments (promise cleanup-callback), got 1.",
        )

        # First argument not a promise
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(on-complete 42 (fn [x] x))", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' first argument must be a promise, got int.",
        )

        # Second argument not a function
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete (resolve 42) "not-function")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' second argument must be a function, got str.",
        )

    def test_complex_promise_chain(self):
        """Test a complex promise chain with all three functions."""
        code = """
        (-> (resolve 10)
            (promise-then (fn [x] 
              (if (> x 5) 
                x 
                (throw "too small"))))
            (promise-then (fn [x] (* x 2)))
            (on-reject (fn [err] 0))
            (on-complete (fn [p] nil))
            (promise-then (fn [x] (+ x 1))))
        """
        result = run_lispy_string(code, self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        # 10 > 5, so 10 * 2 = 20, then 20 + 1 = 21
        self.assertEqual(result.value, 21)

    def test_error_recovery_chain(self):
        """Test error recovery using on-reject."""
        code = """
        (-> (reject "primary-failed")
            (on-reject (fn [err] "backup-data"))
            (promise-then (fn [data] (append "Using: " (str data)))))
        """
        result = run_lispy_string(code, self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "Using: backup-data")

    def test_callback_parameter_validation(self):
        """Test that callbacks must take exactly one parameter."""
        # promise-then callback with wrong parameter count
        with self.assertRaises(EvaluationError) as cm:
            code = '(promise-then (resolve 42) (fn [] "no params"))'
            result = run_lispy_string(code, self.env)
            # Let the promise execute
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' callback must take exactly 1 argument, got 0.",
        )

        # on-reject callback with wrong parameter count
        with self.assertRaises(EvaluationError) as cm:
            code = '(on-reject (reject "error") (fn [a b] "two params"))'
            result = run_lispy_string(code, self.env)
            # Let the promise execute
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' callback must take exactly 1 argument, got 2.",
        )

        # on-complete callback with wrong parameter count
        with self.assertRaises(EvaluationError) as cm:
            code = '(on-complete (resolve 42) (fn [] "no params"))'
            result = run_lispy_string(code, self.env)
            # Let the promise execute
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' callback must take exactly 1 argument, got 0.",
        )


if __name__ == "__main__":
    unittest.main()

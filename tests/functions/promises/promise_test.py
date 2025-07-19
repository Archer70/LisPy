import unittest
import time
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.functions.promises.promise import promise
from lispy.functions.promises.resolve import resolve
from lispy.functions.promises.reject import reject
from lispy.functions import create_global_env


class TestPromiseFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_promise_with_simple_function(self):
        """Test promise with a simple function."""

        def simple_fn(args, env):
            return 42

        result = promise([simple_fn], self.env)
        self.assertIsInstance(result, LispyPromise)

        # Wait for promise to resolve
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

    def test_promise_with_slow_function(self):
        """Test promise with a function that takes time."""

        def slow_fn(args, env):
            time.sleep(0.01)
            return "done"

        result = promise([slow_fn], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "pending")

        # Wait for promise to resolve
        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "done")

    def test_promise_with_error_function(self):
        """Test promise with a function that raises an error."""

        def error_fn(args, env):
            raise ValueError("Test error")

        result = promise([error_fn], self.env)
        self.assertIsInstance(result, LispyPromise)

        # Wait for promise to reject
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        self.assertEqual(str(result.error), "Test error")

    def test_promise_wrong_arg_count(self):
        """Test promise with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            promise([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise' expects 1 argument (function), got 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            promise([lambda: 1, lambda: 2], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise' expects 1 argument (function), got 2.",
        )

    def test_promise_non_callable_arg(self):
        """Test promise with non-callable argument."""
        with self.assertRaises(EvaluationError) as cm:
            promise([42], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise' argument must be a function, got int.",
        )

        with self.assertRaises(EvaluationError) as cm:
            promise(["string"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise' argument must be a function, got str.",
        )

    def test_resolve_with_value(self):
        """Test resolve with various values."""
        result = resolve([42], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

        result = resolve(["hello"], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "hello")

        result = resolve([[1, 2, 3]], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, [1, 2, 3])

    def test_resolve_wrong_arg_count(self):
        """Test resolve with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            resolve([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'resolve' expects 1 argument (value), got 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            resolve([1, 2], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'resolve' expects 1 argument (value), got 2.",
        )

    def test_reject_with_error(self):
        """Test reject with various error values."""
        result = reject(["error message"], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error message")

        result = reject([404], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, 404)

        result = reject([{"error": "not found"}], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, {"error": "not found"})

    def test_reject_wrong_arg_count(self):
        """Test reject with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            reject([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'reject' expects 1 argument (error), got 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            reject([1, 2], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'reject' expects 1 argument (error), got 2.",
        )

    def test_promise_chaining(self):
        """Test promise chaining with then."""

        def base_fn(args, env):
            return 10

        test_promise = promise([base_fn], self.env)

        # Chain with then
        chained = test_promise.then(lambda x: x * 2)

        # Wait for both to resolve
        time.sleep(0.01)

        self.assertEqual(promise.state, "resolved")
        self.assertEqual(promise.value, 10)
        self.assertEqual(chained.state, "resolved")
        self.assertEqual(chained.value, 20)

    def test_promise_error_handling(self):
        """Test promise error handling with catch."""

        def error_fn(args, env):
            raise ValueError("Test error")

        test_promise = promise([error_fn], self.env)

        # Handle error with catch
        handled = test_promise.catch(lambda e: f"Handled: {e}")

        # Wait for both to complete
        time.sleep(0.01)

        self.assertEqual(promise.state, "rejected")
        self.assertEqual(handled.state, "resolved")
        self.assertEqual(handled.value, "Handled: Test error")


if __name__ == "__main__":
    unittest.main()

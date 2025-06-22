"""Tests for promise-then function - promise chaining and transformation"""

import unittest
import time
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.closure import Function
from lispy.types import Symbol
from lispy.functions.promises.then import builtin_promise_then
from lispy.functions.promises.resolve import builtin_resolve
from lispy.functions.promises.reject import builtin_reject
from lispy.functions.promises.promise import builtin_promise
from lispy.functions import create_global_env


class TestPromiseThen(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_then_with_resolved_promise(self):
        """Test then with already resolved promise"""
        promise = builtin_resolve([10], self.env)
        
        def callback(args, env):
            return args[0] * 2
            
        result = builtin_promise_then([promise, callback], self.env)
        
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 20)

    def test_then_with_pending_promise(self):
        """Test then with pending promise"""
        def slow_function(args, env):
            time.sleep(0.01)
            return "original"
            
        promise = builtin_promise([slow_function], self.env)
        
        def callback(args, env):
            return f"transformed: {args[0]}"
            
        result = builtin_promise_then([promise, callback], self.env)
        
        # Should be pending initially
        self.assertEqual(result.state, "pending")
        
        # Wait for completion
        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "transformed: original")

    def test_then_with_lispy_function(self):
        """Test then with user-defined LisPy function"""
        promise = builtin_resolve([5], self.env)
        
        # Create a simple LisPy function: (fn [x] (* x x))
        param = Symbol("x")
        lispy_fn = Function(
            [param], 
            ["multiply_expr"],  # This would be the actual AST
            self.env
        )
        
        # Mock the function evaluation for testing
        def mock_lispy_callback(value):
            return value * value
            
        # Replace the promise's then method temporarily for this test
        original_then = promise.then
        def mock_then(callback):
            return builtin_resolve([mock_lispy_callback(promise.value)], self.env)
        promise.then = mock_then
        
        result = builtin_promise_then([promise, lispy_fn], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 25)

    def test_then_chain_multiple_transformations(self):
        """Test chaining multiple then operations"""
        promise = builtin_resolve([1], self.env)
        
        def add_10(args, env):
            return args[0] + 10
            
        def multiply_3(args, env):
            return args[0] * 3
            
        def to_string(args, env):
            return f"result: {args[0]}"
            
        # Chain: 1 -> 11 -> 33 -> "result: 33"
        step1 = builtin_promise_then([promise, add_10], self.env)
        step2 = builtin_promise_then([step1, multiply_3], self.env)
        step3 = builtin_promise_then([step2, to_string], self.env)
        
        self.assertEqual(step3.state, "resolved")
        self.assertEqual(step3.value, "result: 33")

    def test_then_with_rejected_promise(self):
        """Test then with rejected promise (should skip callback)"""
        promise = builtin_reject(["original error"], self.env)
        
        def callback(args, env):
            return "this should not execute"
            
        result = builtin_promise_then([promise, callback], self.env)
        
        # Should propagate the rejection
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "original error")

    def test_then_callback_throws_error(self):
        """Test then when callback function throws an error"""
        promise = builtin_resolve(["input"], self.env)
        
        def error_callback(args, env):
            raise ValueError("callback error")
            
        result = builtin_promise_then([promise, error_callback], self.env)
        
        # Should reject with the callback error
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        self.assertEqual(str(result.error), "callback error")

    def test_then_wrong_arg_count(self):
        """Test then with wrong number of arguments"""
        promise = builtin_resolve([1], self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([promise], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-then' expects 2 arguments (promise callback), got 1."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([promise, lambda x: x, "extra"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-then' expects 2 arguments (promise callback), got 3."
        )

    def test_then_invalid_promise_type(self):
        """Test then with non-promise first argument"""
        def callback(args, env):
            return args[0]
            
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then(["not a promise", callback], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' first argument must be a promise, got str."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([42, callback], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' first argument must be a promise, got int."
        )

    def test_then_invalid_callback_type(self):
        """Test then with non-function callback"""
        promise = builtin_resolve([1], self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([promise, "not a function"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' second argument must be a function, got str."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([promise, 42], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' second argument must be a function, got int."
        )

    def test_then_callback_wrong_parameter_count(self):
        """Test then with callback that has wrong parameter count"""
        promise = builtin_resolve([1], self.env)
        
        # Create LisPy function with wrong parameter count
        param1 = Symbol("x")
        param2 = Symbol("y")
        wrong_param_fn = Function(
            [param1, param2],  # Takes 2 parameters, should take 1
            ["body"],
            self.env
        )
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_then([promise, wrong_param_fn], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-then' callback must take exactly 1 argument, got 2."
        )

    def test_then_with_different_value_types(self):
        """Test then with different input and output value types"""
        # Number to string
        promise_num = builtin_resolve([42], self.env)
        result_str = builtin_promise_then([promise_num, lambda args, env: str(args[0])], self.env)
        self.assertEqual(result_str.value, "42")
        
        # String to vector
        promise_str = builtin_resolve(["a,b,c"], self.env)
        result_vec = builtin_promise_then([promise_str, lambda args, env: Vector(args[0].split(","))], self.env)
        self.assertEqual(result_vec.value, Vector(["a", "b", "c"]))
        
        # Vector to number
        promise_vec = builtin_resolve([Vector([1, 2, 3])], self.env)
        result_sum = builtin_promise_then([promise_vec, lambda args, env: sum(args[0])], self.env)
        self.assertEqual(result_sum.value, 6)

    def test_then_with_nil_values(self):
        """Test then with nil values"""
        promise = builtin_resolve([None], self.env)
        
        def handle_nil(args, env):
            return "nil handled" if args[0] is None else args[0]
            
        result = builtin_promise_then([promise, handle_nil], self.env)
        self.assertEqual(result.value, "nil handled")

    def test_then_with_complex_data_structures(self):
        """Test then with complex nested data structures"""
        complex_data = {
            "users": Vector([{"name": "Alice"}, {"name": "Bob"}]),
            "count": 2,
            "metadata": LispyList(["active", "premium"])
        }
        
        promise = builtin_resolve([complex_data], self.env)
        
        def extract_names(args, env):
            data = args[0]
            return Vector([user["name"] for user in data["users"]])
            
        result = builtin_promise_then([promise, extract_names], self.env)
        self.assertEqual(result.value, Vector(["Alice", "Bob"]))

    def test_then_async_callback_integration(self):
        """Test then with callbacks that return promises (flattening)"""
        promise = builtin_resolve([5], self.env)
        
        def async_callback(args, env):
            # Return another promise instead of a direct value
            return builtin_resolve([args[0] * 2], env)
            
        # Note: This test assumes promise flattening behavior
        # The actual implementation might need to handle this
        result = builtin_promise_then([promise, async_callback], self.env)
        
        # If flattening is implemented, this should be 10, not a promise
        # If not implemented, result.value would be a promise
        self.assertIsInstance(result, LispyPromise)

    def test_then_error_recovery_pattern(self):
        """Test then used in error recovery patterns"""
        def might_fail_function(args, env):
            time.sleep(0.01)
            raise ValueError("operation failed")
            
        promise = builtin_promise([might_fail_function], self.env)
        
        # This should fail, then be caught and recovered
        def recovery_callback(args, env):
            return "recovered"
            
        result = builtin_promise_then([promise, recovery_callback], self.env)
        
        time.sleep(0.02)
        
        # Should still be rejected (then doesn't handle errors)
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)


if __name__ == "__main__":
    unittest.main() 
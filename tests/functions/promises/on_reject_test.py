"""Tests for on-reject function - promise error handling"""

import time
import unittest

from lispy.closure import Function
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.functions.promises.on_reject import on_reject
from lispy.functions.promises.promise import promise
from lispy.functions.promises.reject import reject
from lispy.functions.promises.resolve import resolve
from lispy.types import LispyList, LispyPromise, Symbol, Vector


class TestOnReject(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_on_reject_with_rejected_promise(self):
        """Test on-reject with already rejected promise"""
        promise = reject(["test error"], self.env)

        def error_handler(args, env):
            return f"handled: {args[0]}"

        result = on_reject([promise, error_handler], self.env)

        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "handled: test error")

    def test_on_reject_with_resolved_promise(self):
        """Test on-reject with resolved promise (should pass through)"""
        promise = resolve(["success"], self.env)

        def error_handler(args, env):
            return "this should not execute"

        result = on_reject([promise, error_handler], self.env)

        # Should pass through original value
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "success")

    def test_on_reject_with_pending_promise_that_resolves(self):
        """Test on-reject with pending promise that eventually resolves"""

        def success_function(args, env):
            time.sleep(0.01)
            return "success result"

        promise_obj = promise([success_function], self.env)

        def error_handler(args, env):
            return "error handled"

        result = on_reject([promise_obj, error_handler], self.env)

        # Should be pending initially
        self.assertEqual(result.state, "pending")

        # Wait for completion - should resolve with original value
        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "success result")

    def test_on_reject_with_pending_promise_that_rejects(self):
        """Test on-reject with pending promise that eventually rejects"""

        def error_function(args, env):
            time.sleep(0.01)
            raise ValueError("async error")

        promise_obj = promise([error_function], self.env)

        def error_handler(args, env):
            return f"caught: {args[0]}"

        result = on_reject([promise_obj, error_handler], self.env)

        # Should be pending initially
        self.assertEqual(result.state, "pending")

        # Wait for completion - should resolve with handled error
        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "caught: async error")

    def test_on_reject_error_handler_throws(self):
        """Test on-reject when error handler itself throws an error"""
        promise = reject(["original error"], self.env)

        def failing_handler(args, env):
            raise RuntimeError("handler error")

        result = on_reject([promise, failing_handler], self.env)

        # Should reject with the handler error
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, RuntimeError)
        self.assertEqual(str(result.error), "handler error")

    def test_on_reject_with_different_error_types(self):
        """Test on-reject with different types of error values"""
        # String error
        promise1 = reject(["string error"], self.env)
        result1 = on_reject(
            [promise1, lambda args, env: f"handled: {args[0]}"], self.env
        )
        self.assertEqual(result1.value, "handled: string error")

        # Number error
        promise2 = reject([404], self.env)
        result2 = on_reject(
            [promise2, lambda args, env: f"error code: {args[0]}"], self.env
        )
        self.assertEqual(result2.value, "error code: 404")

        # Exception object error
        test_exception = ValueError("test exception")
        promise3 = reject([test_exception], self.env)
        result3 = on_reject(
            [promise3, lambda args, env: f"exception: {str(args[0])}"], self.env
        )
        self.assertEqual(result3.value, "exception: test exception")

        # Complex error data
        error_data = {
            "type": "ValidationError",
            "field": "email",
            "message": "invalid format",
        }
        promise4 = reject([error_data], self.env)
        result4 = on_reject([promise4, lambda args, env: args[0]["message"]], self.env)
        self.assertEqual(result4.value, "invalid format")

    def test_on_reject_chaining_with_then(self):
        """Test on-reject in chains with then"""
        promise = reject(["error"], self.env)

        def error_handler(args, env):
            return "recovered"

        def success_handler(args, env):
            return f"processed: {args[0]}"

        # Chain: reject -> on-reject (handles) -> then (processes)
        from lispy.functions.promises.then import promise_then

        recovered = on_reject([promise, error_handler], self.env)
        final_result = promise_then([recovered, success_handler], self.env)

        self.assertEqual(final_result.state, "resolved")
        self.assertEqual(final_result.value, "processed: recovered")

    def test_on_reject_multiple_handlers(self):
        """Test multiple on-reject handlers in chain"""
        promise = reject(["original"], self.env)

        def handler1(args, env):
            return f"first: {args[0]}"

        def handler2(args, env):
            return f"second: {args[0]}"

        # First handler should catch the error
        result1 = on_reject([promise, handler1], self.env)
        # Second handler should not be triggered (promise is now resolved)
        result2 = on_reject([result1, handler2], self.env)

        self.assertEqual(result1.state, "resolved")
        self.assertEqual(result1.value, "first: original")
        self.assertEqual(result2.state, "resolved")
        self.assertEqual(result2.value, "first: original")  # Passed through

    def test_on_reject_wrong_arg_count(self):
        """Test on-reject with wrong number of arguments"""
        promise = reject(["error"], self.env)

        with self.assertRaises(EvaluationError) as cm:
            on_reject([promise], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-reject' expects 2 arguments (promise error-callback), got 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            on_reject([promise, lambda x: x, "extra"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-reject' expects 2 arguments (promise error-callback), got 3.",
        )

    def test_on_reject_invalid_promise_type(self):
        """Test on-reject with non-promise first argument"""

        def handler(args, env):
            return "handled"

        with self.assertRaises(EvaluationError) as cm:
            on_reject(["not a promise", handler], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' first argument must be a promise, got str.",
        )

        with self.assertRaises(EvaluationError) as cm:
            on_reject([42, handler], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' first argument must be a promise, got int.",
        )

    def test_on_reject_invalid_handler_type(self):
        """Test on-reject with non-function handler"""
        promise = reject(["error"], self.env)

        with self.assertRaises(EvaluationError) as cm:
            on_reject([promise, "not a function"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' second argument must be a function, got str.",
        )

        with self.assertRaises(EvaluationError) as cm:
            on_reject([promise, 42], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' second argument must be a function, got int.",
        )

    def test_on_reject_handler_wrong_parameter_count(self):
        """Test on-reject with handler that has wrong parameter count"""
        promise = reject(["error"], self.env)

        # Create LisPy function with wrong parameter count
        param1 = Symbol("x")
        param2 = Symbol("y")
        wrong_param_fn = Function(
            [param1, param2], ["body"], self.env  # Takes 2 parameters, should take 1
        )

        with self.assertRaises(EvaluationError) as cm:
            on_reject([promise, wrong_param_fn], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-reject' callback must take exactly 1 argument, got 2.",
        )

    def test_on_reject_with_nil_error(self):
        """Test on-reject with nil error value"""
        promise = reject([None], self.env)

        def handle_nil_error(args, env):
            return "nil error handled"

        result = on_reject([promise, handle_nil_error], self.env)
        self.assertEqual(result.value, "nil error handled")

    def test_on_reject_return_different_types(self):
        """Test on-reject handler returning different value types"""
        promise = reject(["error"], self.env)

        # Return number
        result1 = on_reject([promise, lambda args, env: 42], self.env)
        self.assertEqual(result1.value, 42)

        # Return vector
        promise2 = reject(["error"], self.env)
        result2 = on_reject(
            [promise2, lambda args, env: Vector(["recovered"])], self.env
        )
        self.assertEqual(result2.value, Vector(["recovered"]))

        # Return dict
        promise3 = reject(["error"], self.env)
        result3 = on_reject(
            [promise3, lambda args, env: {"status": "recovered"}], self.env
        )
        self.assertEqual(result3.value, {"status": "recovered"})

    def test_on_reject_error_recovery_pattern(self):
        """Test on-reject in typical error recovery patterns"""

        def risky_operation(args, env):
            time.sleep(0.01)
            raise ConnectionError("network timeout")

        promise_obj = promise([risky_operation], self.env)

        def fallback_strategy(args, env):
            error = args[0]
            if "network" in str(error):
                return {"status": "offline", "data": "cached"}
            else:
                return {"status": "error", "message": str(error)}

        result = on_reject([promise_obj, fallback_strategy], self.env)

        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, {"status": "offline", "data": "cached"})

    def test_on_reject_with_promise_chain_recovery(self):
        """Test on-reject in a complex promise chain with recovery"""

        def step1(args, env):
            return "step1 success"

        def step2(args, env):
            raise ValueError("step2 failed")

        def recovery(args, env):
            return "recovered from step2"

        def step3(args, env):
            return f"step3: {args[0]}"

        # Chain: resolve -> then(step1) -> then(step2 fails) -> on-reject(recovery) -> then(step3)
        from lispy.functions.promises.then import promise_then

        promise = resolve(["start"], self.env)
        step1_result = promise_then([promise, step1], self.env)
        step2_result = promise_then([step1_result, step2], self.env)
        recovered_result = on_reject([step2_result, recovery], self.env)
        final_result = promise_then([recovered_result, step3], self.env)

        self.assertEqual(final_result.state, "resolved")
        self.assertEqual(final_result.value, "step3: recovered from step2")


if __name__ == "__main__":
    unittest.main()

"""Tests for with-timeout function - wraps promises with timeout and fallback"""

import time
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.functions.promises.promise import promise
from lispy.functions.promises.reject import reject
from lispy.functions.promises.resolve import resolve
from lispy.functions.promises.with_timeout import with_timeout
from lispy.types import LispyList, LispyPromise, Vector


class TestWithTimeout(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_with_timeout_fast_promise_success(self):
        """Test with-timeout when promise resolves before timeout"""
        promise_obj = resolve(["quick result"], self.env)
        result = with_timeout([promise_obj, "fallback", 100], self.env)

        # Should resolve with original promise value, not fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "quick result")

    def test_with_timeout_slow_promise_timeout(self):
        """Test with-timeout when promise times out"""

        def slow_function(args, env):
            time.sleep(0.15)  # 150ms delay
            return "slow result"

        promise_obj = promise([slow_function], self.env)
        result = with_timeout(
            [promise_obj, "timeout fallback", 50], self.env
        )  # 50ms timeout

        # Should timeout and resolve with fallback
        time.sleep(0.08)  # Wait longer than timeout but less than promise
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "timeout fallback")

    def test_with_timeout_promise_rejects_before_timeout(self):
        """Test with-timeout when promise rejects before timeout"""
        promise_obj = reject(["promise error"], self.env)
        result = with_timeout([promise_obj, "fallback", 100], self.env)

        # Should reject with original error, not use fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "promise error")

    def test_with_timeout_zero_timeout(self):
        """Test with-timeout with zero timeout (immediate timeout)"""

        def any_function(args, env):
            time.sleep(0.01)
            return "result"

        promise_obj = promise([any_function], self.env)
        result = with_timeout([promise_obj, "immediate fallback", 0], self.env)

        # Should immediately use fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "immediate fallback")

    def test_with_timeout_different_fallback_types(self):
        """Test with-timeout with different fallback value types"""

        def slow_function(args, env):
            time.sleep(0.1)
            return "original"

        promise_obj = promise([slow_function], self.env)

        # String fallback
        result1 = with_timeout([promise_obj, "string fallback", 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result1.value, "string fallback")

        # Number fallback
        promise_obj2 = promise([slow_function], self.env)
        result2 = with_timeout([promise_obj2, 42, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result2.value, 42)

        # Vector fallback
        promise_obj3 = promise([slow_function], self.env)
        fallback_vector = Vector(["fallback", "data"])
        result3 = with_timeout([promise_obj3, fallback_vector, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result3.value, fallback_vector)

        # Nil fallback
        promise_obj4 = promise([slow_function], self.env)
        result4 = with_timeout([promise_obj4, None, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result4.value, None)

    def test_with_timeout_wrong_arg_count(self):
        """Test with-timeout with wrong number of arguments"""
        promise_obj = resolve([1], self.env)

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 2.",
        )

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback", 100, "extra"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 4.",
        )

    def test_with_timeout_invalid_promise_type(self):
        """Test with-timeout with non-promise first argument"""
        with self.assertRaises(EvaluationError) as cm:
            with_timeout(["not a promise", "fallback", 100], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' first argument must be a promise, got str.",
        )

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([42, "fallback", 100], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' first argument must be a promise, got int.",
        )

    def test_with_timeout_invalid_timeout_type(self):
        """Test with-timeout with invalid timeout type"""
        promise_obj = resolve([1], self.env)

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback", "not a number"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got str.",
        )

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback", Vector([100])], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got Vector.",
        )

    def test_with_timeout_negative_timeout(self):
        """Test with-timeout with negative timeout value"""
        promise_obj = resolve([1], self.env)

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback", -100], self.env)
        self.assertEqual(
            str(cm.exception),
            "ValueError: 'with-timeout' timeout-ms must be non-negative, got -100.",
        )

        with self.assertRaises(EvaluationError) as cm:
            with_timeout([promise_obj, "fallback", -1], self.env)
        self.assertEqual(
            str(cm.exception),
            "ValueError: 'with-timeout' timeout-ms must be non-negative, got -1.",
        )

    def test_with_timeout_float_timeout(self):
        """Test with-timeout with float timeout values"""

        def slow_function(args, env):
            time.sleep(0.1)
            return "result"

        promise_obj = promise([slow_function], self.env)
        result = with_timeout([promise_obj, "fallback", 25.5], self.env)  # 25.5ms

        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fallback")

    def test_with_timeout_race_condition_edge_case(self):
        """Test with-timeout edge case where promise and timeout complete very close together"""

        def precise_timing_function(args, env):
            time.sleep(0.025)  # 25ms
            return "precise result"

        promise_obj = promise([precise_timing_function], self.env)
        result = with_timeout(
            [promise_obj, "timeout fallback", 30], self.env
        )  # 30ms timeout

        # Should resolve with promise result since it completes before timeout
        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        # Note: This might be flaky due to timing, but should usually work
        self.assertEqual(result.value, "precise result")

    def test_with_timeout_chaining_compatibility(self):
        """Test with-timeout works in promise chains"""

        def slow_step1(args, env):
            time.sleep(0.05)
            return "step1"

        def slow_step2(args, env):
            time.sleep(0.08)  # Will timeout
            return "step2"

        # First promise should succeed
        promise_obj1 = promise([slow_step1], self.env)
        result1 = with_timeout([promise_obj1, "fallback1", 100], self.env)
        time.sleep(0.08)
        self.assertEqual(result1.value, "step1")

        # Second promise should timeout (create it fresh so it hasn't already finished)
        promise_obj2 = promise([slow_step2], self.env)
        result2 = with_timeout([promise_obj2, "fallback2", 30], self.env)
        time.sleep(0.05)
        self.assertEqual(result2.value, "fallback2")

    def test_with_timeout_multiple_sequential_calls(self):
        """Test multiple with-timeout calls on different promises"""

        def make_timed_promise(delay):
            def timed_function(args, env):
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                return f"result-{delay}ms"

            return promise([timed_function], self.env)

        # Fast promise - should complete
        fast_promise = make_timed_promise(20)
        fast_result = with_timeout([fast_promise, "fast-fallback", 50], self.env)

        # Slow promise - should timeout
        slow_promise = make_timed_promise(80)
        slow_result = with_timeout([slow_promise, "slow-fallback", 50], self.env)

        time.sleep(0.1)

        self.assertEqual(fast_result.value, "result-20ms")
        self.assertEqual(slow_result.value, "slow-fallback")

    def test_with_timeout_with_complex_fallback_data(self):
        """Test with-timeout with complex fallback data structures"""

        def slow_function(args, env):
            time.sleep(0.1)
            return {"original": "data"}

        promise_obj = promise([slow_function], self.env)

        complex_fallback = {
            "status": "timeout",
            "data": Vector(["fallback", "values"]),
            "metadata": {"timestamp": "now", "reason": "timeout_occurred"},
        }

        result = with_timeout([promise_obj, complex_fallback, 30], self.env)
        time.sleep(0.05)

        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, complex_fallback)
        self.assertEqual(result.value["status"], "timeout")


if __name__ == "__main__":
    unittest.main()

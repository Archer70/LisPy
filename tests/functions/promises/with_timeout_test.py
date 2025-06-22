"""Tests for with-timeout function - wraps promises with timeout and fallback"""

import unittest
import time
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.functions.promises.with_timeout import builtin_with_timeout
from lispy.functions.promises.resolve import builtin_resolve
from lispy.functions.promises.reject import builtin_reject
from lispy.functions.promises.promise import builtin_promise


class TestWithTimeout(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_with_timeout_fast_promise_success(self):
        """Test with-timeout when promise resolves before timeout"""
        promise = builtin_resolve(["quick result"], self.env)
        result = builtin_with_timeout([promise, "fallback", 100], self.env)
        
        # Should resolve with original promise value, not fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "quick result")

    def test_with_timeout_slow_promise_timeout(self):
        """Test with-timeout when promise times out"""
        def slow_function(args, env):
            time.sleep(0.15)  # 150ms delay
            return "slow result"
            
        promise = builtin_promise([slow_function], self.env)
        result = builtin_with_timeout([promise, "timeout fallback", 50], self.env)  # 50ms timeout
        
        # Should timeout and resolve with fallback
        time.sleep(0.08)  # Wait longer than timeout but less than promise
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "timeout fallback")

    def test_with_timeout_promise_rejects_before_timeout(self):
        """Test with-timeout when promise rejects before timeout"""
        promise = builtin_reject(["promise error"], self.env)
        result = builtin_with_timeout([promise, "fallback", 100], self.env)
        
        # Should reject with original error, not use fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "promise error")

    def test_with_timeout_zero_timeout(self):
        """Test with-timeout with zero timeout (immediate timeout)"""
        def any_function(args, env):
            time.sleep(0.01)
            return "result"
            
        promise = builtin_promise([any_function], self.env)
        result = builtin_with_timeout([promise, "immediate fallback", 0], self.env)
        
        # Should immediately use fallback
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "immediate fallback")

    def test_with_timeout_different_fallback_types(self):
        """Test with-timeout with different fallback value types"""
        def slow_function(args, env):
            time.sleep(0.1)
            return "original"
            
        promise = builtin_promise([slow_function], self.env)
        
        # String fallback
        result1 = builtin_with_timeout([promise, "string fallback", 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result1.value, "string fallback")
        
        # Number fallback
        promise2 = builtin_promise([slow_function], self.env)
        result2 = builtin_with_timeout([promise2, 42, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result2.value, 42)
        
        # Vector fallback
        promise3 = builtin_promise([slow_function], self.env)
        fallback_vector = Vector(["fallback", "data"])
        result3 = builtin_with_timeout([promise3, fallback_vector, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result3.value, fallback_vector)
        
        # Nil fallback
        promise4 = builtin_promise([slow_function], self.env)
        result4 = builtin_with_timeout([promise4, None, 20], self.env)
        time.sleep(0.05)
        self.assertEqual(result4.value, None)

    def test_with_timeout_wrong_arg_count(self):
        """Test with-timeout with wrong number of arguments"""
        promise = builtin_resolve([1], self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 2."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 1."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback", 100, "extra"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 4."
        )

    def test_with_timeout_invalid_promise_type(self):
        """Test with-timeout with non-promise first argument"""
        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout(["not a promise", "fallback", 100], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' first argument must be a promise, got str."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([42, "fallback", 100], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' first argument must be a promise, got int."
        )

    def test_with_timeout_invalid_timeout_type(self):
        """Test with-timeout with invalid timeout type"""
        promise = builtin_resolve([1], self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback", "not a number"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got str."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback", Vector([100])], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got Vector."
        )

    def test_with_timeout_negative_timeout(self):
        """Test with-timeout with negative timeout value"""
        promise = builtin_resolve([1], self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback", -100], self.env)
        self.assertEqual(
            str(cm.exception),
            "ValueError: 'with-timeout' timeout-ms must be non-negative, got -100."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_with_timeout([promise, "fallback", -1], self.env)
        self.assertEqual(
            str(cm.exception),
            "ValueError: 'with-timeout' timeout-ms must be non-negative, got -1."
        )

    def test_with_timeout_float_timeout(self):
        """Test with-timeout with float timeout values"""
        def slow_function(args, env):
            time.sleep(0.1)
            return "result"
            
        promise = builtin_promise([slow_function], self.env)
        result = builtin_with_timeout([promise, "fallback", 25.5], self.env)  # 25.5ms
        
        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fallback")

    def test_with_timeout_race_condition_edge_case(self):
        """Test with-timeout edge case where promise and timeout complete very close together"""
        def precise_timing_function(args, env):
            time.sleep(0.025)  # 25ms
            return "precise result"
            
        promise = builtin_promise([precise_timing_function], self.env)
        result = builtin_with_timeout([promise, "timeout fallback", 30], self.env)  # 30ms timeout
        
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
        promise1 = builtin_promise([slow_step1], self.env)
        result1 = builtin_with_timeout([promise1, "fallback1", 100], self.env)
        time.sleep(0.08)
        self.assertEqual(result1.value, "step1")
        
        # Second promise should timeout (create it fresh so it hasn't already finished)
        promise2 = builtin_promise([slow_step2], self.env)
        result2 = builtin_with_timeout([promise2, "fallback2", 30], self.env)
        time.sleep(0.05)
        self.assertEqual(result2.value, "fallback2")

    def test_with_timeout_multiple_sequential_calls(self):
        """Test multiple with-timeout calls on different promises"""
        def make_timed_promise(delay):
            def timed_function(args, env):
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                return f"result-{delay}ms"
            return builtin_promise([timed_function], self.env)
        
        # Fast promise - should complete
        fast_promise = make_timed_promise(20)
        fast_result = builtin_with_timeout([fast_promise, "fast-fallback", 50], self.env)
        
        # Slow promise - should timeout  
        slow_promise = make_timed_promise(80)
        slow_result = builtin_with_timeout([slow_promise, "slow-fallback", 50], self.env)
        
        time.sleep(0.1)
        
        self.assertEqual(fast_result.value, "result-20ms")
        self.assertEqual(slow_result.value, "slow-fallback")

    def test_with_timeout_with_complex_fallback_data(self):
        """Test with-timeout with complex fallback data structures"""
        def slow_function(args, env):
            time.sleep(0.1)
            return {"original": "data"}
            
        promise = builtin_promise([slow_function], self.env)
        
        complex_fallback = {
            "status": "timeout",
            "data": Vector(["fallback", "values"]),
            "metadata": {
                "timestamp": "now",
                "reason": "timeout_occurred"
            }
        }
        
        result = builtin_with_timeout([promise, complex_fallback, 30], self.env)
        time.sleep(0.05)
        
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, complex_fallback)
        self.assertEqual(result.value["status"], "timeout")


if __name__ == "__main__":
    unittest.main() 
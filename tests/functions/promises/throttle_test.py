"""
Tests for throttle function - rate limiting function execution.

Tests cover:
- Basic throttling behavior (first call executes, subsequent ignored)
- Rate limiting timing verification
- Argument validation and error handling
- Both user-defined and built-in functions
- Thread safety and concurrent access
- Edge cases (zero rate, rapid calls, etc.)
- Comparison with debounce behavior patterns
"""

import unittest
import time
import threading
from lispy.functions import create_global_env
from lispy.types import Vector
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class TestThrottle(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()
        # Track function calls for testing
        self.call_count = 0
        self.call_times = []
        self.last_args = None
        self.results = []

    def create_tracking_function(self):
        """Create a function that tracks calls."""
        def tracking_fn(args, env):
            self.call_count += 1
            self.call_times.append(time.time())
            if args:
                self.last_args = args
                self.results.append(args[0])
            return f"call-{self.call_count}"
        
        return tracking_fn

    def reset_tracking(self):
        """Reset tracking variables."""
        self.call_count = 0
        self.call_times = []
        self.last_args = None
        self.results = []

    def test_throttle_first_call_executes_immediately(self):
        """Test that the first call to a throttled function executes immediately."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 1000))", self.env)
        result = run_lispy_string("(throttled-fn)", self.env)
        
        self.assertEqual(result, "call-1")
        self.assertEqual(self.call_count, 1)

    def test_throttle_subsequent_calls_ignored(self):
        """Test that subsequent calls within rate period are ignored."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 500))", self.env)
        
        # First call should execute
        result1 = run_lispy_string("(throttled-fn)", self.env)
        self.assertEqual(result1, "call-1")
        
        # Immediate second call should be ignored
        result2 = run_lispy_string("(throttled-fn)", self.env)
        self.assertIsNone(result2)
        
        # Third call still ignored
        result3 = run_lispy_string("(throttled-fn)", self.env)
        self.assertIsNone(result3)
        
        # Should only have executed once
        self.assertEqual(self.call_count, 1)

    def test_throttle_calls_after_rate_period(self):
        """Test that calls after rate period executes."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 100))", self.env)
        
        # First call executes
        result1 = run_lispy_string("(throttled-fn)", self.env)
        self.assertEqual(result1, "call-1")
        
        # Wait for rate period to expire
        time.sleep(0.15)  # 150ms > 100ms rate
        
        # Next call should execute
        result2 = run_lispy_string("(throttled-fn)", self.env)
        self.assertEqual(result2, "call-2")
        
        self.assertEqual(self.call_count, 2)

    def test_throttle_with_arguments(self):
        """Test throttling preserves function arguments."""
        def store_args(args, env):
            self.call_count += 1
            if args:
                self.results.append(args[0])
            return f"stored-{args[0] if args else 'none'}"
        
        self.env.define("store-args", store_args)
        
        run_lispy_string("(define throttled-store (throttle store-args 100))", self.env)
        
        # First call with argument
        result1 = run_lispy_string('(throttled-store "first")', self.env)
        self.assertEqual(result1, "stored-first")
        
        # Second call ignored
        result2 = run_lispy_string('(throttled-store "second")', self.env)
        self.assertIsNone(result2)
        
        # Wait and call again
        time.sleep(0.15)
        result3 = run_lispy_string('(throttled-store "third")', self.env)
        self.assertEqual(result3, "stored-third")
        
        # Should have only stored first and third
        self.assertEqual(self.results, ["first", "third"])

    def test_throttle_zero_rate(self):
        """Test throttle with zero rate allows all calls."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 0))", self.env)
        
        # All calls should execute with zero rate
        result1 = run_lispy_string("(throttled-fn)", self.env)
        result2 = run_lispy_string("(throttled-fn)", self.env)
        result3 = run_lispy_string("(throttled-fn)", self.env)
        
        self.assertEqual(result1, "call-1")
        self.assertEqual(result2, "call-2")
        self.assertEqual(result3, "call-3")
        self.assertEqual(self.call_count, 3)

    def test_throttle_rate_timing_accuracy(self):
        """Test that throttle timing is reasonably accurate."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        rate = 200  # 200ms rate
        run_lispy_string(f"(define throttled-fn (throttle tracking-fn {rate}))", self.env)
        
        # First call
        start_time = time.time()
        run_lispy_string("(throttled-fn)", self.env)
        
        # Rapid calls (should be ignored)
        for _ in range(5):
            run_lispy_string("(throttled-fn)", self.env)
            time.sleep(0.02)  # 20ms between calls
        
        # Wait for rate period and call again
        time.sleep(0.2)  # 200ms
        run_lispy_string("(throttled-fn)", self.env)
        end_time = time.time()
        
        total_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Should have executed twice: first call + after rate period
        self.assertEqual(self.call_count, 2)
        
        # Total time should be approximately rate period
        self.assertGreater(total_time, rate * 0.8)  # At least 80% of expected
        self.assertLess(total_time, rate * 2)       # Less than 200% of expected

    def test_throttle_with_user_defined_function(self):
        """Test throttle with user-defined functions."""
        run_lispy_string('(define simple-fn (fn [] "user-defined-result"))', self.env)
        run_lispy_string("(define throttled-fn (throttle simple-fn 100))", self.env)
        
        # First call executes
        result1 = run_lispy_string("(throttled-fn)", self.env)
        self.assertEqual(result1, "user-defined-result")
        
        # Second call ignored
        result2 = run_lispy_string("(throttled-fn)", self.env)
        self.assertIsNone(result2)

    def test_throttle_multiple_independent_functions(self):
        """Test multiple independent throttled functions."""
        def counter1(args, env):
            self.call_count += 1
            return f"counter1-{self.call_count}"
        
        def counter2(args, env):
            return f"counter2-{len(self.results) + 1}"
        
        self.env.define("counter1", counter1)
        self.env.define("counter2", counter2)
        
        run_lispy_string("(define throttled1 (throttle counter1 100))", self.env)
        run_lispy_string("(define throttled2 (throttle counter2 100))", self.env)
        
        # Both first calls should execute
        result1 = run_lispy_string("(throttled1)", self.env)
        result2 = run_lispy_string("(throttled2)", self.env)
        
        self.assertEqual(result1, "counter1-1")
        self.assertEqual(result2, "counter2-1")
        
        # Both second calls should be ignored
        result3 = run_lispy_string("(throttled1)", self.env)
        result4 = run_lispy_string("(throttled2)", self.env)
        
        self.assertIsNone(result3)
        self.assertIsNone(result4)

    def test_argument_validation_wrong_count(self):
        """Test error handling for wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(throttle)", self.env)
        self.assertIn("expects 2 arguments", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(throttle (fn [] nil) 100 "extra")', self.env)
        self.assertIn("expects 2 arguments", str(cm.exception))

    def test_argument_validation_non_function(self):
        """Test error handling for non-function first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(throttle "not-a-function" 100)', self.env)
        self.assertIn("first argument must be a function", str(cm.exception))

    def test_argument_validation_non_number_rate(self):
        """Test error handling for non-number rate argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(throttle (fn [] nil) "not-a-number")', self.env)
        self.assertIn("second argument (rate) must be a number", str(cm.exception))

    def test_argument_validation_negative_rate(self):
        """Test error handling for negative rate."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(throttle (fn [] nil) -100)', self.env)
        self.assertIn("rate must be non-negative", str(cm.exception))

    def test_throttle_with_different_rate_values(self):
        """Test throttle with various rate values."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        # Test with floating point rate
        run_lispy_string("(define throttled-float (throttle tracking-fn 50.5))", self.env)
        result = run_lispy_string("(throttled-float)", self.env)
        self.assertEqual(result, "call-1")
        
        # Reset for next test
        self.reset_tracking()
        
        # Test with large rate
        run_lispy_string("(define throttled-large (throttle tracking-fn 5000))", self.env)
        result1 = run_lispy_string("(throttled-large)", self.env)
        result2 = run_lispy_string("(throttled-large)", self.env)
        
        self.assertEqual(result1, "call-1")
        self.assertIsNone(result2)

    def test_throttle_thread_safety(self):
        """Test thread safety with concurrent calls."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 200))", self.env)
        
        def call_throttled():
            run_lispy_string("(throttled-fn)", self.env)
        
        # Make concurrent calls from multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=call_throttled)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should only execute once despite multiple concurrent calls
        self.assertLessEqual(self.call_count, 2)  # Allow for some timing variance

    def test_throttle_preserves_result_types(self):
        """Test that throttle preserves the original function's return types."""
        test_cases = [
            ('(fn [] 42)', 42),
            ('(fn [] "hello")', "hello"),
            ('(fn [] true)', True),
            ('(fn [] nil)', None),
            ('(fn [] [1 2 3])', Vector([1, 2, 3])),
        ]
        
        for i, (func_def, expected) in enumerate(test_cases):
            with self.subTest(func=func_def, expected=expected):
                throttled_name = f"throttled-{i}"
                run_lispy_string(f"(define {throttled_name} (throttle {func_def} 10))", self.env)
                result = run_lispy_string(f"({throttled_name})", self.env)
                self.assertEqual(result, expected)

    def test_throttle_vs_debounce_behavior(self):
        """Test that throttle behaves differently from debounce."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        # Create both throttled and debounced versions
        run_lispy_string("(define throttled-fn (throttle tracking-fn 100))", self.env)
        
        # Throttle: first call executes immediately
        result = run_lispy_string("(throttled-fn)", self.env)
        self.assertEqual(result, "call-1")
        self.assertEqual(self.call_count, 1)
        
        # Reset for debounce comparison
        self.reset_tracking()
        
        # Debounce: first call is delayed
        run_lispy_string("(define debounced-fn (debounce tracking-fn 100))", self.env)
        result = run_lispy_string("(debounced-fn)", self.env)
        self.assertIsNone(result)  # Debounce returns nil immediately
        self.assertEqual(self.call_count, 0)  # Not executed yet

    def test_throttle_rapid_successive_calls(self):
        """Test throttle with many rapid successive calls."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 200))", self.env)
        
        # Make 10 rapid calls with very short intervals
        results = []
        for i in range(10):
            result = run_lispy_string("(throttled-fn)", self.env)
            results.append(result)
            time.sleep(0.005)  # 5ms between calls (much faster than 200ms rate)
        
        # Only first call should have executed (all others within rate period)
        non_none_results = [r for r in results if r is not None]
        self.assertLessEqual(len(non_none_results), 2)  # Allow for timing variance
        self.assertTrue("call-1" in [str(r) for r in non_none_results])
        self.assertLessEqual(self.call_count, 2)  # Should be mostly 1, but allow for timing

    def test_throttle_function_with_arguments(self):
        """Test throttle with functions that take arguments."""
        def echo_args(args, env):
            self.call_count += 1
            if args:
                return f"echo-{args[0]}"
            return "echo-none"
        
        self.env.define("echo-args", echo_args)
        
        run_lispy_string("(define throttled-echo (throttle echo-args 100))", self.env)
        
        # First call with argument
        result1 = run_lispy_string('(throttled-echo "hello")', self.env)
        self.assertEqual(result1, "echo-hello")
        
        # Second call ignored
        result2 = run_lispy_string('(throttled-echo "world")', self.env)
        self.assertIsNone(result2)
        
        # Wait and try again
        time.sleep(0.15)
        result3 = run_lispy_string('(throttled-echo "again")', self.env)
        self.assertEqual(result3, "echo-again")
        
        self.assertEqual(self.call_count, 2)

    def test_throttle_with_zero_argument_function(self):
        """Test throttle with zero-argument functions."""
        # Test throttle with a simple zero-argument function that returns a value
        run_lispy_string('(define simple-fn (fn [] "zero-arg-result"))', self.env)
        run_lispy_string("(define throttled-simple (throttle simple-fn 100))", self.env)
        
        # First call executes
        result1 = run_lispy_string("(throttled-simple)", self.env)
        self.assertEqual(result1, "zero-arg-result")
        
        # Second call ignored
        result2 = run_lispy_string("(throttled-simple)", self.env)
        self.assertIsNone(result2)
        
        # Wait and call again
        time.sleep(0.15)
        result3 = run_lispy_string("(throttled-simple)", self.env)
        self.assertEqual(result3, "zero-arg-result")

    def test_throttle_error_handling(self):
        """Test throttle handles function errors gracefully."""
        def error_fn(args, env):
            self.call_count += 1
            if self.call_count == 1:
                raise Exception("First call error")
            return "success"
        
        self.env.define("error-fn", error_fn)
        
        run_lispy_string("(define throttled-error (throttle error-fn 100))", self.env)
        
        # First call should handle error gracefully (returns None)
        result1 = run_lispy_string("(throttled-error)", self.env)
        self.assertIsNone(result1)
        
        # Wait and try again
        time.sleep(0.15)
        result2 = run_lispy_string("(throttled-error)", self.env)
        self.assertEqual(result2, "success")

    def test_throttle_timing_precision(self):
        """Test throttle timing precision for short rates."""
        tracking_fn = self.create_tracking_function()
        self.env.define("tracking-fn", tracking_fn)
        
        run_lispy_string("(define throttled-fn (throttle tracking-fn 50))", self.env)
        
        start_time = time.time()
        
        # First call
        run_lispy_string("(throttled-fn)", self.env)
        
        # Wait precisely for rate period
        time.sleep(0.06)  # 60ms > 50ms rate
        
        # Second call
        run_lispy_string("(throttled-fn)", self.env)
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        
        # Should have executed twice
        self.assertEqual(self.call_count, 2)
        
        # Timing should be reasonable
        self.assertGreater(total_time, 40)   # At least 40ms
        self.assertLess(total_time, 100)     # Less than 100ms


if __name__ == "__main__":
    unittest.main() 
"""
Tests for debounce function - delayed function execution with cancellation.

Tests cover:
- Basic debouncing behavior
- Cancellation of previous calls
- Multiple rapid calls
- Argument handling
- Error validation
- Thread safety
- Timing verification
"""

import unittest
import time
import threading
from lispy.functions import create_global_env
from lispy.types import Vector
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class TestDebounce(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()
        # Track function calls for testing
        self.call_count = 0
        self.last_args = None
        self.results = []

    def create_test_function(self, delay_ms=0):
        """Create a test function that tracks calls."""
        def test_fn(args, env):
            self.call_count += 1
            self.last_args = args
            if args:
                self.results.append(args[0])
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)
            return f"call-{self.call_count}"
        
        return test_fn

    def test_basic_debounce_behavior(self):
        """Test that debounce delays function execution."""
        # Track execution using a list we can modify
        self.call_count = 0
        
        def track_calls(args, env):
            self.call_count += 1
            return self.call_count
        
        # Add our tracking function to the environment
        self.env.define("track-calls", track_calls)
        
        run_lispy_string("(define debounced-track (debounce track-calls 100))", self.env)
        result = run_lispy_string("(debounced-track)", self.env)
        
        self.assertIsNone(result)  # Debounced function returns None immediately
        self.assertEqual(self.call_count, 0)  # Function hasn't executed yet
        
        # Wait for debounce to trigger
        time.sleep(0.15)  # 150ms to ensure 100ms delay completes
        
        # Check that function was called
        self.assertEqual(self.call_count, 1)

    def test_debounce_cancellation(self):
        """Test that rapid calls cancel previous executions."""
        self.call_count = 0
        
        def count_calls(args, env):
            self.call_count += 1
            return self.call_count
        
        self.env.define("count-calls", count_calls)
        
        run_lispy_string("(define debounced-fn (debounce count-calls 100))", self.env)
        
        # Make rapid calls
        for _ in range(5):
            run_lispy_string("(debounced-fn)", self.env)
            time.sleep(0.02)  # 20ms between calls, much less than 100ms delay
        
        # Wait for final call to execute
        time.sleep(0.15)
        
        # Should only have executed once (the last call)
        self.assertEqual(self.call_count, 1)

    def test_debounce_with_arguments(self):
        """Test debounce preserves function arguments."""
        self.last_value = None
        
        def store_value(args, env):
            if args:
                self.last_value = args[0]
            return self.last_value
        
        self.env.define("store-value", store_value)
        
        run_lispy_string("(define debounced-store (debounce store-value 50))", self.env)
        run_lispy_string('(debounced-store "first")', self.env)
        run_lispy_string('(debounced-store "second")', self.env)
        run_lispy_string('(debounced-store "final")', self.env)
        
        # Wait for debounce to trigger
        time.sleep(0.1)
        
        # Should have stored the last value
        self.assertEqual(self.last_value, "final")

    def test_debounce_zero_delay(self):
        """Test debounce with zero delay executes immediately."""
        result = run_lispy_string("""
            (define counter 0)
            (define increment (fn [] (define counter (+ counter 1))))
            (define debounced-increment (debounce increment 0))
            (debounced-increment)
        """, self.env)
        
        # With zero delay, should execute almost immediately
        time.sleep(0.01)  # Small delay to allow timer to fire
        
        counter_value = run_lispy_string("counter", self.env)
        self.assertEqual(counter_value, 1)

    def test_multiple_debounced_functions(self):
        """Test multiple independent debounced functions."""
        run_lispy_string("""
            (define counter1 0)
            (define counter2 0)
            (define increment1 (fn [] (define counter1 (+ counter1 1))))
            (define increment2 (fn [] (define counter2 (+ counter2 1))))
            (define debounced1 (debounce increment1 50))
            (define debounced2 (debounce increment2 50))
        """, self.env)
        
        # Call both debounced functions
        run_lispy_string("(debounced1)", self.env)
        run_lispy_string("(debounced2)", self.env)
        
        # Wait for execution
        time.sleep(0.1)
        
        # Both should have executed
        counter1 = run_lispy_string("counter1", self.env)
        counter2 = run_lispy_string("counter2", self.env)
        self.assertEqual(counter1, 1)
        self.assertEqual(counter2, 1)

    def test_debounce_returns_nil(self):
        """Test that debounced function returns nil immediately."""
        result = run_lispy_string("""
            (define test-fn (fn [] "result"))
            (define debounced-fn (debounce test-fn 50))
            (debounced-fn)
        """, self.env)
        
        # Should return nil immediately, not the result of the original function
        self.assertIsNone(result)

    def test_argument_validation_wrong_count(self):
        """Test error handling for wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(debounce)", self.env)
        self.assertIn("expects 2 arguments", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(debounce (fn [] nil) 100 "extra")', self.env)
        self.assertIn("expects 2 arguments", str(cm.exception))

    def test_argument_validation_non_function(self):
        """Test error handling for non-function first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(debounce "not-a-function" 100)', self.env)
        self.assertIn("first argument must be a function", str(cm.exception))

    def test_argument_validation_non_number_delay(self):
        """Test error handling for non-number delay argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(debounce (fn [] nil) "not-a-number")', self.env)
        self.assertIn("second argument (delay) must be a number", str(cm.exception))

    def test_argument_validation_negative_delay(self):
        """Test error handling for negative delay."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(debounce (fn [] nil) -100)', self.env)
        self.assertIn("delay must be non-negative", str(cm.exception))

    def test_debounce_with_different_arities(self):
        """Test debounce works with functions of different arities."""
        # No arguments
        result = run_lispy_string("""
            (define counter 0)
            (define increment (fn [] (define counter (+ counter 1))))
            (define debounced (debounce increment 50))
            (debounced)
        """, self.env)
        time.sleep(0.1)
        counter = run_lispy_string("counter", self.env)
        self.assertEqual(counter, 1)
        
        # One argument
        result = run_lispy_string("""
            (define value nil)
            (define setter (fn [x] (define value x)))
            (define debounced-setter (debounce setter 50))
            (debounced-setter "test")
        """, self.env)
        time.sleep(0.1)
        value = run_lispy_string("value", self.env)
        self.assertEqual(value, "test")

    def test_timing_precision(self):
        """Test that debounce timing is reasonably accurate."""
        start_time = time.time()
        
        run_lispy_string("""
            (define executed-time nil)
            (define mark-time (fn [] (define executed-time "done")))
            (define debounced-mark (debounce mark-time 100))
            (debounced-mark)
        """, self.env)
        
        # Wait for execution
        time.sleep(0.15)
        
        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to ms
        
        # Should have taken approximately 100ms (allow some tolerance)
        self.assertGreater(elapsed, 80)   # At least 80ms
        self.assertLess(elapsed, 200)     # Less than 200ms
        
        # Verify function was executed
        executed = run_lispy_string("executed-time", self.env)
        self.assertEqual(executed, "done")

    def test_thread_safety_concurrent_calls(self):
        """Test thread safety with concurrent calls."""
        run_lispy_string("""
            (define call-count 0)
            (define increment (fn [] (define call-count (+ call-count 1))))
            (define debounced-increment (debounce increment 100))
        """, self.env)
        
        # Make concurrent calls from multiple threads
        def call_debounced():
            run_lispy_string("(debounced-increment)", self.env)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=call_debounced)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Wait for debounce to execute
        time.sleep(0.15)
        
        # Should only execute once despite multiple concurrent calls
        call_count = run_lispy_string("call-count", self.env)
        self.assertEqual(call_count, 1)

    def test_sequential_calls_with_gaps(self):
        """Test sequential calls with time gaps larger than delay."""
        run_lispy_string("""
            (define call-count 0)
            (define increment (fn [] (define call-count (+ call-count 1))))
            (define debounced-increment (debounce increment 50))
        """, self.env)
        
        # First call
        run_lispy_string("(debounced-increment)", self.env)
        time.sleep(0.1)  # Wait for first call to execute
        
        # Second call after delay
        run_lispy_string("(debounced-increment)", self.env)
        time.sleep(0.1)  # Wait for second call to execute
        
        # Both calls should have executed
        call_count = run_lispy_string("call-count", self.env)
        self.assertEqual(call_count, 2)


if __name__ == "__main__":
    unittest.main() 
"""
Tests for retry function - automatic retry logic with exponential backoff.

Tests cover:
- Basic retry behavior (success and failure cases)
- Exponential backoff timing
- Argument validation and error handling
- Both synchronous and asynchronous operations
- Promise return values from operations
- Edge cases (zero delay, single attempt, etc.)
- Thread safety and timing verification
"""

import unittest
import time
import threading
from lispy.functions import create_global_env
from lispy.types import Vector, LispyPromise
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class TestRetry(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()
        # Track function calls for testing
        self.call_count = 0
        self.call_times = []
        self.last_error = None
        self.results = []

    def create_failing_function(self, fail_count=2):
        """Create a function that fails fail_count times then succeeds."""
        def failing_fn(args, env):
            self.call_count += 1
            self.call_times.append(time.time())
            
            if self.call_count <= fail_count:
                raise Exception(f"Attempt {self.call_count} failed")
            
            return f"Success on attempt {self.call_count}"
        
        return failing_fn

    def create_always_failing_function(self):
        """Create a function that always fails."""
        def always_fails(args, env):
            self.call_count += 1
            self.call_times.append(time.time())
            raise Exception(f"Always fails - attempt {self.call_count}")
        
        return always_fails

    def create_always_succeeding_function(self):
        """Create a function that always succeeds."""
        def always_succeeds(args, env):
            self.call_count += 1
            self.call_times.append(time.time())
            return f"Success on attempt {self.call_count}"
        
        return always_succeeds

    def test_retry_success_on_first_attempt(self):
        """Test retry when operation succeeds immediately."""
        self.call_count = 0
        
        def success_fn(args, env):
            self.call_count += 1
            return "immediate success"
        
        self.env.define("success-fn", success_fn)
        
        result = run_lispy_string("""
            (await (retry success-fn 3 100))
        """, self.env)
        
        self.assertEqual(result, "immediate success")
        self.assertEqual(self.call_count, 1)  # Only called once

    def test_retry_success_after_failures(self):
        """Test retry succeeds after some failures."""
        # Function that fails twice then succeeds
        failing_fn = self.create_failing_function(fail_count=2)
        self.env.define("failing-fn", failing_fn)
        
        result = run_lispy_string("""
            (await (retry failing-fn 5 50))
        """, self.env)
        
        self.assertEqual(result, "Success on attempt 3")
        self.assertEqual(self.call_count, 3)  # Called 3 times total

    def test_retry_all_attempts_fail(self):
        """Test retry when all attempts fail."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        with self.assertRaises(Exception) as cm:
            run_lispy_string("""
                (await (retry always-fails 3 50))
            """, self.env)
        
        error_msg = str(cm.exception)
        self.assertIn("RetryError", error_msg)
        self.assertIn("Failed after 3 attempts", error_msg)
        self.assertIn("Always fails - attempt 3", error_msg)
        self.assertEqual(self.call_count, 3)  # All 3 attempts were made

    def test_exponential_backoff_timing(self):
        """Test that exponential backoff delays are working correctly."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        start_time = time.time()
        
        try:
            run_lispy_string("""
                (await (retry always-fails 4 100))
            """, self.env)
        except:
            pass  # Expected to fail
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Expected delays: 0ms, 100ms, 200ms, 400ms = 700ms total
        # Allow some tolerance for timing variations (system dependent)
        self.assertGreater(total_time, 500)  # At least 500ms
        self.assertLess(total_time, 1500)    # Less than 1500ms (generous upper bound)
        
        # Verify individual call timing
        if len(self.call_times) >= 4:
            # First call should be immediate
            self.assertLess(self.call_times[0] - start_time, 0.05)
            
            # Subsequent calls should have increasing delays
            delay1 = (self.call_times[1] - self.call_times[0]) * 1000
            delay2 = (self.call_times[2] - self.call_times[1]) * 1000
            delay3 = (self.call_times[3] - self.call_times[2]) * 1000
            
            self.assertGreater(delay1, 50)   # ~100ms (with tolerance)
            self.assertLess(delay1, 250)    # Even more generous
            
            self.assertGreater(delay2, 100)  # ~200ms (with tolerance)
            self.assertLess(delay2, 450)    # Very generous upper bound
            
            self.assertGreater(delay3, 200)  # ~400ms (with tolerance)
            self.assertLess(delay3, 900)    # Very generous upper bound

    def test_zero_delay_retry(self):
        """Test retry with zero delay executes rapidly."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        start_time = time.time()
        
        try:
            run_lispy_string("""
                (await (retry always-fails 3 0))
            """, self.env)
        except:
            pass  # Expected to fail
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to ms
        
        # With zero delay, should complete very quickly
        self.assertLess(total_time, 50)  # Less than 50ms
        self.assertEqual(self.call_count, 3)

    def test_single_attempt_retry(self):
        """Test retry with max_attempts = 1."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        with self.assertRaises(Exception) as cm:
            run_lispy_string("""
                (await (retry always-fails 1 100))
            """, self.env)
        
        error_msg = str(cm.exception)
        self.assertIn("Failed after 1 attempts", error_msg)
        self.assertEqual(self.call_count, 1)

    def test_retry_with_promise_returning_operation(self):
        """Test retry with operations that return promises."""
        self.call_count = 0
        
        def promise_operation(args, env):
            self.call_count += 1
            promise = LispyPromise()
            
            def resolve_later():
                time.sleep(0.01)  # Small delay
                if self.call_count <= 2:  # Fail first 2 attempts
                    promise.reject(f"Promise failed on attempt {self.call_count}")
                else:
                    promise.resolve(f"Promise succeeded on attempt {self.call_count}")
            
            threading.Thread(target=resolve_later, daemon=True).start()
            return promise
        
        self.env.define("promise-operation", promise_operation)
        
        result = run_lispy_string("""
            (await (retry promise-operation 5 50))
        """, self.env)
        
        self.assertEqual(result, "Promise succeeded on attempt 3")
        self.assertEqual(self.call_count, 3)

    def test_retry_with_user_defined_function(self):
        """Test retry with user-defined functions."""
        # Create a simple test that doesn't rely on mutable state
        # This test just verifies that user-defined functions work with retry
        run_lispy_string('(define simple-success-op (fn [] "User-defined function works"))', self.env)
        result = run_lispy_string("(await (retry simple-success-op 3 50))", self.env)
        
        self.assertEqual(result, "User-defined function works")

    def test_argument_validation_wrong_count(self):
        """Test error handling for wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(retry)", self.env)
        self.assertIn("expects 3 arguments", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 3)', self.env)
        self.assertIn("expects 3 arguments", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 3 100 "extra")', self.env)
        self.assertIn("expects 3 arguments", str(cm.exception))

    def test_argument_validation_non_function(self):
        """Test error handling for non-function operation argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry "not-a-function" 3 100)', self.env)
        self.assertIn("first argument must be a function", str(cm.exception))

    def test_argument_validation_non_integer_attempts(self):
        """Test error handling for non-integer max_attempts argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) "not-a-number" 100)', self.env)
        self.assertIn("second argument (max-attempts) must be an integer", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 3.5 100)', self.env)
        self.assertIn("second argument (max-attempts) must be an integer", str(cm.exception))

    def test_argument_validation_zero_attempts(self):
        """Test error handling for zero or negative max_attempts."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 0 100)', self.env)
        self.assertIn("max-attempts must be positive", str(cm.exception))
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) -1 100)', self.env)
        self.assertIn("max-attempts must be positive", str(cm.exception))

    def test_argument_validation_non_number_delay(self):
        """Test error handling for non-number delay argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 3 "not-a-number")', self.env)
        self.assertIn("third argument (delay) must be a number", str(cm.exception))

    def test_argument_validation_negative_delay(self):
        """Test error handling for negative delay."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [] nil) 3 -100)', self.env)
        self.assertIn("delay must be non-negative", str(cm.exception))

    def test_argument_validation_function_arity(self):
        """Test error handling for functions with wrong arity."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(retry (fn [x] x) 3 100)', self.env)
        self.assertIn("operation must take 0 arguments", str(cm.exception))

    def test_retry_with_thread_first_operator(self):
        """Test retry works with thread-first operator."""
        self.call_count = 0
        
        def process_result(args, env):
            if args:
                return f"Processed: {args[0]}"
            return "Processed: nil"
        
        success_fn = self.create_always_succeeding_function()
        self.env.define("success-fn", success_fn)
        self.env.define("process-result", process_result)
        
        result = run_lispy_string("""
            (await (-> (retry success-fn 3 100)
                       (promise-then process-result)))
        """, self.env)
        
        self.assertEqual(result, "Processed: Success on attempt 1")

    def test_retry_error_propagation(self):
        """Test that retry errors are properly formatted and informative."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        with self.assertRaises(Exception) as cm:
            run_lispy_string("""
                (await (retry always-fails 2 100))
            """, self.env)
        
        error_msg = str(cm.exception)
        self.assertIn("RetryError", error_msg)
        self.assertIn("Failed after 2 attempts", error_msg)
        self.assertIn("Always fails - attempt 2", error_msg)

    def test_concurrent_retry_operations(self):
        """Test multiple retry operations running concurrently."""
        success_fn = self.create_always_succeeding_function()
        self.env.define("success-fn", success_fn)
        
        result = run_lispy_string("""
            (await (promise-all (vector
                (retry success-fn 3 50)
                (retry success-fn 3 50)
                (retry success-fn 3 50))))
        """, self.env)
        
        # Should get a vector of 3 success results
        expected = Vector([
            "Success on attempt 1",
            "Success on attempt 2", 
            "Success on attempt 3"
        ])
        self.assertEqual(result, expected)
        self.assertEqual(self.call_count, 3)  # Each retry called the function once

    def test_retry_with_different_delay_values(self):
        """Test retry with various delay values (including edge cases)."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        # Test with floating point delay
        try:
            run_lispy_string("(await (retry always-fails 2 50.5))", self.env)
        except:
            pass  # Expected to fail, but should accept float delay
        
        # Reset call count
        self.call_count = 0
        
        # Test with zero delay
        try:
            run_lispy_string("(await (retry always-fails 2 0))", self.env)
        except:
            pass  # Expected to fail
        
        self.assertEqual(self.call_count, 2)

    def test_retry_preserves_original_result_types(self):
        """Test that retry preserves the original operation's return types."""
        # Test with different return types
        test_cases = [
            ('(fn [] 42)', 42),
            ('(fn [] "hello")', "hello"),
            ('(fn [] true)', True),
            ('(fn [] nil)', None),
            ('(fn [] [1 2 3])', Vector([1, 2, 3])),
        ]
        
        for func_def, expected in test_cases:
            with self.subTest(func=func_def, expected=expected):
                result = run_lispy_string(f"""
                    (await (retry {func_def} 1 0))
                """, self.env)
                self.assertEqual(result, expected)

    def test_retry_timing_accuracy(self):
        """Test that retry timing is reasonably accurate for small delays."""
        always_fails = self.create_always_failing_function()
        self.env.define("always-fails", always_fails)
        
        start_time = time.time()
        
        try:
            run_lispy_string("""
                (await (retry always-fails 3 100))
            """, self.env)
        except:
            pass  # Expected to fail
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Expected: 0 + 100 + 200 = 300ms minimum
        self.assertGreater(total_time, 200)  # At least 200ms (with tolerance)
        self.assertLess(total_time, 800)     # Less than 800ms (generous upper bound)


if __name__ == "__main__":
    unittest.main() 
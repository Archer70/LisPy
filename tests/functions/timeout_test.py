import unittest
import time
from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.parser import parse
from lispy.lexer import tokenize
from lispy.types import LispyPromise
from lispy.exceptions import EvaluationError
from lispy.functions import global_env


def run_lispy_string(code_string, env=None):
    """Helper function to run LisPy code from a string."""
    if env is None:
        env = Environment(outer=global_env)
    
    tokens = tokenize(code_string)
    parsed_expr = parse(tokens)
    return evaluate(parsed_expr, env)


class TestTimeoutFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        self.env = Environment(outer=global_env)
    
    def test_timeout_basic_functionality(self):
        """Test basic timeout functionality."""
        result = run_lispy_string('(timeout 100)', self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "pending")
        
        # Wait for timeout to complete
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertIsNone(result.value)
    
    def test_timeout_with_value(self):
        """Test timeout with a specific value."""
        result = run_lispy_string('(timeout 100 "done")', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "done")
    
    def test_timeout_zero_delay(self):
        """Test timeout with zero delay."""
        result = run_lispy_string('(timeout 0 "immediate")', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        # Should resolve very quickly
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "immediate")
    
    def test_timeout_argument_validation(self):
        """Test timeout function argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(timeout)', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'timeout' expects 1 or 2 arguments (ms [value]), got 0.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(timeout 1000 "value" "extra")', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'timeout' expects 1 or 2 arguments (ms [value]), got 3.")
        
        # Invalid timeout type
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(timeout "not-a-number")', self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'timeout' first argument (ms) must be a number, got str.")
        
        # Negative timeout
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(timeout -100)', self.env)
        self.assertEqual(str(cm.exception), "ValueError: 'timeout' ms must be non-negative, got -100.")
    
    def test_timeout_thread_first_compatibility(self):
        """Test timeout works with thread-first operator."""
        result = run_lispy_string('(-> (timeout 100 "chained") (promise-then (fn [x] (append x "!!"))))', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "chained!!")
    
    def test_with_timeout_basic_functionality(self):
        """Test basic with-timeout functionality."""
        # Create a promise that resolves quickly
        result = run_lispy_string('(with-timeout (resolve "fast") "fallback" 1000)', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fast")
    
    def test_with_timeout_triggers_fallback(self):
        """Test with-timeout uses fallback when timeout occurs."""
        # Create a promise that takes longer than the timeout
        result = run_lispy_string('(with-timeout (timeout 200 "slow") "fallback" 100)', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fallback")
    
    def test_with_timeout_preserves_rejection(self):
        """Test with-timeout preserves original promise rejections."""
        result = run_lispy_string('(with-timeout (reject "error") "fallback" 1000)', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")
    
    def test_with_timeout_argument_validation(self):
        """Test with-timeout function argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(with-timeout (resolve 42))', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 1.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(with-timeout (resolve 42) "fallback" 1000 "extra")', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got 4.")
        
        # First argument not a promise
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(with-timeout "not-promise" "fallback" 1000)', self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'with-timeout' first argument must be a promise, got str.")
        
        # Invalid timeout type
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(with-timeout (resolve 42) "fallback" "not-number")', self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got str.")
        
        # Negative timeout
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(with-timeout (resolve 42) "fallback" -100)', self.env)
        self.assertEqual(str(cm.exception), "ValueError: 'with-timeout' timeout-ms must be non-negative, got -100.")
    
    def test_with_timeout_thread_first_compatibility(self):
        """Test with-timeout works with thread-first operator."""
        result = run_lispy_string('''
            (-> (resolve "data")
                (with-timeout "fallback" 1000)
                (promise-then (fn [x] (append "Result: " x))))
        ''', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "Result: data")
    
    def test_with_timeout_chaining_multiple(self):
        """Test chaining multiple with-timeout calls."""
        result = run_lispy_string('''
            (-> (timeout 50 "primary")
                (with-timeout "backup1" 25)
                (promise-then (fn [x] 
                  (if (equal? x "backup1") 
                    x 
                    (timeout 200 x))))
                (with-timeout "backup2" 100))
        ''', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "backup1")  # First timeout should trigger
    
    def test_timeout_with_promise_race(self):
        """Test timeout used with promise-race for timeout patterns."""
        result = run_lispy_string('''
            (promise-race (vector
                            (timeout 200 "slow")
                            (timeout 50 "fast")))
        ''', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.1)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fast")
    
    def test_complex_timeout_scenario(self):
        """Test complex scenario with multiple timeout patterns."""
        result = run_lispy_string('''
            (-> (promise-race (vector
                                (timeout 100 "operation-result")
                                (timeout 200 "timeout")))
                (promise-then (fn [result] 
                  (if (equal? result "timeout")
                    "fallback-data"
                    result)))
                (with-timeout "emergency-fallback" 300))
        ''', self.env)
        self.assertIsInstance(result, LispyPromise)
        
        time.sleep(0.15)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "operation-result")


if __name__ == '__main__':
    unittest.main() 
"""Tests for async-map function - concurrent async mapping"""

import unittest
import time
from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.parser import parse
from lispy.lexer import tokenize
from lispy.types import LispyPromise, Vector
from lispy.exceptions import EvaluationError
from lispy.functions import global_env


def run_lispy_string(code_string, env=None):
    """Helper function to run LisPy code from a string."""
    if env is None:
        env = Environment(outer=global_env)
    
    tokens = tokenize(code_string)
    parsed_expr = parse(tokens)
    return evaluate(parsed_expr, env)


class TestAsyncMap(unittest.TestCase):
    def setUp(self):
        self.env = Environment(outer=global_env)

    def test_async_map_basic_functionality(self):
        """Test basic async-map with timeout operations"""
        result = run_lispy_string('''
            (await (async-map [1 2 3] (fn [x] (timeout 50 (* x 2)))))
        ''', self.env)
        self.assertEqual(result, Vector([2, 4, 6]))

    def test_async_map_empty_collection(self):
        """Test async-map with empty collection"""
        result = run_lispy_string('''
            (await (async-map [] (fn [x] (timeout 50 x))))
        ''', self.env)
        self.assertEqual(result, Vector([]))

    def test_async_map_concurrent_execution(self):
        """Test that operations run concurrently, not sequentially"""
        start_time = time.time()
        
        result = run_lispy_string('''
            (await (async-map [100 100 100] (fn [x] (timeout x x))))
        ''', self.env)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Should take ~100ms (concurrent), not ~300ms (sequential)
        self.assertLess(execution_time, 200, "Operations should run concurrently")
        self.assertEqual(result, Vector([100, 100, 100]))

    def test_async_map_order_preservation(self):
        """Test that results maintain original order regardless of completion order"""
        result = run_lispy_string('''
            (await (async-map [200 50 100] (fn [x] (timeout x x))))
        ''', self.env)
        
        # Results should be in original order [200, 50, 100]
        # even though 50 completes first, then 100, then 200
        self.assertEqual(result, Vector([200, 50, 100]))

    def test_async_map_with_synchronous_callback(self):
        """Test async-map with synchronous callback function"""
        result = run_lispy_string('''
            (await (async-map [1 2 3 4] (fn [x] (* x x))))
        ''', self.env)
        self.assertEqual(result, Vector([1, 4, 9, 16]))

    def test_async_map_mixed_sync_async(self):
        """Test async-map with mixed synchronous and asynchronous operations"""
        result = run_lispy_string('''
            (await (async-map [1 2 3] (fn [x] 
                                        (if (= x 2)
                                          (timeout 50 (* x 10))  ; Async for 2
                                          (* x 10)))))           ; Sync for 1,3
        ''', self.env)
        self.assertEqual(result, Vector([10, 20, 30]))

    def test_async_map_fail_fast_behavior(self):
        """Test that async-map fails fast when any operation rejects"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('''
                (await (async-map [1 2 3] (fn [x]
                                            (if (= x 2)
                                              (reject "error on 2")
                                              (timeout 100 x)))))
            ''', self.env)
        
        self.assertIn("error on 2", str(cm.exception))

    def test_async_map_error_in_callback(self):
        """Test error handling when callback function throws"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('''
                (await (async-map [1 2 3] (fn [x]
                                            (if (= x 2)
                                              (/ x 0)  ; Division by zero
                                              (timeout 50 x)))))
            ''', self.env)
        
        self.assertIn("division by zero", str(cm.exception).lower())

    def test_async_map_thread_first_compatibility(self):
        """Test async-map works with thread-first operator"""
        result = run_lispy_string('''
            (-> [1 2 3 4 5]
                (async-map (fn [x] (timeout 30 (+ x 10))))
                (await))
        ''', self.env)
        self.assertEqual(result, Vector([11, 12, 13, 14, 15]))

    def test_async_map_with_promise_chaining(self):
        """Test async-map with promise chaining operations"""
        result = run_lispy_string('''
            (await (async-map [1 2 3] (fn [x]
                                        (-> (timeout 50 (* x 2))
                                            (promise-then (fn [y] (+ y 5)))))))
        ''', self.env)
        self.assertEqual(result, Vector([7, 9, 11]))

    def test_async_map_large_collection(self):
        """Test async-map with larger collection"""
        result = run_lispy_string('''
            (let [numbers (range 1 11)]  ; [1 2 3 4 5 6 7 8 9 10]
              (await (async-map numbers (fn [x] (timeout 20 (* x x))))))
        ''', self.env)
        expected = [i * i for i in range(1, 11)]
        self.assertEqual(result, Vector(expected))

    def test_async_map_invalid_collection_type(self):
        """Test async-map with invalid collection type"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(async-map "not-a-collection" (fn [x] x))', self.env)
        
        self.assertIn("expects a vector or list", str(cm.exception))

    def test_async_map_invalid_callback_type(self):
        """Test async-map with invalid callback type"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(async-map [1 2 3] "not-a-function")', self.env)
        
        self.assertIn("expects a function", str(cm.exception))

    def test_async_map_wrong_argument_count(self):
        """Test async-map with wrong number of arguments"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(async-map [1 2 3])', self.env)
        
        self.assertIn("expects 2 arguments", str(cm.exception))

    def test_async_map_with_lists(self):
        """Test async-map works with lists as well as vectors"""
        result = run_lispy_string('''
            (await (async-map (list 1 2 3) (fn [x] (timeout 30 (* x 3)))))
        ''', self.env)
        self.assertEqual(result, Vector([3, 6, 9]))

    def test_async_map_performance_comparison(self):
        """Test that async-map is significantly faster than sequential processing"""
        # Sequential version using functional reduce pattern
        start_sequential = time.time()
        run_lispy_string('''
            (reduce [100 100 100] 
                    (fn [acc x] (conj acc (await (timeout x x))))
                    [])
        ''', self.env)
        sequential_time = (time.time() - start_sequential) * 1000
        
        # Concurrent version with async-map
        start_concurrent = time.time()
        run_lispy_string('''
            (await (async-map [100 100 100] (fn [x] (timeout x x))))
        ''', self.env)
        concurrent_time = (time.time() - start_concurrent) * 1000
        
        # Concurrent should be significantly faster
        self.assertLess(concurrent_time, sequential_time * 0.6, 
                       "async-map should be much faster than sequential processing")


if __name__ == '__main__':
    unittest.main() 
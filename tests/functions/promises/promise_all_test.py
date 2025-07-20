"""Tests for promise-all function - waits for all promises to resolve"""

import unittest
import time
import threading
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.functions.promises.promise_all import promise_all
from lispy.functions.promises.resolve import resolve
from lispy.functions.promises.reject import reject
from lispy.functions.promises.promise import promise
from lispy.functions import create_global_env


class TestPromiseAll(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_promise_all_with_resolved_promises(self):
        """Test promise-all with pre-resolved promises"""
        promise1 = resolve([1], self.env)
        promise2 = resolve([2], self.env)
        promise3 = resolve([3], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        result = promise_all([promises], self.env)
        
        self.assertIsInstance(result, LispyPromise)
        
        # Wait for result to resolve
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector([1, 2, 3]))

    def test_promise_all_with_list_collection(self):
        """Test promise-all with list instead of vector"""
        promise1 = resolve([10], self.env)
        promise2 = resolve([20], self.env)
        
        promises = LispyList([promise1, promise2])
        result = promise_all([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, LispyList([10, 20]))

    def test_promise_all_empty_vector(self):
        """Test promise-all with empty vector resolves immediately"""
        empty_vector = Vector([])
        result = promise_all([empty_vector], self.env)
        
        # Should resolve immediately
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector([]))

    def test_promise_all_empty_list(self):
        """Test promise-all with empty list resolves immediately"""
        empty_list = LispyList([])
        result = promise_all([empty_list], self.env)
        
        # Should resolve immediately
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, LispyList([]))

    def test_promise_all_with_pending_promises(self):
        """Test promise-all with promises that resolve over time"""
        def slow_function_1(args, env):
            time.sleep(0.02)
            return "result1"
            
        def slow_function_2(args, env):
            time.sleep(0.01)
            return "result2"
            
        promise1 = promise([slow_function_1], self.env)
        promise2 = promise([slow_function_2], self.env)
        
        promises = Vector([promise1, promise2])
        result = promise_all([promises], self.env)
        
        # Should be pending initially
        self.assertEqual(result.state, "pending")
        
        # Wait for all to complete
        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector(["result1", "result2"]))

    def test_promise_all_preserves_order(self):
        """Test that promise-all preserves order regardless of completion order"""
        def fast_function(args, env):
            time.sleep(0.01)
            return "fast"
            
        def slow_function(args, env):
            time.sleep(0.03)
            return "slow"
            
        # Order: slow, fast - but fast completes first
        promise1 = promise([slow_function], self.env)
        promise2 = promise([fast_function], self.env)
        
        promises = Vector([promise1, promise2])
        result = promise_all([promises], self.env)
        
        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector(["slow", "fast"]))

    def test_promise_all_fail_fast_behavior(self):
        """Test that promise-all fails fast when any promise rejects"""
        promise1 = resolve(["success"], self.env)
        promise2 = reject(["error"], self.env)
        promise3 = resolve(["also success"], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        result = promise_all([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")

    def test_promise_all_with_mixed_promise_types(self):
        """Test promise-all with mix of resolved, rejected, and pending promises"""
        def pending_function(args, env):
            time.sleep(0.02)
            return "pending result"
            
        promise1 = resolve(["immediate"], self.env)
        promise2 = promise([pending_function], self.env)
        
        promises = Vector([promise1, promise2])
        result = promise_all([promises], self.env)
        
        time.sleep(0.03)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector(["immediate", "pending result"]))

    def test_promise_all_with_error_in_pending_promise(self):
        """Test promise-all when a pending promise rejects"""
        def error_function(args, env):
            time.sleep(0.01)
            raise ValueError("async error")
            
        promise1 = resolve(["success"], self.env)
        promise2 = promise([error_function], self.env)
        
        promises = Vector([promise1, promise2])
        result = promise_all([promises], self.env)
        
        time.sleep(0.02)
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        self.assertEqual(str(result.error), "async error")

    def test_promise_all_wrong_arg_count(self):
        """Test promise-all with wrong number of arguments"""
        with self.assertRaises(EvaluationError) as cm:
            promise_all([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-all' expects 1 argument, got 0."
        )

        with self.assertRaises(EvaluationError) as cm:
            promise_all([Vector([]), Vector([])], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-all' expects 1 argument, got 2."
        )

    def test_promise_all_invalid_collection_type(self):
        """Test promise-all with invalid collection type"""
        with self.assertRaises(EvaluationError) as cm:
            promise_all(["not a collection"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-all' argument must be a list or vector, got str."
        )

        with self.assertRaises(EvaluationError) as cm:
            promise_all([42], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-all' argument must be a list or vector, got int."
        )

    def test_promise_all_non_promise_elements(self):
        """Test promise-all with non-promise elements in collection"""
        promise1 = resolve([1], self.env)
        promises = Vector([promise1, "not a promise"])
        
        with self.assertRaises(EvaluationError) as cm:
            promise_all([promises], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: All elements must be promises, got str at position 1."
        )

    def test_promise_all_mixed_non_promises(self):
        """Test promise-all with multiple non-promise elements"""
        promises = Vector([42, "string", {}])
        
        with self.assertRaises(EvaluationError) as cm:
            promise_all([promises], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: All elements must be promises, got int at position 0."
        )

    def test_promise_all_single_promise(self):
        """Test promise-all with single promise"""
        promise = resolve(["single"], self.env)
        promises = Vector([promise])
        result = promise_all([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector(["single"]))

    def test_promise_all_concurrent_execution(self):
        """Test that promises run concurrently, not sequentially"""
        def timer_function(delay):
            def inner(args, env):
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                return delay
            return inner
            
        # Each promise takes 50ms, but should run concurrently
        promise1 = promise([timer_function(50)], self.env)
        promise2 = promise([timer_function(50)], self.env)
        promise3 = promise([timer_function(50)], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        
        # Measure how long promise-all takes to complete
        start_time = time.time()
        result = promise_all([promises], self.env)
        
        # Wait for completion
        while result.state == "pending":
            time.sleep(0.001)
            
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, Vector([50, 50, 50]))
        # Should take ~50ms (concurrent), not ~150ms (sequential)
        # Allow some overhead for thread scheduling and system variations
        self.assertLess(execution_time, 80, "Promises should execute concurrently")

    def test_promise_all_with_different_value_types(self):
        """Test promise-all with promises that resolve to different types"""
        promise1 = resolve([42], self.env)
        promise2 = resolve(["string"], self.env)
        promise3 = resolve([Vector([1, 2, 3])], self.env)
        promise4 = resolve([{"key": "value"}], self.env)
        promise5 = resolve([None], self.env)
        
        promises = Vector([promise1, promise2, promise3, promise4, promise5])
        result = promise_all([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        expected = Vector([42, "string", Vector([1, 2, 3]), {"key": "value"}, None])
        self.assertEqual(result.value, expected)

    def test_promise_all_thread_safety(self):
        """Test promise-all thread safety with concurrent operations"""
        def concurrent_function(value):
            def inner(args, env):
                # Simulate some concurrent work
                time.sleep(0.01)
                return value * 2
            return inner
            
        promises = Vector([
            promise([concurrent_function(i)], self.env) 
            for i in range(10)
        ])
        
        result = promise_all([promises], self.env)
        time.sleep(0.05)
        
        self.assertEqual(result.state, "resolved")
        expected = Vector([i * 2 for i in range(10)])
        self.assertEqual(result.value, expected)


if __name__ == "__main__":
    unittest.main() 
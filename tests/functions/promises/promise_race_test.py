"""Tests for promise-race function - first promise to resolve wins"""

import unittest
import time
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.functions.promises.promise_race import builtin_promise_race
from lispy.functions.promises.resolve import builtin_resolve
from lispy.functions.promises.reject import builtin_reject
from lispy.functions.promises.promise import builtin_promise
from lispy.functions import create_global_env


class TestPromiseRace(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_promise_race_first_resolves(self):
        """Test promise-race where first promise resolves first"""
        promise1 = builtin_resolve(["first"], self.env)
        promise2 = builtin_resolve(["second"], self.env)
        
        promises = Vector([promise1, promise2])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        # Should resolve with the first promise's value
        self.assertEqual(result.value, "first")

    def test_promise_race_different_timing(self):
        """Test promise-race with different timing scenarios"""
        def fast_function(args, env):
            time.sleep(0.01)
            return "fast"
            
        def slow_function(args, env):
            time.sleep(0.05)
            return "slow"
            
        fast_promise = builtin_promise([fast_function], self.env)
        slow_promise = builtin_promise([slow_function], self.env)
        
        promises = Vector([slow_promise, fast_promise])  # Slow first, fast second
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.03)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fast")  # Fast should win

    def test_promise_race_first_rejects(self):
        """Test promise-race where first promise rejects first"""
        def error_function(args, env):
            time.sleep(0.01)
            raise ValueError("first error")
            
        def slow_function(args, env):
            time.sleep(0.05)
            return "slow success"
            
        error_promise = builtin_promise([error_function], self.env)
        slow_promise = builtin_promise([slow_function], self.env)
        
        promises = Vector([error_promise, slow_promise])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.03)
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        self.assertEqual(str(result.error), "first error")

    def test_promise_race_pre_resolved_vs_pending(self):
        """Test promise-race mixing pre-resolved and pending promises"""
        resolved_promise = builtin_resolve(["immediate"], self.env)
        
        def slow_function(args, env):
            time.sleep(0.1)
            return "slow"
            
        slow_promise = builtin_promise([slow_function], self.env)
        
        promises = Vector([slow_promise, resolved_promise])
        result = builtin_promise_race([promises], self.env)
        
        # Immediate promise should win
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "immediate")

    def test_promise_race_pre_rejected_vs_pending(self):
        """Test promise-race mixing pre-rejected and pending promises"""
        rejected_promise = builtin_reject(["immediate error"], self.env)
        
        def slow_function(args, env):
            time.sleep(0.1)
            return "slow"
            
        slow_promise = builtin_promise([slow_function], self.env)
        
        promises = Vector([slow_promise, rejected_promise])
        result = builtin_promise_race([promises], self.env)
        
        # Immediate rejection should win
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "immediate error")

    def test_promise_race_with_list_collection(self):
        """Test promise-race with list instead of vector"""
        promise1 = builtin_resolve(["first"], self.env)
        promise2 = builtin_resolve(["second"], self.env)
        
        promises = LispyList([promise1, promise2])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "first")

    def test_promise_race_empty_collection(self):
        """Test promise-race with empty collection"""
        empty_vector = Vector([])
        result = builtin_promise_race([empty_vector], self.env)
        
        # Should remain pending forever (or until timeout)
        time.sleep(0.01)
        self.assertEqual(result.state, "pending")

    def test_promise_race_single_promise(self):
        """Test promise-race with single promise"""
        promise = builtin_resolve(["single"], self.env)
        promises = Vector([promise])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "single")

    def test_promise_race_all_resolved(self):
        """Test promise-race with all pre-resolved promises"""
        promise1 = builtin_resolve(["first"], self.env)
        promise2 = builtin_resolve(["second"], self.env)
        promise3 = builtin_resolve(["third"], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "first")  # First in array wins

    def test_promise_race_all_rejected(self):
        """Test promise-race with all pre-rejected promises"""
        promise1 = builtin_reject(["first error"], self.env)
        promise2 = builtin_reject(["second error"], self.env)
        promise3 = builtin_reject(["third error"], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "first error")  # First in array wins

    def test_promise_race_wrong_arg_count(self):
        """Test promise-race with wrong number of arguments"""
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_race([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-race' expects 1 argument, got 0."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_race([Vector([]), Vector([])], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'promise-race' expects 1 argument, got 2."
        )

    def test_promise_race_invalid_collection_type(self):
        """Test promise-race with invalid collection type"""
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_race(["not a collection"], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'promise-race' argument must be a list or vector, got str."
        )

    def test_promise_race_non_promise_elements(self):
        """Test promise-race with non-promise elements"""
        promise = builtin_resolve([1], self.env)
        promises = Vector([promise, "not a promise"])
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_promise_race([promises], self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: All elements must be promises, got str at position 1."
        )

    def test_promise_race_timing_precision(self):
        """Test promise-race with very close timing"""
        def timed_function(delay, value):
            def inner(args, env):
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                return value
            return inner
            
        # Both promises very close in timing
        promise1 = builtin_promise([timed_function(25, "first")], self.env)
        promise2 = builtin_promise([timed_function(30, "second")], self.env)
        
        promises = Vector([promise1, promise2])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.05)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "first")  # First should win

    def test_promise_race_mixed_success_failure(self):
        """Test promise-race with mixed success and failure scenarios"""
        def success_function(args, env):
            time.sleep(0.02)
            return "success"
            
        def error_function(args, env):
            time.sleep(0.03)
            raise ValueError("error")
            
        success_promise = builtin_promise([success_function], self.env)
        error_promise = builtin_promise([error_function], self.env)
        
        promises = Vector([success_promise, error_promise])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.05)
        # Success should win because it completes first
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "success")

    def test_promise_race_with_different_value_types(self):
        """Test promise-race with different value types"""
        promise1 = builtin_resolve([42], self.env)
        promise2 = builtin_resolve(["string"], self.env)
        promise3 = builtin_resolve([Vector([1, 2, 3])], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        result = builtin_promise_race([promises], self.env)
        
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)  # First wins

    def test_promise_race_concurrent_resolution(self):
        """Test promise-race with truly concurrent operations"""
        def concurrent_function(delay, value):
            def inner(args, env):
                time.sleep(delay / 1000.0)
                return value
            return inner
            
        # All promises start at same time
        promise1 = builtin_promise([concurrent_function(30, "slow")], self.env)
        promise2 = builtin_promise([concurrent_function(10, "fast")], self.env)
        promise3 = builtin_promise([concurrent_function(20, "medium")], self.env)
        
        promises = Vector([promise1, promise2, promise3])
        
        # Measure how long the race takes to resolve
        start_time = time.time()
        result = builtin_promise_race([promises], self.env)
        
        # Wait for result to be available
        while result.state == "pending":
            time.sleep(0.001)
            
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "fast")  # Fastest should win
        # Should complete close to the fastest promise time (10ms), with some overhead
        self.assertLess(execution_time, 30, "Should complete in time of fastest promise")


if __name__ == "__main__":
    unittest.main() 
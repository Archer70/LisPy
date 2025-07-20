"""Tests for on-complete function - handles promise completion regardless of outcome"""

import unittest
import time
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.closure import Function
from lispy.types import Symbol
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.functions.promises.on_complete import on_complete
from lispy.functions.promises.resolve import resolve
from lispy.functions.promises.reject import reject
from lispy.functions.promises.promise import promise


class TestOnComplete(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_on_complete_with_resolved_promise(self):
        """Test on-complete with resolved promise"""
        result = run_lispy_string('(on-complete (resolve "success") (fn [p] "cleanup done"))', self.env)
        
        self.assertIsInstance(result, LispyPromise)
        # on-complete should preserve original resolution
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "success")

    def test_on_complete_with_rejected_promise(self):
        """Test on-complete with rejected promise"""
        result = run_lispy_string('(on-complete (reject "error") (fn [p] "cleanup done"))', self.env)
        
        # on-complete should preserve original rejection
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")

    def test_on_complete_with_pending_promise_that_resolves(self):
        """Test on-complete with pending promise that eventually resolves"""
        def success_function(args, env):
            time.sleep(0.01)
            return "async success"
            
        promise_obj = promise([success_function], self.env)
        
        def completion_handler(args, env):
            return "handler executed"
            
        result = on_complete([promise_obj, completion_handler], self.env)
        
        # Should be pending initially
        self.assertEqual(result.state, "pending")
        
        # Wait for completion
        time.sleep(0.02)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "async success")

    def test_on_complete_with_pending_promise_that_rejects(self):
        """Test on-complete with pending promise that eventually rejects"""
        def error_function(args, env):
            time.sleep(0.01)
            raise ValueError("async error")
            
        promise_obj = promise([error_function], self.env)
        
        def completion_handler(args, env):
            return "handler executed"
            
        result = on_complete([promise_obj, completion_handler], self.env)
        
        # Should be pending initially
        self.assertEqual(result.state, "pending")
        
        # Wait for completion
        time.sleep(0.02)
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        self.assertEqual(str(result.error), "async error")

    def test_on_complete_handler_throws_error(self):
        """Test on-complete when completion handler throws an error"""
        result = run_lispy_string('(on-complete (resolve "success") (fn [p] (throw "handler failed")))', self.env)
        
        # Should reject with handler error, not preserve original resolution
        self.assertEqual(result.state, "rejected")
        self.assertEqual(str(result.error), "handler failed")

    def test_on_complete_handler_with_rejected_promise_throws(self):
        """Test on-complete when handler throws on rejected promise"""
        result = run_lispy_string('(on-complete (reject "original error") (fn [p] (throw "handler failed")))', self.env)
        
        # Should reject with handler error, not original error
        self.assertEqual(result.state, "rejected")
        self.assertEqual(str(result.error), "handler failed")

    def test_on_complete_side_effects_tracking(self):
        """Test on-complete handler executes for side effects"""
        promise = resolve(["data"], self.env)
        
        # Track that handler was called
        handler_called = []
        
        def tracking_handler(args, env):
            handler_called.append("called")
            return "side effect done"
            
        result = on_complete([promise, tracking_handler], self.env)
        
        time.sleep(0.01)
        self.assertEqual(len(handler_called), 1)
        self.assertEqual(handler_called[0], "called")
        # Original value preserved
        self.assertEqual(result.value, "data")

    def test_on_complete_chaining_multiple_handlers(self):
        """Test chaining multiple on-complete handlers"""
        promise = resolve(["start"], self.env)
        
        call_order = []
        
        def handler1(args, env):
            call_order.append("handler1")
            return "first cleanup"
            
        def handler2(args, env):
            call_order.append("handler2")
            return "second cleanup"
            
        result1 = on_complete([promise, handler1], self.env)
        result2 = on_complete([result1, handler2], self.env)
        
        time.sleep(0.01)
        self.assertEqual(len(call_order), 2)
        self.assertEqual(call_order, ["handler1", "handler2"])
        # Original value preserved through chain
        self.assertEqual(result2.value, "start")

    def test_on_complete_wrong_arg_count(self):
        """Test on-complete with wrong number of arguments"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete (resolve 1))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-complete' expects 2 arguments (promise cleanup-callback), got 1."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete (resolve 1) (fn [x] x) "extra")', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'on-complete' expects 2 arguments (promise cleanup-callback), got 3."
        )

    def test_on_complete_invalid_promise_type(self):
        """Test on-complete with non-promise first argument"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete "not a promise" (fn [x] "handled"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' first argument must be a promise, got str."
        )

    def test_on_complete_invalid_handler_type(self):
        """Test on-complete with non-function handler"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete (resolve 1) "not a function")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' second argument must be a function, got str."
        )

    def test_on_complete_handler_wrong_parameter_count(self):
        """Test on-complete with handler that has wrong parameter count"""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(on-complete (resolve 1) (fn [x y] x))', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'on-complete' callback must take exactly 1 argument, got 2."
        )

    def test_on_complete_cleanup_pattern(self):
        """Test on-complete used for cleanup/finally pattern"""
        def resource_operation(args, env):
            time.sleep(0.01)
            # Simulate some resource operation
            return "operation result"
            
        promise_obj = promise([resource_operation], self.env)
        
        cleanup_executed = []
        
        def cleanup_handler(args, env):
            cleanup_executed.append("resource cleaned up")
            return "cleanup complete"
            
        result = on_complete([promise_obj, cleanup_handler], self.env)
        
        time.sleep(0.02)
        
        # Operation should succeed
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "operation result")
        
        # Cleanup should have executed
        self.assertEqual(len(cleanup_executed), 1)
        self.assertEqual(cleanup_executed[0], "resource cleaned up")

    def test_on_complete_with_error_cleanup_pattern(self):
        """Test on-complete cleanup executes even when operation fails"""
        def failing_operation(args, env):
            time.sleep(0.01)
            raise ValueError("operation failed")
            
        promise_obj = promise([failing_operation], self.env)
        
        cleanup_executed = []
        
        def cleanup_handler(args, env):
            cleanup_executed.append("cleanup despite error")
            return "cleanup complete"
            
        result = on_complete([promise_obj, cleanup_handler], self.env)
        
        time.sleep(0.02)
        
        # Operation should fail
        self.assertEqual(result.state, "rejected")
        self.assertIsInstance(result.error, ValueError)
        
        # But cleanup should still have executed
        self.assertEqual(len(cleanup_executed), 1)
        self.assertEqual(cleanup_executed[0], "cleanup despite error")

    def test_on_complete_with_different_completion_handlers(self):
        """Test on-complete with different types of completion handlers"""
        # Simple logging handler
        logs = []
        
        def log_handler(args, env):
            logs.append("operation completed")
            
        promise1 = resolve(["success"], self.env)
        result1 = on_complete([promise1, log_handler], self.env)
        
        # Metric collection handler
        metrics = {"completions": 0}
        
        def metric_handler(args, env):
            metrics["completions"] += 1
            
        promise2 = reject(["error"], self.env)
        result2 = on_complete([promise2, metric_handler], self.env)
        
        time.sleep(0.01)
        
        # Both handlers should have executed
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0], "operation completed")
        self.assertEqual(metrics["completions"], 1)
        
        # Original outcomes preserved
        self.assertEqual(result1.state, "resolved")
        self.assertEqual(result1.value, "success")
        self.assertEqual(result2.state, "rejected")
        self.assertEqual(result2.error, "error")

    def test_on_complete_with_promise_chain_integration(self):
        """Test on-complete integrated in promise chains"""
        # Complex chain with multiple completions using thread-first operator
        result = run_lispy_string('''
            (-> (resolve "start")
                (promise-then (fn [x] "step1 done"))
                (on-complete (fn [p] nil))
                (promise-then (fn [x] "step2 done"))
                (on-complete (fn [p] nil)))
        ''', self.env)
        
        # Final result should be correct
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "step2 done")


if __name__ == "__main__":
    unittest.main() 
"""Tests for reject function - creates immediately rejected promises"""

import unittest
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.functions.promises.reject import reject


class TestReject(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_reject_with_string_error(self):
        """Test reject with string error messages"""
        result = reject(["error message"], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error message")

        result = reject([""], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "")

        result = reject(["Multi\nline\nerror"], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "Multi\nline\nerror")

    def test_reject_with_number_error(self):
        """Test reject with numeric error codes"""
        result = reject([404], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, 404)

        result = reject([0], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, 0)

        result = reject([-1], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, -1)

        result = reject([3.14], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, 3.14)

    def test_reject_with_boolean_error(self):
        """Test reject with boolean error values"""
        result = reject([False], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, False)

        result = reject([True], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, True)

    def test_reject_with_nil_error(self):
        """Test reject with nil error value"""
        result = reject([None], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, None)

    def test_reject_with_vector_error(self):
        """Test reject with vector error data"""
        error_vector = Vector(["error", "details", 123])
        result = reject([error_vector], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, error_vector)

        empty_vector = Vector([])
        result = reject([empty_vector], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, empty_vector)

    def test_reject_with_list_error(self):
        """Test reject with list error data"""
        error_list = LispyList(["error", "type", "validation"])
        result = reject([error_list], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, error_list)

    def test_reject_with_dict_error(self):
        """Test reject with dictionary/map error data"""
        error_dict = {"error": "not found", "code": 404, "path": "/api/user"}
        result = reject([error_dict], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, error_dict)

        empty_dict = {}
        result = reject([empty_dict], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, empty_dict)

    def test_reject_with_nested_error_structures(self):
        """Test reject with complex nested error structures"""
        nested_error = {
            "type": "ValidationError",
            "details": Vector(["field1", "field2"]),
            "context": {"user": "test", "action": "create"},
            "stack": LispyList(["func1", "func2", "main"])
        }
        result = reject([nested_error], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, nested_error)

    def test_reject_wrong_arg_count_zero(self):
        """Test reject with no arguments"""
        with self.assertRaises(EvaluationError) as cm:
            reject([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'reject' expects 1 argument (error), got 0."
        )

    def test_reject_wrong_arg_count_many(self):
        """Test reject with too many arguments"""
        with self.assertRaises(EvaluationError) as cm:
            reject(["error1", "error2"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'reject' expects 1 argument (error), got 2."
        )

        with self.assertRaises(EvaluationError) as cm:
            reject(["error1", "error2", "error3"], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'reject' expects 1 argument (error), got 3."
        )

    def test_reject_immediate_availability(self):
        """Test that rejected promises are immediately available"""
        result = reject(["immediate error"], self.env)
        
        # Should be immediately rejected, no waiting needed
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "immediate error")

    def test_reject_chain_error_propagation(self):
        """Test reject propagates through promise chains"""
        result = reject(["original error"], self.env)
        
        # then() should be skipped, error should propagate
        chained = result.then(lambda x: "should not execute")
        self.assertEqual(chained.state, "rejected")
        self.assertEqual(chained.error, "original error")

    def test_reject_error_handling_compatibility(self):
        """Test reject works with error handling chains"""
        result = reject(["test error"], self.env)
        
        # Should trigger catch handler
        caught = result.catch(lambda e: f"handled: {e}")
        self.assertEqual(caught.state, "resolved")
        self.assertEqual(caught.value, "handled: test error")

    def test_reject_with_exception_object(self):
        """Test reject with actual exception objects"""
        test_exception = ValueError("test exception")
        result = reject([test_exception], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, test_exception)

        # Verify it's the same exception instance
        self.assertIs(result.error, test_exception)

    def test_reject_multiple_catch_handlers(self):
        """Test reject with multiple catch handlers in chain"""
        result = reject(["original"], self.env)
        
        # First catch should handle the error
        caught1 = result.catch(lambda e: f"first: {e}")
        caught2 = caught1.catch(lambda e: f"second: {e}")
        
        self.assertEqual(caught1.state, "resolved")
        self.assertEqual(caught1.value, "first: original")
        self.assertEqual(caught2.state, "resolved")
        self.assertEqual(caught2.value, "first: original")  # Second catch not triggered

    def test_reject_then_catch_chain(self):
        """Test reject in then-catch chains"""
        result = reject(["error"], self.env)
        
        # Complex chain: reject -> then (skipped) -> catch (handles) -> then (executes)
        chain = (result
                .then(lambda x: f"processed: {x}")  # Skipped
                .catch(lambda e: f"handled: {e}")   # Executes
                .then(lambda x: f"final: {x}"))     # Executes
        
        self.assertEqual(chain.state, "resolved")
        self.assertEqual(chain.value, "final: handled: error")

    def test_reject_with_function_object_error(self):
        """Test reject with function objects as error"""
        def error_fn():
            return "error function"
            
        result = reject([error_fn], self.env)
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, error_fn)


if __name__ == "__main__":
    unittest.main() 
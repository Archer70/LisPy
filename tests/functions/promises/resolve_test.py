"""Tests for resolve function - creates immediately resolved promises"""

import unittest
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Vector, LispyList
from lispy.functions.promises.resolve import builtin_resolve
from lispy.functions import create_global_env


class TestResolve(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_resolve_with_number(self):
        """Test resolve with numeric values"""
        result = builtin_resolve([42], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

        result = builtin_resolve([3.14], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 3.14)

        result = builtin_resolve([0], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 0)

        result = builtin_resolve([-42], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, -42)

    def test_resolve_with_string(self):
        """Test resolve with string values"""
        result = builtin_resolve(["hello"], self.env)
        self.assertIsInstance(result, LispyPromise)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "hello")

        result = builtin_resolve([""], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "")

        result = builtin_resolve(["multi\nline\nstring"], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "multi\nline\nstring")

    def test_resolve_with_boolean(self):
        """Test resolve with boolean values"""
        result = builtin_resolve([True], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, True)

        result = builtin_resolve([False], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, False)

    def test_resolve_with_nil(self):
        """Test resolve with nil value"""
        result = builtin_resolve([None], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, None)

    def test_resolve_with_vector(self):
        """Test resolve with vector collections"""
        vector = Vector([1, 2, 3])
        result = builtin_resolve([vector], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, vector)

        empty_vector = Vector([])
        result = builtin_resolve([empty_vector], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, empty_vector)

    def test_resolve_with_list(self):
        """Test resolve with list collections"""
        lispy_list = LispyList([1, 2, 3])
        result = builtin_resolve([lispy_list], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, lispy_list)

        empty_list = LispyList([])
        result = builtin_resolve([empty_list], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, empty_list)

    def test_resolve_with_dict(self):
        """Test resolve with dictionary/map values"""
        test_dict = {"key": "value", "count": 42}
        result = builtin_resolve([test_dict], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, test_dict)

        empty_dict = {}
        result = builtin_resolve([empty_dict], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, empty_dict)

    def test_resolve_with_nested_structures(self):
        """Test resolve with nested data structures"""
        nested = {
            "list": [1, 2, Vector([3, 4])],
            "dict": {"inner": "value"},
            "mixed": Vector([1, {"key": "val"}, LispyList([5, 6])])
        }
        result = builtin_resolve([nested], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, nested)

    def test_resolve_wrong_arg_count_zero(self):
        """Test resolve with no arguments"""
        with self.assertRaises(EvaluationError) as cm:
            builtin_resolve([], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'resolve' expects 1 argument (value), got 0."
        )

    def test_resolve_wrong_arg_count_many(self):
        """Test resolve with too many arguments"""
        with self.assertRaises(EvaluationError) as cm:
            builtin_resolve([1, 2], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'resolve' expects 1 argument (value), got 2."
        )

        with self.assertRaises(EvaluationError) as cm:
            builtin_resolve([1, 2, 3], self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'resolve' expects 1 argument (value), got 3."
        )

    def test_resolve_immediate_availability(self):
        """Test that resolved promises are immediately available"""
        result = builtin_resolve(["immediate"], self.env)
        
        # Should be immediately resolved, no waiting needed
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, "immediate")
        
        # Can be used immediately in then/catch chains
        chained = result.then(lambda x: x.upper())
        self.assertEqual(chained.state, "resolved")
        self.assertEqual(chained.value, "IMMEDIATE")

    def test_resolve_with_function_object(self):
        """Test resolve with function objects"""
        def test_fn():
            return "function result"
            
        result = builtin_resolve([test_fn], self.env)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, test_fn)

    def test_resolve_chain_compatibility(self):
        """Test resolve works in promise chains"""
        result = builtin_resolve([10], self.env)
        
        # Chain multiple operations
        chain1 = result.then(lambda x: x * 2)
        chain2 = chain1.then(lambda x: x + 5)
        
        self.assertEqual(chain1.state, "resolved")
        self.assertEqual(chain1.value, 20)
        self.assertEqual(chain2.state, "resolved")
        self.assertEqual(chain2.value, 25)

    def test_resolve_error_handling_compatibility(self):
        """Test resolve works with error handling chains"""
        result = builtin_resolve(["success"], self.env)
        
        # Should not trigger catch handler
        caught = result.catch(lambda e: "error handled")
        self.assertEqual(caught.state, "resolved")
        self.assertEqual(caught.value, "success")


if __name__ == "__main__":
    unittest.main() 
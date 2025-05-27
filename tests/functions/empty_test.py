# tests/functions/empty_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env # To get an environment with 'empty?'
from lispy.exceptions import EvaluationError
from lispy.types import Symbol, Vector # For type checking in expected results if needed
from lispy.closure import Function # Import Function for testing

class EmptyFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env() # This env will need 'empty?' to be defined

    def test_empty_true_list(self):
        self.assertTrue(run_lispy_string("(empty? (list))", self.env))

    def test_empty_true_vector(self):
        self.assertTrue(run_lispy_string("(empty? [])", self.env))

    def test_empty_true_map(self):
        self.assertTrue(run_lispy_string("(empty? {})", self.env))

    def test_empty_true_string(self):
        self.assertTrue(run_lispy_string('(empty? "")', self.env))
        
    def test_empty_true_nil(self):
        self.assertTrue(run_lispy_string("(empty? nil)", self.env))

    def test_empty_false_list(self):
        self.assertFalse(run_lispy_string("(empty? (list 1 2))", self.env))

    def test_empty_false_vector(self):
        self.assertFalse(run_lispy_string("(empty? [1 2])", self.env))

    def test_empty_false_map(self):
        self.assertFalse(run_lispy_string('(empty? {:a 1})', self.env))

    def test_empty_false_string(self):
        self.assertFalse(run_lispy_string('(empty? "hello")', self.env))

    def test_empty_arg_count_error_none(self):
        # with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'empty?' expects 1 argument, got 0\\."):
        #     run_lispy_string("(empty?)", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(empty?)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'empty?' expects 1 argument, got 0.")

    def test_empty_arg_count_error_many(self):
        # with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'empty?' expects 1 argument, got 2\\."):
        #     run_lispy_string('(empty? [] "")', self.env) # Vector and string as two args
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(empty? [] "")', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'empty?' expects 1 argument, got 2.")

    def test_empty_type_error_number(self):
        # with self.assertRaisesRegex(EvaluationError, r"TypeError: 'empty?' expects a list, vector, map, string, or nil. Got int"):
        #     run_lispy_string("(empty? 123)", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(empty? 123)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'empty?' expects a list, vector, map, string, or nil. Got int")
            
    def test_empty_type_error_boolean(self):
        # with self.assertRaisesRegex(EvaluationError, r"TypeError: 'empty?' expects a list, vector, map, string, or nil. Got bool"):
        #     run_lispy_string("(empty? true)", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(empty? true)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'empty?' expects a list, vector, map, string, or nil. Got bool")
            
    def test_empty_type_error_function(self):
        # Create a dummy function object directly
        dummy_fn = Function(params=[], body=[], defining_env=self.env)
        self.env.define("my_dummy_fn", dummy_fn)
        # with self.assertRaisesRegex(EvaluationError, r"TypeError: 'empty?' expects a list, vector, map, string, or nil. Got Function"):
        #     run_lispy_string("(empty? my_dummy_fn)", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(empty? my_dummy_fn)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'empty?' expects a list, vector, map, string, or nil. Got Function")

if __name__ == '__main__':
    unittest.main() 
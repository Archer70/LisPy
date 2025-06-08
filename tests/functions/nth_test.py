import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector, Symbol

class NthFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_nth_vector_valid_index(self):
        """Test (nth [10 20 30] 0) returns 10."""
        result = run_lispy_string("(nth [10 20 30] 0)", self.env)
        self.assertEqual(result, 10)
        
        result = run_lispy_string("(nth [10 20 30] 1)", self.env)
        self.assertEqual(result, 20)
        
        result = run_lispy_string("(nth [10 20 30] 2)", self.env)
        self.assertEqual(result, 30)

    def test_nth_list_valid_index(self):
        """Test (nth '(10 20 30) 0) returns 10."""
        result = run_lispy_string("(nth '(10 20 30) 0)", self.env)
        self.assertEqual(result, 10)
        
        result = run_lispy_string("(nth '(10 20 30) 1)", self.env)
        self.assertEqual(result, 20)
        
        result = run_lispy_string("(nth '(10 20 30) 2)", self.env)
        self.assertEqual(result, 30)

    def test_nth_vector_out_of_bounds_no_default(self):
        """Test nth raises IndexError for out of bounds access without default."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [10 20 30] 3)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: 3 out of bounds for collection of size 3.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [10 20 30] -1)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: -1 out of bounds for collection of size 3.")

    def test_nth_list_out_of_bounds_no_default(self):
        """Test nth raises IndexError for out of bounds access without default."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth '(10 20 30) 3)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: 3 out of bounds for collection of size 3.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth '(10 20 30) -1)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: -1 out of bounds for collection of size 3.")

    def test_nth_vector_out_of_bounds_with_default(self):
        """Test nth returns default for out of bounds access with default."""
        result = run_lispy_string("(nth [10 20 30] 3 \"default\")", self.env)
        self.assertEqual(result, "default")
        
        result = run_lispy_string("(nth [10 20 30] -1 nil)", self.env)
        self.assertIsNone(result)
        
        result = run_lispy_string("(nth [10 20 30] 5 42)", self.env)
        self.assertEqual(result, 42)

    def test_nth_list_out_of_bounds_with_default(self):
        """Test nth returns default for out of bounds access with default."""
        result = run_lispy_string("(nth '(10 20 30) 3 \"default\")", self.env)
        self.assertEqual(result, "default")
        
        result = run_lispy_string("(nth '(10 20 30) -1 nil)", self.env)
        self.assertIsNone(result)
        
        result = run_lispy_string("(nth '(10 20 30) 5 42)", self.env)
        self.assertEqual(result, 42)

    def test_nth_empty_vector(self):
        """Test nth with empty vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [] 0)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: 0 out of bounds for collection of size 0.")
        
        result = run_lispy_string("(nth [] 0 \"empty\")", self.env)
        self.assertEqual(result, "empty")

    def test_nth_empty_list(self):
        """Test nth with empty list."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth '() 0)", self.env)
        self.assertEqual(str(cm.exception), "IndexError: 0 out of bounds for collection of size 0.")
        
        result = run_lispy_string("(nth '() 0 \"empty\")", self.env)
        self.assertEqual(result, "empty")

    def test_nth_mixed_type_collections(self):
        """Test nth with mixed type collections."""
        result = run_lispy_string("(nth [1 \"hello\" 2.5 true] 1)", self.env)
        self.assertEqual(result, "hello")
        
        result = run_lispy_string("(nth '(1 \"hello\" 2.5 true) 2)", self.env)
        self.assertEqual(result, 2.5)
        
        result = run_lispy_string("(nth [1 \"hello\" 2.5 true] 3)", self.env)
        self.assertTrue(result)

    # --- Argument Validation Tests ---
    def test_nth_too_few_args(self):
        """Test nth with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'nth' expects 2 or 3 arguments, got 0.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [1 2 3])", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'nth' expects 2 or 3 arguments, got 1.")

    def test_nth_too_many_args(self):
        """Test nth with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [1 2 3] 0 'default 'extra)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'nth' expects 2 or 3 arguments, got 4.")

    def test_nth_invalid_collection_type(self):
        """Test nth with invalid collection type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth \"not-a-collection\" 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'nth' first argument must be a vector or list, got <class 'str'>.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth 123 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'nth' first argument must be a vector or list, got <class 'int'>.")

    def test_nth_invalid_index_type(self):
        """Test nth with invalid index type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [1 2 3] \"not-a-number\")", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'nth' index must be an integer, got <class 'str'>.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(nth [1 2 3] 1.5)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'nth' index must be an integer, got <class 'float'>.")

    def test_nth_with_thread_first(self):
        """Test nth used with the -> (thread-first) special form."""
        result = run_lispy_string("(-> [10 20 30 40] (nth 1))", self.env)
        self.assertEqual(result, 20)
        
        result = run_lispy_string("(-> '(10 20 30 40) (nth 2))", self.env)
        self.assertEqual(result, 30)
        
        result = run_lispy_string("(-> [10 20 30] (nth 5 \"default\"))", self.env)
        self.assertEqual(result, "default")

if __name__ == '__main__':
    unittest.main() 
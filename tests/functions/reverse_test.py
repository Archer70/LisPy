import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector


class ReverseFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_reverse_empty_vector(self):
        """Test (reverse []) returns []."""
        result = run_lispy_string("(reverse [])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_reverse_empty_list(self):
        """Test (reverse '()) returns '()."""
        result = run_lispy_string("(reverse '())", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([]))

    def test_reverse_single_element_vector(self):
        """Test (reverse [42]) returns [42]."""
        result = run_lispy_string("(reverse [42])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([42]))

    def test_reverse_single_element_list(self):
        """Test (reverse '(42)) returns (42)."""
        result = run_lispy_string("(reverse '(42))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([42]))

    def test_reverse_numbers_vector(self):
        """Test (reverse [1 2 3 4 5]) returns [5 4 3 2 1]."""
        result = run_lispy_string("(reverse [1 2 3 4 5])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([5, 4, 3, 2, 1]))

    def test_reverse_numbers_list(self):
        """Test (reverse '(1 2 3 4 5)) returns (5 4 3 2 1)."""
        result = run_lispy_string("(reverse '(1 2 3 4 5))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([5, 4, 3, 2, 1]))

    def test_reverse_mixed_types_vector(self):
        """Test reverse works with mixed types in vector."""
        result = run_lispy_string('(reverse [1 "hello" 3.14 true])', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([True, 3.14, "hello", 1]))

    def test_reverse_mixed_types_list(self):
        """Test reverse works with mixed types in list."""
        result = run_lispy_string('(reverse \'(1 "hello" 3.14 true))', self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([True, 3.14, "hello", 1]))

    def test_reverse_strings_vector(self):
        """Test (reverse ["apple" "banana" "cherry"]) works correctly."""
        result = run_lispy_string('(reverse ["apple" "banana" "cherry"])', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["cherry", "banana", "apple"]))

    def test_reverse_original_vector_unchanged(self):
        """Test that reverse does not mutate the original vector."""
        run_lispy_string("(define my-vec [10 20 30 40])", self.env)
        run_lispy_string("(reverse my-vec)", self.env)
        original_vec = run_lispy_string("my-vec", self.env)
        self.assertIsInstance(original_vec, Vector)
        self.assertEqual(original_vec, Vector([10, 20, 30, 40]))

    def test_reverse_original_list_unchanged(self):
        """Test that reverse does not mutate the original list."""
        run_lispy_string("(define my-list '(10 20 30 40))", self.env)
        run_lispy_string("(reverse my-list)", self.env)
        original_list = run_lispy_string("my-list", self.env)
        self.assertIsInstance(original_list, LispyList)
        self.assertEqual(original_list, LispyList([10, 20, 30, 40]))

    # --- Argument Validation Tests ---
    def test_reverse_too_few_args(self):
        """Test reverse with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reverse)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'reverse' expects 1 argument, got 0.")

    def test_reverse_too_many_args(self):
        """Test reverse with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reverse [] 'extra)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'reverse' expects 1 argument, got 2.")

    def test_reverse_collection_not_list_or_vector(self):
        """Test reverse when collection is not a list or vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(reverse "abc")', self.env)
        self.assertEqual(str(cm.exception), "TypeError: Argument to 'reverse' must be a list or vector, got <class 'str'>.")
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reverse 123)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: Argument to 'reverse' must be a list or vector, got <class 'int'>.")

    def test_reverse_with_thread_first(self):
        """Test reverse used with the -> (thread-first) macro."""
        result = run_lispy_string("(-> [1 2 3 4 5] (reverse))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([5, 4, 3, 2, 1]))
        
        result_list = run_lispy_string("(-> '(1 2 3 4 5) (reverse))", self.env)
        self.assertIsInstance(result_list, LispyList)
        self.assertEqual(result_list, LispyList([5, 4, 3, 2, 1]))

    def test_reverse_twice_returns_original(self):
        """Test that reversing twice returns the original order."""
        result = run_lispy_string("(-> [1 2 3 4 5] (reverse) (reverse))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))


if __name__ == '__main__':
    unittest.main() 
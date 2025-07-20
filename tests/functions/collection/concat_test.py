import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyList, Vector
from lispy.utils import run_lispy_string


class ConcatFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_concat_empty_args(self):
        """Test (concat) returns []."""
        result = run_lispy_string("(concat)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_concat_single_vector(self):
        """Test (concat [1 2 3]) returns [1 2 3]."""
        result = run_lispy_string("(concat [1 2 3])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_concat_single_list(self):
        """Test (concat '(1 2 3)) returns (1 2 3)."""
        result = run_lispy_string("(concat '(1 2 3))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([1, 2, 3]))

    def test_concat_two_vectors(self):
        """Test (concat [1 2] [3 4]) returns [1 2 3 4]."""
        result = run_lispy_string("(concat [1 2] [3 4])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4]))

    def test_concat_two_lists(self):
        """Test (concat '(1 2) '(3 4)) returns (1 2 3 4)."""
        result = run_lispy_string("(concat '(1 2) '(3 4))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([1, 2, 3, 4]))

    def test_concat_multiple_vectors(self):
        """Test (concat [1] [2 3] [4 5 6]) returns [1 2 3 4 5 6]."""
        result = run_lispy_string("(concat [1] [2 3] [4 5 6])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5, 6]))

    def test_concat_multiple_lists(self):
        """Test (concat '(1) '(2 3) '(4 5 6)) returns (1 2 3 4 5 6)."""
        result = run_lispy_string("(concat '(1) '(2 3) '(4 5 6))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([1, 2, 3, 4, 5, 6]))

    def test_concat_mixed_types_vector_first(self):
        """Test concat with mixed collection types, vector first."""
        result = run_lispy_string("(concat [1 2] '(3 4) [5])", self.env)
        self.assertIsInstance(result, Vector)  # Result type matches first arg
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

    def test_concat_mixed_types_list_first(self):
        """Test concat with mixed collection types, list first."""
        result = run_lispy_string("(concat '(1 2) [3 4] '(5))", self.env)
        self.assertIsInstance(result, LispyList)  # Result type matches first arg
        self.assertEqual(result, LispyList([1, 2, 3, 4, 5]))

    def test_concat_with_empty_collections(self):
        """Test concat with empty collections included."""
        result = run_lispy_string("(concat [1 2] [] [3 4])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4]))

        result_list = run_lispy_string("(concat '() '(1 2) '() '(3))", self.env)
        self.assertIsInstance(result_list, LispyList)
        self.assertEqual(result_list, LispyList([1, 2, 3]))

    def test_concat_mixed_data_types(self):
        """Test concat with different data types."""
        result = run_lispy_string(
            '(concat [1 "hello"] [true 3.14] ["world"])', self.env
        )
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, "hello", True, 3.14, "world"]))

    def test_concat_original_collections_unchanged(self):
        """Test that concat does not mutate the original collections."""
        run_lispy_string("(define vec1 [1 2])", self.env)
        run_lispy_string("(define vec2 [3 4])", self.env)
        run_lispy_string("(concat vec1 vec2)", self.env)

        original_vec1 = run_lispy_string("vec1", self.env)
        original_vec2 = run_lispy_string("vec2", self.env)

        self.assertIsInstance(original_vec1, Vector)
        self.assertEqual(original_vec1, Vector([1, 2]))
        self.assertIsInstance(original_vec2, Vector)
        self.assertEqual(original_vec2, Vector([3, 4]))

    # --- Error Handling Tests ---
    def test_concat_invalid_first_argument(self):
        """Test concat with invalid first argument type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(concat "not-a-collection")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'concat' arguments must be lists or vectors, got <class 'str'> as first argument.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(concat 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'concat' arguments must be lists or vectors, got <class 'int'> as first argument.",
        )

    def test_concat_invalid_subsequent_argument(self):
        """Test concat with invalid subsequent argument types."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(concat [1 2] "not-a-collection")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'concat' arguments must be lists or vectors, got <class 'str'> at position 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(concat [1] [2] 123 [4])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'concat' arguments must be lists or vectors, got <class 'int'> at position 2.",
        )

    def test_concat_with_thread_first(self):
        """Test concat used with the -> (thread-first) special form."""
        result = run_lispy_string("(-> [1 2] (concat [3 4] [5]))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

        result_list = run_lispy_string("(-> '(1 2) (concat '(3 4) '(5)))", self.env)
        self.assertIsInstance(result_list, LispyList)
        self.assertEqual(result_list, LispyList([1, 2, 3, 4, 5]))

    def test_concat_chaining_with_thread_first(self):
        """Test chaining concat with other functions via thread-first."""
        result = run_lispy_string("(-> [1 2] (concat [3 4]) (reverse))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([4, 3, 2, 1]))

    def test_concat_large_number_of_collections(self):
        """Test concat with many collections."""
        result = run_lispy_string(
            "(concat [1] [2] [3] [4] [5] [6] [7] [8] [9] [10])", self.env
        )
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


if __name__ == "__main__":
    unittest.main()

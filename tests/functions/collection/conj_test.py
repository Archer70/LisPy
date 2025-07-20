import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyList, Vector
from lispy.utils import run_lispy_string


class ConjFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # List tests
    def test_conj_list_one_item(self):
        """Test (conj '(1 2) 3) returns (3 1 2)."""
        lispy_code = "(conj '(1 2) 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([3, 1, 2]))

    def test_conj_list_multiple_items(self):
        """Test (conj '(1) 2 3) returns (3 2 1)."""
        lispy_code = "(conj '(1) 2 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([3, 2, 1]))

    def test_conj_empty_list_one_item(self):
        """Test (conj '() 1) returns (1)."""
        lispy_code = "(conj '() 1)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([1]))

    def test_conj_empty_list_multiple_items(self):
        """Test (conj '() 1 2 3) returns (3 2 1)."""
        lispy_code = "(conj '() 1 2 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([3, 2, 1]))

    def test_conj_list_original_unchanged(self):
        """Test conj on list does not modify original."""
        run_lispy_string("(define my-list '(1 2))", self.env)
        run_lispy_string("(conj my-list 3)", self.env)
        original_list = run_lispy_string("my-list", self.env)
        self.assertEqual(original_list, LispyList([1, 2]))

    # Vector tests
    def test_conj_vector_one_item(self):
        """Test (conj [1 2] 3) returns [1 2 3]."""
        lispy_code = "(conj [1 2] 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_conj_vector_multiple_items(self):
        """Test (conj [1] 2 3) returns [1 2 3]."""
        lispy_code = "(conj [1] 2 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_conj_empty_vector_one_item(self):
        """Test (conj [] 1) returns [1]."""
        lispy_code = "(conj [] 1)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([1]))

    def test_conj_empty_vector_multiple_items(self):
        """Test (conj [] 1 2 3) returns [1 2 3]."""
        lispy_code = "(conj [] 1 2 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_conj_vector_original_unchanged(self):
        """Test conj on vector does not modify original."""
        run_lispy_string("(define my-vec [1 2])", self.env)
        run_lispy_string("(conj my-vec 3)", self.env)
        original_vector = run_lispy_string("my-vec", self.env)
        self.assertEqual(original_vector, Vector([1, 2]))

    # Nil collection tests
    def test_conj_nil_one_item(self):
        """Test (conj nil 1) results in list (1)"""
        lispy_code = "(conj nil 1)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([1]))

    def test_conj_nil_multiple_items(self):
        """Test (conj nil 1 2 3) results in list (3 2 1)"""
        lispy_code = "(conj nil 1 2 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([3, 2, 1]))

    # Error handling tests
    def test_conj_no_items(self):
        """Test (conj '(1 2)) raises SyntaxError (needs at least one item to add)."""
        lispy_code = "(conj '(1 2))"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'conj' expects at least 2 arguments (collection and item(s)), got 1.",
        )

    def test_conj_no_args(self):
        """Test (conj) raises SyntaxError."""
        lispy_code = "(conj)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'conj' expects at least 2 arguments (collection and item(s)), got 0.",
        )

    def test_conj_wrong_collection_type(self):
        """Test (conj {:a 1} 2) raises TypeError."""
        lispy_code = "(conj {:a 1} 2)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'conj' expects a list, vector, or nil as the first argument, got <class 'dict'>.",
        )

    def test_conj_string_collection(self):
        """Test (conj \"abc\" \"d\") raises TypeError."""
        lispy_code = '(conj "abc" "d")'
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'conj' expects a list, vector, or nil as the first argument, got <class 'str'>.",
        )


if __name__ == "__main__":
    unittest.main()

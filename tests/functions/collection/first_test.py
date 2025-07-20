import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyList
from lispy.utils import run_lispy_string


class FirstFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_first_on_list(self):
        """Test (first '(1 2 3)) returns 1."""
        lispy_code = "(first '(1 2 3))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, 1)

    def test_first_on_vector(self):
        """Test (first [1 2 3]) returns 1."""
        lispy_code = "(first [1 2 3])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, 1)

    def test_first_on_single_element_list(self):
        """Test (first '(1)) returns 1."""
        lispy_code = "(first '(1))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, 1)

    def test_first_on_single_element_vector(self):
        """Test (first [1]) returns 1."""
        lispy_code = "(first [1])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, 1)

    def test_first_on_empty_list(self):
        """Test (first '()) returns nil."""
        lispy_code = "(first '())"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsNone(result)

    def test_first_on_empty_vector(self):
        """Test (first []) returns nil."""
        lispy_code = "(first [])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsNone(result)

    def test_first_on_nil(self):
        """Test (first nil) returns nil."""
        lispy_code = "(first nil)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsNone(result)

    def test_first_complex_elements(self):
        """Test first with list containing various types, including another list."""
        # Lispy code: (first '((1 2) :foo [3 4]))
        # Expected result: LispyList([1, 2])
        lispy_code = "(first '((1 2) :foo [3 4]))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([1, 2]))

    def test_first_on_string(self):
        """Test (first "abc") returns "a"."""
        lispy_code = '(first "abc")'
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, "a")

    def test_first_on_empty_string(self):
        """Test (first "") returns nil."""
        lispy_code = '(first "")'
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsNone(result)

    # Error handling tests
    def test_first_no_args(self):
        """Test (first) raises SyntaxError."""
        lispy_code = "(first)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'first' expects 1 argument, got 0."
        )

    def test_first_too_many_args(self):
        """Test (first '(1) '(2)) raises SyntaxError."""
        lispy_code = "(first '(1) '(2))"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'first' expects 1 argument, got 2."
        )

    def test_first_wrong_type(self):
        """Test (first 123) raises TypeError."""
        lispy_code = "(first 123)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'first' expects a list, vector, string, or nil, got <class 'int'>.",
        )

    def test_first_map_type(self):
        """Test (first {:a 1}) raises TypeError."""
        lispy_code = "(first {:a 1})"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'first' expects a list, vector, string, or nil, got <class 'dict'>.",
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class JoinFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_join_vector_with_space(self):
        """Test (join ["a" "b" "c"] " ") returns "a b c"."""
        result = run_lispy_string('(join ["a" "b" "c"] " ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "a b c")

    def test_join_list_with_comma(self):
        """Test (join '("apple" "banana" "cherry") ", ") returns comma-separated string."""
        result = run_lispy_string('(join \'("apple" "banana" "cherry") ", ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "apple, banana, cherry")

    def test_join_vector_with_empty_separator(self):
        """Test (join ["h" "e" "l" "l" "o"] "") returns "hello"."""
        result = run_lispy_string('(join ["h" "e" "l" "l" "o"] "")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello")

    def test_join_vector_with_dash(self):
        """Test (join ["one" "two" "three"] "-") returns "one-two-three"."""
        result = run_lispy_string('(join ["one" "two" "three"] "-")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "one-two-three")

    def test_join_empty_vector(self):
        """Test (join [] " ") returns ""."""
        result = run_lispy_string('(join [] " ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_join_empty_list(self):
        """Test (join '() ", ") returns ""."""
        result = run_lispy_string('(join \'() ", ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_join_single_element_vector(self):
        """Test (join ["hello"] " ") returns "hello"."""
        result = run_lispy_string('(join ["hello"] " ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello")

    def test_join_single_element_list(self):
        """Test (join '("world") ", ") returns "world"."""
        result = run_lispy_string('(join \'("world") ", ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "world")

    def test_join_vector_with_empty_strings(self):
        """Test join with empty strings in collection."""
        result = run_lispy_string('(join ["a" "" "b" "" "c"] ":")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "a::b::c")

    def test_join_vector_all_empty_strings(self):
        """Test join with all empty strings."""
        result = run_lispy_string('(join ["" "" ""] "|")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "||")

    def test_join_with_complex_separator(self):
        """Test join with multi-character separator."""
        result = run_lispy_string('(join ["start" "middle" "end"] " --> ")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "start --> middle --> end")

    def test_join_with_variables(self):
        """Test join with variables."""
        run_lispy_string('(define words ["hello" "beautiful" "world"])', self.env)
        run_lispy_string('(define sep " ")', self.env)
        result = run_lispy_string("(join words sep)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello beautiful world")

    # --- Error Handling Tests ---
    def test_join_too_few_args(self):
        """Test join with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(join)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'join' expects 2 arguments, got 0."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(join [])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'join' expects 2 arguments, got 1."
        )

    def test_join_too_many_args(self):
        """Test join with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join ["a"] " " "extra")', self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'join' expects 2 arguments, got 3."
        )

    def test_join_invalid_separator_type(self):
        """Test join with non-string separator."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join ["a" "b"] 123)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'join' second argument (separator) must be a string, got <class 'int'>.",
        )

    def test_join_invalid_collection_type(self):
        """Test join with non-collection first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join "not-a-collection" " ")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'join' first argument must be a list or vector, got <class 'str'>.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join 123 " ")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'join' first argument must be a list or vector, got <class 'int'>.",
        )

    def test_join_collection_with_non_string_elements(self):
        """Test join with non-string elements in collection."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join ["a" 123 "c"] " ")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: All elements in collection must be strings, got <class 'int'> at position 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(join [true "b"] " ")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: All elements in collection must be strings, got <class 'bool'> at position 0.",
        )

    def test_join_with_thread_first(self):
        """Test join used with the -> (thread-first) special form."""
        result = run_lispy_string('(-> ["hello" "world"] (join " "))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello world")

    def test_join_chaining_with_thread_first(self):
        """Test chaining join with other operations via thread-first."""
        result = run_lispy_string(
            '(-> ["a" "b" "c"] (join "-") (append "!"))', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, "a-b-c!")

    def test_join_complex_thread_first(self):
        """Test complex join operation with thread-first."""
        result = run_lispy_string(
            '(-> ["1" "2" "3"] (join ", ") (append " are numbers"))', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, "1, 2, 3 are numbers")


if __name__ == "__main__":
    unittest.main()

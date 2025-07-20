import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import Vector
from lispy.utils import run_lispy_string


class SplitFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_split_comma_separated(self):
        """Test (split "a,b,c" ",") returns ["a" "b" "c"]."""
        result = run_lispy_string('(split "a,b,c" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a", "b", "c"]))

    def test_split_space_separated(self):
        """Test (split "hello world" " ") returns ["hello" "world"]."""
        result = run_lispy_string('(split "hello world" " ")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["hello", "world"]))

    def test_split_dash_separated(self):
        """Test (split "one-two-three" "-") returns ["one" "two" "three"]."""
        result = run_lispy_string('(split "one-two-three" "-")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["one", "two", "three"]))

    def test_split_into_characters(self):
        """Test (split "hello" "") returns ["h" "e" "l" "l" "o"]."""
        result = run_lispy_string('(split "hello" "")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["h", "e", "l", "l", "o"]))

    def test_split_empty_string(self):
        """Test (split "" ",") returns [""]."""
        result = run_lispy_string('(split "" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([""]))

    def test_split_empty_string_into_characters(self):
        """Test (split "" "") returns []."""
        result = run_lispy_string('(split "" "")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_split_no_separator_found(self):
        """Test split when separator is not found in string."""
        result = run_lispy_string('(split "hello" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["hello"]))

    def test_split_separator_at_start(self):
        """Test split with separator at the beginning."""
        result = run_lispy_string('(split ",a,b" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["", "a", "b"]))

    def test_split_separator_at_end(self):
        """Test split with separator at the end."""
        result = run_lispy_string('(split "a,b," ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a", "b", ""]))

    def test_split_consecutive_separators(self):
        """Test split with consecutive separators."""
        result = run_lispy_string('(split "a,,b" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a", "", "b"]))

    def test_split_only_separators(self):
        """Test split string that contains only separators."""
        result = run_lispy_string('(split ",,," ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["", "", "", ""]))

    def test_split_multi_character_separator(self):
        """Test split with multi-character separator."""
        result = run_lispy_string('(split "one --> two --> three" " --> ")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["one", "two", "three"]))

    def test_split_single_character_string(self):
        """Test split single character string."""
        result = run_lispy_string('(split "a" ",")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a"]))

        result2 = run_lispy_string('(split "a" "")', self.env)
        self.assertIsInstance(result2, Vector)
        self.assertEqual(result2, Vector(["a"]))

    def test_split_with_variables(self):
        """Test split with variables."""
        run_lispy_string('(define text "apple,banana,cherry")', self.env)
        run_lispy_string('(define sep ",")', self.env)
        result = run_lispy_string("(split text sep)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["apple", "banana", "cherry"]))

    def test_split_whitespace_variations(self):
        """Test split with different whitespace characters."""
        result = run_lispy_string('(split "a\\tb\\tc" "\\t")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a", "b", "c"]))

    # --- Error Handling Tests ---
    def test_split_too_few_args(self):
        """Test split with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(split)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'split' expects 2 arguments, got 0."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split "hello")', self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'split' expects 2 arguments, got 1."
        )

    def test_split_too_many_args(self):
        """Test split with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split "hello" " " "extra")', self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'split' expects 2 arguments, got 3."
        )

    def test_split_invalid_string_type(self):
        """Test split with non-string first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split 123 ",")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'split' first argument must be a string, got <class 'int'>.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split ["a" "b"] ",")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'split' first argument must be a string, got <class 'lispy.types.Vector'>.",
        )

    def test_split_invalid_separator_type(self):
        """Test split with non-string separator."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split "hello" 123)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'split' second argument (separator) must be a string, got <class 'int'>.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(split "hello" true)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'split' second argument (separator) must be a string, got <class 'bool'>.",
        )

    def test_split_with_thread_first(self):
        """Test split used with the -> (thread-first) special form."""
        result = run_lispy_string('(-> "a,b,c" (split ","))', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["a", "b", "c"]))

    def test_split_chaining_with_thread_first(self):
        """Test chaining split with other operations via thread-first."""
        result = run_lispy_string('(-> "hello world" (split " ") (join "-"))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello-world")

    def test_split_complex_thread_first(self):
        """Test complex split operation with thread-first."""
        result = run_lispy_string('(-> "a,b,c" (split ",") (join " | "))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "a | b | c")

    def test_split_join_roundtrip(self):
        """Test that split and join are inverse operations."""
        original = "apple,banana,cherry"
        result = run_lispy_string(
            '(-> "apple,banana,cherry" (split ",") (join ","))', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, original)


if __name__ == "__main__":
    unittest.main()

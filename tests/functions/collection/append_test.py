import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class AppendFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_append_empty_args(self):
        """Test (append) returns ""."""
        result = run_lispy_string("(append)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_append_single_string(self):
        """Test (append "hello") returns "hello"."""
        result = run_lispy_string('(append "hello")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello")

    def test_append_two_strings(self):
        """Test (append "hello" "world") returns "helloworld"."""
        result = run_lispy_string('(append "hello" "world")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "helloworld")

    def test_append_multiple_strings(self):
        """Test (append "a" "b" "c" "d") returns "abcd"."""
        result = run_lispy_string('(append "a" "b" "c" "d")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "abcd")

    def test_append_with_spaces(self):
        """Test appending strings with spaces and punctuation."""
        result = run_lispy_string('(append "Hello" " " "World" "!")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello World!")

    def test_append_empty_strings(self):
        """Test append with empty strings included."""
        result = run_lispy_string('(append "start" "" "middle" "" "end")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "startmiddleend")

    def test_append_only_empty_strings(self):
        """Test append with only empty strings."""
        result = run_lispy_string('(append "" "" "")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_append_special_characters(self):
        """Test append with special characters and unicode."""
        result = run_lispy_string('(append "Hello" " 🌍 " "World")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello 🌍 World")

    def test_append_numbers_as_strings(self):
        """Test append with numeric strings."""
        result = run_lispy_string('(append "123" "456" "789")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "123456789")

    def test_append_long_strings(self):
        """Test append with longer strings."""
        result = run_lispy_string(
            '(append "The quick brown fox " "jumps over " "the lazy dog")', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, "The quick brown fox jumps over the lazy dog")

    def test_append_with_variables(self):
        """Test append with string variables."""
        run_lispy_string('(define greeting "Hello")', self.env)
        run_lispy_string('(define name "Alice")', self.env)
        result = run_lispy_string('(append greeting " " name "!")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello Alice!")

    def test_append_many_strings(self):
        """Test append with many string arguments."""
        lispy_code = '(append "a" "b" "c" "d" "e" "f" "g" "h" "i" "j")'
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "abcdefghij")

    # --- Error Handling Tests ---
    def test_append_invalid_argument_type(self):
        """Test append with non-string arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(append 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'append' arguments must be strings, got <class 'int'> at position 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(append [1 2 3])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'append' arguments must be strings, got <class 'lispy.types.Vector'> at position 0.",
        )

    def test_append_mixed_valid_invalid_args(self):
        """Test append with mix of valid and invalid arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(append "hello" 123 "world")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'append' arguments must be strings, got <class 'int'> at position 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(append "a" "b" true "d")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'append' arguments must be strings, got <class 'bool'> at position 2.",
        )

    def test_append_with_thread_first(self):
        """Test append used with the -> (thread-first) special form."""
        result = run_lispy_string('(-> "Hello" (append " " "World"))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello World")

    def test_append_chaining_with_thread_first(self):
        """Test chaining multiple append operations via thread-first."""
        result = run_lispy_string(
            '(-> "Start" (append " middle") (append " end"))', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Start middle end")

    def test_append_complex_thread_first(self):
        """Test complex append operation with thread-first."""
        result = run_lispy_string(
            '(-> "Hello" (append " beautiful") (append " " "World" "!"))', self.env
        )
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello beautiful World!")

    def test_append_immutability(self):
        """Test that append does not modify the original string variables."""
        run_lispy_string('(define str1 "Hello")', self.env)
        run_lispy_string('(define str2 " World")', self.env)
        run_lispy_string("(append str1 str2)", self.env)

        # Check that original strings are unchanged (though strings are immutable in Python anyway)
        original_str1 = run_lispy_string("str1", self.env)
        original_str2 = run_lispy_string("str2", self.env)

        self.assertEqual(original_str1, "Hello")
        self.assertEqual(original_str2, " World")


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class ReadLineFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    @patch("builtins.input", return_value="Hello World")
    def test_read_line_no_prompt(self, mock_input):
        result = run_lispy_string("(read-line)", self.env)
        self.assertEqual(result, "Hello World")
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="Alice")
    def test_read_line_with_prompt(self, mock_input):
        result = run_lispy_string('(read-line "Enter name: ")', self.env)
        self.assertEqual(result, "Alice")
        mock_input.assert_called_once_with("Enter name: ")

    @patch("builtins.input", return_value="42")
    def test_read_line_returns_string(self, mock_input):
        result = run_lispy_string("(read-line)", self.env)
        self.assertEqual(result, "42")
        self.assertIsInstance(result, str)

    @patch("builtins.input", return_value="")
    def test_read_line_empty_input(self, mock_input):
        result = run_lispy_string("(read-line)", self.env)
        self.assertEqual(result, "")

    @patch("builtins.input", side_effect=EOFError())
    def test_read_line_eof_handling(self, mock_input):
        result = run_lispy_string("(read-line)", self.env)
        self.assertEqual(result, "")

    @patch("builtins.input", side_effect=KeyboardInterrupt())
    def test_read_line_keyboard_interrupt(self, mock_input):
        with self.assertRaises(KeyboardInterrupt):
            run_lispy_string("(read-line)", self.env)

    def test_read_line_too_many_arguments(self):
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(read-line "prompt1" "prompt2")', self.env)
        self.assertIn(
            "SyntaxError: 'read-line' expects 0 or 1 arguments (optional prompt), got 2.",
            str(cm.exception),
        )

    def test_read_line_non_string_prompt(self):
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(read-line 42)", self.env)
        self.assertIn(
            "TypeError: 'read-line' prompt must be a string, got int.",
            str(cm.exception),
        )

    def test_read_line_boolean_prompt(self):
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(read-line true)", self.env)
        self.assertIn(
            "TypeError: 'read-line' prompt must be a string, got bool.",
            str(cm.exception),
        )

    @patch("builtins.input", return_value="test input")
    def test_read_line_integration_with_variable(self, mock_input):
        # Test using read-line with variable assignment
        result = run_lispy_string('(let [name (read-line "Name: ")] name)', self.env)
        self.assertEqual(result, "test input")
        mock_input.assert_called_once_with("Name: ")


if __name__ == "__main__":
    unittest.main()

import os
import tempfile
import unittest
from unittest.mock import patch

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class SlurpFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_file(self, filename, content):
        """Helper method to create test files"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def _escape_path(self, filepath):
        """Helper method to escape Windows paths for LisPy strings"""
        return filepath.replace("\\", "\\\\")

    def test_slurp_simple_file(self):
        # Create a test file
        content = "Hello, World!"
        filepath = self._create_test_file("test.txt", content)
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(f'(slurp "{escaped_filepath}")', self.env)
        self.assertEqual(result, content)

    def test_slurp_multiline_file(self):
        # Test file with multiple lines
        content = "Line 1\nLine 2\nLine 3"
        filepath = self._create_test_file("multiline.txt", content)
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(f'(slurp "{escaped_filepath}")', self.env)
        self.assertEqual(result, content)

    def test_slurp_empty_file(self):
        # Test empty file
        filepath = self._create_test_file("empty.txt", "")
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(f'(slurp "{escaped_filepath}")', self.env)
        self.assertEqual(result, "")

    def test_slurp_file_with_special_chars(self):
        # Test file with special characters and unicode
        content = "Special chars: !@#$%^&*()\nUnicode: café, naïve, résumé"
        filepath = self._create_test_file("special.txt", content)
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(f'(slurp "{escaped_filepath}")', self.env)
        self.assertEqual(result, content)

    def test_slurp_file_not_found(self):
        # Test non-existent file
        fake_path = os.path.join(self.temp_dir, "nonexistent.txt")
        escaped_fake_path = self._escape_path(fake_path)

        with self.assertRaises(Exception) as cm:
            run_lispy_string(f'(slurp "{escaped_fake_path}")', self.env)
        self.assertIn("FileNotFoundError: File", str(cm.exception))
        self.assertIn("does not exist", str(cm.exception))

    def test_slurp_directory_instead_of_file(self):
        # Test trying to slurp a directory
        escaped_temp_dir = self._escape_path(self.temp_dir)
        with self.assertRaises(Exception) as cm:
            run_lispy_string(f'(slurp "{escaped_temp_dir}")', self.env)
        self.assertIn("FileError:", str(cm.exception))
        self.assertIn("is not a regular file", str(cm.exception))

    def test_slurp_no_arguments(self):
        # Test with no arguments
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(slurp)", self.env)
        self.assertIn(
            "SyntaxError: 'slurp' expects 1 argument (filename), got 0.",
            str(cm.exception),
        )

    def test_slurp_too_many_arguments(self):
        # Test with too many arguments
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(slurp "file1.txt" "file2.txt")', self.env)
        self.assertIn(
            "SyntaxError: 'slurp' expects 1 argument (filename), got 2.",
            str(cm.exception),
        )

    def test_slurp_non_string_argument(self):
        # Test with non-string argument
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(slurp 42)", self.env)
        self.assertIn(
            "TypeError: 'slurp' filename must be a string, got int.", str(cm.exception)
        )

    def test_slurp_boolean_argument(self):
        # Test with boolean argument
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(slurp true)", self.env)
        self.assertIn(
            "TypeError: 'slurp' filename must be a string, got bool.", str(cm.exception)
        )

    def test_slurp_integration_with_count(self):
        # Test using slurp with count function
        content = "Hello"
        filepath = self._create_test_file("count_test.txt", content)
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(f'(count (slurp "{escaped_filepath}"))', self.env)
        self.assertEqual(result, len(content))

    def test_slurp_integration_with_split(self):
        # Test using slurp with split function to get lines
        content = "line1\nline2\nline3"
        filepath = self._create_test_file("split_test.txt", content)
        escaped_filepath = self._escape_path(filepath)

        result = run_lispy_string(
            f'(split (slurp "{escaped_filepath}") "\\n")', self.env
        )
        expected = ["line1", "line2", "line3"]
        # Convert Vector to list for comparison
        self.assertEqual(list(result), expected)

    def test_slurp_permission_error(self):
        # Test permission denied error using a simpler approach
        # Create a file that we know exists
        content = "test content"
        filepath = self._create_test_file("permission_test.txt", content)
        escaped_filepath = self._escape_path(filepath)

        # Mock the open function to raise PermissionError
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with self.assertRaises(Exception) as cm:
                run_lispy_string(f'(slurp "{escaped_filepath}")', self.env)
            self.assertIn(
                "PermissionError: Permission denied reading file", str(cm.exception)
            )


if __name__ == "__main__":
    unittest.main()

import unittest
import tempfile
import os
from unittest.mock import patch

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class SpitFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _escape_path(self, filepath):
        """Helper method to escape Windows paths for LisPy strings"""
        return filepath.replace("\\", "\\\\")

    def _get_test_filepath(self, filename):
        """Helper method to get escaped test file path"""
        filepath = os.path.join(self.temp_dir, filename)
        return self._escape_path(filepath)

    def test_spit_simple_content(self):
        # Test writing simple content to a file
        filepath = self._get_test_filepath("test.txt")
        content = "Hello, World!"

        result = run_lispy_string(f'(spit "{filepath}" "{content}")', self.env)
        self.assertIsNone(result)  # spit should return nil

        # Verify file was created and has correct content
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, content)

    def test_spit_multiline_content(self):
        # Test writing multiline content
        filepath = self._get_test_filepath("multiline.txt")
        content = "Line 1\\nLine 2\\nLine 3"

        result = run_lispy_string(f'(spit "{filepath}" "{content}")', self.env)
        self.assertIsNone(result)

        # Verify file content (LisPy should interpret \\n as actual newlines)
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, "Line 1\nLine 2\nLine 3")

    def test_spit_empty_content(self):
        # Test writing empty content
        filepath = self._get_test_filepath("empty.txt")

        result = run_lispy_string(f'(spit "{filepath}" "")', self.env)
        self.assertIsNone(result)

        # Verify empty file was created
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, "")

    def test_spit_overwrite_existing_file(self):
        # Test overwriting an existing file
        filepath = self._get_test_filepath("overwrite.txt")
        unescaped_path = filepath.replace("\\\\", "\\")

        # Create initial file
        with open(unescaped_path, "w", encoding="utf-8") as f:
            f.write("Original content")

        # Overwrite with spit
        new_content = "New content"
        result = run_lispy_string(f'(spit "{filepath}" "{new_content}")', self.env)
        self.assertIsNone(result)

        # Verify file was overwritten
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, new_content)

    def test_spit_create_directory(self):
        # Test creating directories if they don't exist
        subdirpath = os.path.join(self.temp_dir, "newdir", "subdir")
        filepath = os.path.join(subdirpath, "test.txt")
        escaped_filepath = self._escape_path(filepath)
        content = "Directory created!"

        result = run_lispy_string(f'(spit "{escaped_filepath}" "{content}")', self.env)
        self.assertIsNone(result)

        # Verify directory and file were created
        self.assertTrue(os.path.exists(subdirpath))
        self.assertTrue(os.path.isfile(filepath))

        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, content)

    def test_spit_special_characters(self):
        # Test writing special characters and unicode
        filepath = self._get_test_filepath("special.txt")
        content = "Special chars: !@#$%^&*()\\nUnicode: café, naïve, résumé"

        result = run_lispy_string(f'(spit "{filepath}" "{content}")', self.env)
        self.assertIsNone(result)

        # Verify content
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        expected = "Special chars: !@#$%^&*()\nUnicode: café, naïve, résumé"
        self.assertEqual(file_content, expected)

    def test_spit_no_arguments(self):
        # Test with no arguments
        with self.assertRaises(Exception) as cm:
            run_lispy_string("(spit)", self.env)
        self.assertIn(
            "SyntaxError: 'spit' expects 2 arguments (filename, content), got 0.",
            str(cm.exception),
        )

    def test_spit_one_argument(self):
        # Test with only one argument
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit "filename.txt")', self.env)
        self.assertIn(
            "SyntaxError: 'spit' expects 2 arguments (filename, content), got 1.",
            str(cm.exception),
        )

    def test_spit_too_many_arguments(self):
        # Test with too many arguments
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit "file1.txt" "content" "extra")', self.env)
        self.assertIn(
            "SyntaxError: 'spit' expects 2 arguments (filename, content), got 3.",
            str(cm.exception),
        )

    def test_spit_non_string_filename(self):
        # Test with non-string filename
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit 42 "content")', self.env)
        self.assertIn(
            "TypeError: 'spit' filename must be a string, got int.", str(cm.exception)
        )

    def test_spit_non_string_content(self):
        # Test with non-string content
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit "filename.txt" 42)', self.env)
        self.assertIn(
            "TypeError: 'spit' content must be a string, got int.", str(cm.exception)
        )

    def test_spit_boolean_arguments(self):
        # Test with boolean arguments
        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit true "content")', self.env)
        self.assertIn(
            "TypeError: 'spit' filename must be a string, got bool.", str(cm.exception)
        )

        with self.assertRaises(Exception) as cm:
            run_lispy_string('(spit "filename.txt" false)', self.env)
        self.assertIn(
            "TypeError: 'spit' content must be a string, got bool.", str(cm.exception)
        )

    def test_spit_integration_with_str(self):
        # Test using spit with str function
        filepath = self._get_test_filepath("str_test.txt")

        result = run_lispy_string(f'(spit "{filepath}" (str 42))', self.env)
        self.assertIsNone(result)

        # Verify content
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, "42")

    def test_spit_integration_with_join(self):
        # Test using spit with join function
        filepath = self._get_test_filepath("join_test.txt")

        result = run_lispy_string(
            f'(spit "{filepath}" (join ["line1" "line2" "line3"] "\\n"))', self.env
        )
        self.assertIsNone(result)

        # Verify content
        unescaped_path = filepath.replace("\\\\", "\\")
        with open(unescaped_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, "line1\nline2\nline3")

    def test_spit_slurp_roundtrip(self):
        # Test spit followed by slurp (round-trip)
        filepath = self._get_test_filepath("roundtrip.txt")
        content = "Round-trip test content!"

        # Write with spit
        result = run_lispy_string(f'(spit "{filepath}" "{content}")', self.env)
        self.assertIsNone(result)

        # Read back with slurp
        read_result = run_lispy_string(f'(slurp "{filepath}")', self.env)
        self.assertEqual(read_result, content)

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_spit_permission_error(self, mock_open):
        # Test permission denied error
        filepath = self._get_test_filepath("permission_test.txt")

        with self.assertRaises(Exception) as cm:
            run_lispy_string(f'(spit "{filepath}" "content")', self.env)
        self.assertIn(
            "PermissionError: Permission denied writing to file", str(cm.exception)
        )

    def test_spit_directory_as_filename(self):
        # Test trying to write to a directory instead of a file
        escaped_temp_dir = self._escape_path(self.temp_dir)

        with self.assertRaises(Exception) as cm:
            run_lispy_string(f'(spit "{escaped_temp_dir}" "content")', self.env)
        # On Windows, this might be PermissionError instead of IsADirectoryError
        error_msg = str(cm.exception)
        self.assertTrue(
            "IsADirectoryError:" in error_msg or "PermissionError:" in error_msg,
            f"Expected IsADirectoryError or PermissionError, got: {error_msg}",
        )


if __name__ == "__main__":
    unittest.main()

import unittest
import os
import tempfile
import shutil
from lispy.module_system import Module, get_module_loader
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string
from lispy.functions import create_global_env


class ModuleSystemTest(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temporary directory for test modules."""
        self.test_dir = tempfile.mkdtemp()
        self.loader = get_module_loader()  # Use global loader
        self.loader.add_load_path(self.test_dir)
        self.env = create_global_env()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
        # Clear module cache to avoid interference between tests
        self.loader.cache.clear()
        self.loader.loading.clear()
        # Remove test directory from load paths
        if self.test_dir in self.loader.load_paths:
            self.loader.load_paths.remove(self.test_dir)

    def create_test_module(self, name, content):
        """Helper to create a test module file."""
        module_path = os.path.join(self.test_dir, f"{name}.lpy")
        os.makedirs(os.path.dirname(module_path), exist_ok=True)
        with open(module_path, "w") as f:
            f.write(content)
        return module_path

    def test_module_creation(self):
        """Test basic module creation."""
        module = Module("test", "/path/to/test.lpy")
        self.assertEqual(module.name, "test")
        self.assertEqual(module.file_path, "/path/to/test.lpy")
        self.assertFalse(module.loaded)
        self.assertEqual(len(module.exports), 0)

    def test_module_exports(self):
        """Test module export functionality."""
        module = Module("test", "/path/to/test.lpy")

        # Add exports
        module.add_export("func1")
        module.add_export("var1")

        self.assertIn("func1", module.exports)
        self.assertIn("var1", module.exports)
        self.assertEqual(len(module.exports), 2)

    def test_module_loader_find_file(self):
        """Test module file discovery."""
        # Create a test module
        self.create_test_module("simple", "(define x 42)")

        # Test finding the module
        found_path = self.loader.find_module_file("simple")
        self.assertIsNotNone(found_path)
        self.assertTrue(found_path.endswith("simple.lpy"))

        # Test non-existent module
        not_found = self.loader.find_module_file("nonexistent")
        self.assertIsNone(not_found)

    def test_module_loader_nested_paths(self):
        """Test module loading with nested directory paths."""
        # Create nested module
        self.create_test_module("math/utils", "(define pi 3.14159)")

        found_path = self.loader.find_module_file("math/utils")
        self.assertIsNotNone(found_path)
        self.assertTrue(found_path.endswith(os.path.join("math", "utils.lpy")))

    def test_simple_module_loading(self):
        """Test loading a simple module."""
        # Create a simple module
        content = """
        (define x 42)
        (define double (fn [n] (* n 2)))
        (export x double)
        """
        self.create_test_module("simple", content)

        # Load the module
        module = self.loader.load_module("simple", evaluate)

        self.assertTrue(module.loaded)
        self.assertEqual(module.name, "simple")
        self.assertIn("x", module.exports)
        self.assertIn("double", module.exports)

        # Check that symbols are defined in module environment
        self.assertEqual(module.env.lookup("x"), 42)

    def test_module_caching(self):
        """Test that modules are cached and not loaded multiple times."""
        content = "(define counter 0) (define counter (+ counter 1)) (export counter)"
        self.create_test_module("cached", content)

        # Load module twice
        module1 = self.loader.load_module("cached", evaluate)
        module2 = self.loader.load_module("cached", evaluate)

        # Should be the same instance
        self.assertIs(module1, module2)

    def test_circular_dependency_detection(self):
        """Test detection of circular dependencies."""
        # Create modules with circular dependency
        self.create_test_module("a", '(import "b") (define a-val 1) (export a-val)')
        self.create_test_module("b", '(import "a") (define b-val 2) (export b-val)')

        # Should raise error on circular dependency
        with self.assertRaisesRegex(EvaluationError, "Circular dependency detected"):
            self.loader.load_module("a", evaluate)

    def test_module_not_found_error(self):
        """Test error when module file is not found."""
        with self.assertRaisesRegex(EvaluationError, "Module 'nonexistent' not found"):
            self.loader.load_module("nonexistent", evaluate)


class ExportFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_export_basic_functionality(self):
        """Test basic export functionality within a module context."""
        # This test would need to be run within a module context
        # For now, we'll test the error case when not in a module
        with self.assertRaisesRegex(
            EvaluationError, "'export' can only be used within a module"
        ):
            run_lispy_string("(export x y)", self.env)

    def test_export_requires_symbols(self):
        """Test that export requires at least one symbol."""
        with self.assertRaisesRegex(
            EvaluationError, "'export' requires at least one symbol"
        ):
            run_lispy_string("(export)", self.env)


class ImportFormTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.env = create_global_env()
        # Add test directory to module load path
        loader = get_module_loader()
        loader.add_load_path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_test_module(self, name, content):
        """Helper to create a test module file."""
        module_path = os.path.join(self.test_dir, f"{name}.lpy")
        os.makedirs(os.path.dirname(module_path), exist_ok=True)
        with open(module_path, "w") as f:
            f.write(content)
        return module_path

    def test_import_requires_module_name(self):
        """Test that import requires a module name."""
        with self.assertRaisesRegex(EvaluationError, "'import' requires a module name"):
            run_lispy_string("(import)", self.env)

    def test_import_module_name_must_be_string(self):
        """Test that import module name must be a string."""
        with self.assertRaisesRegex(EvaluationError, "module name must be a string"):
            run_lispy_string("(import some-symbol)", self.env)


if __name__ == "__main__":
    unittest.main()

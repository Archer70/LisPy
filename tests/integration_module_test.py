import os
import shutil
import tempfile
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.module_system import get_module_loader
from lispy.utils import run_lispy_string


class ModuleIntegrationTest(unittest.TestCase):
    """Integration tests for the complete module system workflow."""

    def setUp(self):
        """Set up test environment with temporary directory for test modules."""
        self.test_dir = tempfile.mkdtemp()
        self.loader = get_module_loader()
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

    def test_basic_import_export_workflow(self):
        """Test basic module creation, export, and import."""
        # Create a math utilities module
        math_content = """
        (define pi 3.14159)
        (define square (fn [x] (* x x)))
        (define circle-area (fn [r] (* pi (* r r))))
        (export pi square circle-area)
        """
        self.create_test_module("math-utils", math_content)

        # Import and use the module
        run_lispy_string('(import "math-utils")', self.env)

        # Test that exported symbols are available
        result = run_lispy_string("pi", self.env)
        self.assertAlmostEqual(result, 3.14159)

        result = run_lispy_string("(square 5)", self.env)
        self.assertEqual(result, 25)

        result = run_lispy_string("(circle-area 2)", self.env)
        self.assertAlmostEqual(result, 12.56636, places=5)

    def test_selective_import(self):
        """Test importing only specific symbols from a module."""
        # Create a module with multiple exports
        utils_content = """
        (define add (fn [x y] (+ x y)))
        (define multiply (fn [x y] (* x y)))
        (define subtract (fn [x y] (- x y)))
        (define divide (fn [x y] (/ x y)))
        (export add multiply subtract divide)
        """
        self.create_test_module("utils", utils_content)

        # Import only specific functions
        run_lispy_string('(import "utils" :only (add multiply))', self.env)

        # Test that imported symbols work
        result = run_lispy_string("(add 3 4)", self.env)
        self.assertEqual(result, 7)

        result = run_lispy_string("(multiply 3 4)", self.env)
        self.assertEqual(result, 12)

        # Test that non-imported symbols are not available
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: subtract"):
            run_lispy_string("(subtract 10 3)", self.env)

    def test_prefixed_import(self):
        """Test importing with a prefix."""
        # Create a string utilities module
        string_content = """
        (define length (fn [s] (count s)))
        (define upper (fn [s] s))  ; Simplified - would need real string functions
        (define concat (fn [s1 s2] s1))  ; Simplified
        (export length upper concat)
        """
        self.create_test_module("string-utils", string_content)

        # Import with prefix
        run_lispy_string('(import "string-utils" :as "str")', self.env)

        # Test that prefixed symbols work
        result = run_lispy_string('(str/length "hello")', self.env)
        self.assertEqual(result, 5)

        # Test that unprefixed symbols are not available
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: length"):
            run_lispy_string('(length "hello")', self.env)

    def test_module_with_no_exports(self):
        """Test importing from a module with no exports."""
        # Create a module with definitions but no exports
        private_content = """
        (define secret-value 42)
        (define secret-function (fn [x] (* x 2)))
        ; No export statement - nothing should be exported
        """
        self.create_test_module("private", private_content)

        # Import the module (should succeed but import nothing)
        run_lispy_string('(import "private")', self.env)

        # Test that symbols are not available
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: secret-value"):
            run_lispy_string("secret-value", self.env)

    def test_nested_module_imports(self):
        """Test modules that import other modules."""
        # Create a base module
        base_content = """
        (define base-value 10)
        (define base-function (fn [x] (+ x base-value)))
        (export base-value base-function)
        """
        self.create_test_module("base", base_content)

        # Create a module that imports from base
        derived_content = """
        (import "base")
        (define derived-value (* base-value 2))
        (define derived-function (fn [x] (base-function (* x 2))))
        (export derived-value derived-function)
        """
        self.create_test_module("derived", derived_content)

        # Import the derived module
        run_lispy_string('(import "derived")', self.env)

        # Test that derived functionality works
        result = run_lispy_string("derived-value", self.env)
        self.assertEqual(result, 20)

        result = run_lispy_string("(derived-function 5)", self.env)
        self.assertEqual(result, 20)  # (5 * 2) + 10 = 20

    def test_module_with_complex_data_structures(self):
        """Test modules that export complex data structures."""
        data_content = """
        (define config {:host "localhost" :port 8080 :debug true})
        (define users ["alice" "bob" "charlie"])
        (define get-config (fn [key] (get config key)))
        (export config users get-config)
        """
        self.create_test_module("data", data_content)

        # Import and use the module
        run_lispy_string('(import "data")', self.env)

        # Test complex data structure access
        result = run_lispy_string("(get-config ':host)", self.env)
        self.assertEqual(result, "localhost")

        result = run_lispy_string("(count users)", self.env)
        self.assertEqual(result, 3)

        result = run_lispy_string("(first users)", self.env)
        self.assertEqual(result, "alice")

    def test_error_importing_nonexistent_symbol(self):
        """Test error when trying to selectively import a non-exported symbol."""
        simple_content = """
        (define visible 42)
        (define hidden 24)
        (export visible)
        """
        self.create_test_module("simple", simple_content)

        # Try to import a non-exported symbol
        with self.assertRaisesRegex(EvaluationError, "Symbol 'hidden' is not exported"):
            run_lispy_string('(import "simple" :only (visible hidden))', self.env)


if __name__ == "__main__":
    unittest.main()

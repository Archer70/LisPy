import unittest
from lispy.functions import (
    create_global_env, 
    create_web_safe_env,
    get_web_unsafe_functions,
    get_web_unsafe_special_forms,
    get_web_unsafe_bdd_forms
)
from lispy.special_forms import web_safe_special_form_handlers, special_form_handlers, get_web_unsafe_special_forms
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class WebSafeEnvironmentTest(unittest.TestCase):
    """Test the web-safe environment functionality."""

    def setUp(self):
        """Set up test environments."""
        self.regular_env = create_global_env()
        self.web_safe_env = create_web_safe_env()

    def test_web_safe_env_excludes_dangerous_functions(self):
        """Test that web-safe environment excludes dangerous functions."""
        unsafe_functions = get_web_unsafe_functions()
        
        for func_name in unsafe_functions.keys():
            # Function should exist in regular environment
            try:
                self.regular_env.lookup(func_name)
            except EvaluationError:
                self.fail(f"Function '{func_name}' should exist in regular environment")
            
            # Function should NOT exist in web-safe environment
            with self.assertRaises(EvaluationError, msg=f"Function '{func_name}' should not exist in web-safe environment"):
                self.web_safe_env.lookup(func_name)

    def test_web_safe_env_includes_safe_functions(self):
        """Test that web-safe environment includes safe functions."""
        safe_functions = [
            # Math functions
            "+", "-", "*", "/", "%", "abs", "max", "min",
            # Comparison functions  
            "=", "<", ">", "<=", ">=", "equal?",
            # Collection functions
            "map", "filter", "reduce", "conj", "first", "rest", "count",
            "append", "concat", "nth", "reverse", "sort", "some", "every?", "empty?",
            # List functions
            "list", "vector", "car", "cdr", "cons",
            # Map functions
            "hash-map", "get", "assoc", "dissoc", "keys", "vals", "merge",
            # Type checking functions
            "is-number?", "is-string?", "is-boolean?", "is-list?", "is-vector?", "is-map?", "is-nil?", "is-function?",
            # String functions
            "join", "split", "str", "to-str", "to-int", "to-float", "to-bool",
            # Logical functions
            "not",
            # I/O functions (safe ones)
            "print", "println",
            # Promise functions
            "promise", "resolve", "reject", "promise-all", "promise-race", "timeout",
            # Documentation
            "doc", "print-doc"
        ]
        
        for func_name in safe_functions:
            try:
                self.web_safe_env.lookup(func_name)
            except EvaluationError:
                self.fail(f"Safe function '{func_name}' should exist in web-safe environment")

    def test_file_io_functions_excluded(self):
        """Test that file I/O functions are excluded from web-safe environment."""
        # These should work in regular environment
        self.regular_env.lookup("slurp")
        self.regular_env.lookup("spit")
        self.regular_env.lookup("read-line")
        
        # These should NOT work in web-safe environment
        with self.assertRaises(EvaluationError):
            self.web_safe_env.lookup("slurp")
            
        with self.assertRaises(EvaluationError):
            self.web_safe_env.lookup("spit")
            
        with self.assertRaises(EvaluationError):
            self.web_safe_env.lookup("read-line")

    def test_safe_operations_work_in_web_safe_env(self):
        """Test that safe operations work correctly in web-safe environment."""
        # Math operations
        result = run_lispy_string("(+ 1 2 3)", self.web_safe_env)
        self.assertEqual(result, 6)
        
        # Collection operations
        result = run_lispy_string("(map [1 2 3] (fn [x] (* x 2)))", self.web_safe_env)
        self.assertEqual(result, [2, 4, 6])
        
        # String operations
        result = run_lispy_string('(join ["a" "b" "c"] ", ")', self.web_safe_env)
        self.assertEqual(result, "a, b, c")
        
        # Map operations
        result = run_lispy_string("(get {:a 1 :b 2} ':a)", self.web_safe_env)
        self.assertEqual(result, 1)

    def test_unsafe_function_names_list(self):
        """Test that the list of unsafe functions is correct."""
        unsafe_functions = get_web_unsafe_functions()
        
        expected_unsafe = {'slurp', 'spit', 'read-line', 'http-delete', 'http-get', 'http-post', 'http-put', 'http-request'}
        actual_unsafe = set(unsafe_functions.keys())
        
        self.assertEqual(actual_unsafe, expected_unsafe)
        
        # Verify reasons are provided
        for func_name, reason in unsafe_functions.items():
            self.assertIsInstance(reason, str)
            self.assertTrue(len(reason) > 0)

    def test_web_safe_special_forms(self):
        """Test that web-safe special forms registry excludes dangerous forms."""
        # Import and export should not be in web-safe handlers
        self.assertIn("import", special_form_handlers)
        self.assertIn("export", special_form_handlers)
        self.assertIn("throw", special_form_handlers)
        
        self.assertNotIn("import", web_safe_special_form_handlers)
        self.assertNotIn("export", web_safe_special_form_handlers)
        self.assertNotIn("throw", web_safe_special_form_handlers)
        
        # Safe forms should be in both
        safe_forms = ["if", "let", "fn", "define", "cond", "and", "or", "when"]
        for form in safe_forms:
            self.assertIn(form, special_form_handlers)
            self.assertIn(form, web_safe_special_form_handlers)

    def test_get_web_unsafe_special_forms(self):
        """Test the function that returns unsafe special forms."""
        unsafe_forms = get_web_unsafe_special_forms()
        
        expected_unsafe = {'import', 'export', 'throw', 'describe', 'it', 'given', 'then', 'action', 'assert-raises?'}
        
        self.assertEqual(unsafe_forms, expected_unsafe)

    def test_safe_special_forms_work(self):
        """Test that safe special forms work in web-safe environment."""
        # Define and use a function
        run_lispy_string("(define square (fn [x] (* x x)))", self.web_safe_env)
        result = run_lispy_string("(square 5)", self.web_safe_env)
        self.assertEqual(result, 25)
        
        # Let binding
        result = run_lispy_string("(let [x 10 y 20] (+ x y))", self.web_safe_env)
        self.assertEqual(result, 30)
        
        # Conditional
        result = run_lispy_string('(if (> 5 3) "yes" "no")', self.web_safe_env)
        self.assertEqual(result, "yes")

    def test_math_and_logic_comprehensive(self):
        """Test comprehensive math and logic operations in web-safe environment."""
        test_cases = [
            ("(+ 1 2 3 4)", 10),
            ("(- 10 3 2)", 5),
            ("(* 2 3 4)", 24),
            ("(/ 20 2 2)", 5.0),
            ("(% 17 5)", 2),
            ("(abs -5)", 5),
            ("(max 1 5 3)", 5),
            ("(min 1 5 3)", 1),
            ("(= 5 5)", True),
            ("(< 3 5)", True),
            ("(> 3 5)", False),
            ("(<= 3 3)", True),
            ("(>= 5 3)", True),
            ("(not true)", False),
            ("(not false)", True),
        ]
        
        for lispy_code, expected in test_cases:
            result = run_lispy_string(lispy_code, self.web_safe_env)
            self.assertEqual(result, expected, f"Failed for: {lispy_code}")

    def test_collection_operations_comprehensive(self):
        """Test comprehensive collection operations in web-safe environment."""
        test_cases = [
            ("(count [1 2 3])", 3),
            ("(first [1 2 3])", 1),
            ("(rest [1 2 3])", [2, 3]),
            ("(conj [1 2] 3)", [1, 2, 3]),
            ("(concat [1 2] [3 4])", [1, 2, 3, 4]),
            ("(concat [1 2] [3 4] [5])", [1, 2, 3, 4, 5]),
            ("(nth [10 20 30] 1)", 20),
            ("(reverse [1 2 3])", [3, 2, 1]),
            ("(sort [3 1 4 2])", [1, 2, 3, 4]),
            ("(empty? [])", True),
            ("(empty? [1])", False),
        ]
        
        for lispy_code, expected in test_cases:
            result = run_lispy_string(lispy_code, self.web_safe_env)
            self.assertEqual(result, expected, f"Failed for: {lispy_code}")

    def test_documentation_works_in_web_safe_env(self):
        """Test that documentation functions work in web-safe environment."""
        # Test that doc function exists and works
        result = run_lispy_string("(doc '+)", self.web_safe_env)
        self.assertIsInstance(result, str)
        self.assertIn("add", result.lower())
        
        # Test that print-doc exists (we can't easily test its output)
        self.web_safe_env.lookup("print-doc")

    def test_promise_functions_available(self):
        """Test that promise/async functions are available in web-safe environment."""
        promise_functions = [
            "promise", "resolve", "reject", "promise-all", "promise-race", 
            "promise-any", "promise-all-settled", "timeout", "with-timeout",
            "async-map", "async-filter", "async-reduce", "debounce", "retry", "throttle"
        ]
        
        for func_name in promise_functions:
            try:
                self.web_safe_env.lookup(func_name)
            except EvaluationError:
                self.fail(f"Promise function '{func_name}' should be available in web-safe environment")

    def test_type_checking_functions_available(self):
        """Test that all type checking functions are available."""
        type_check_functions = [
            "is-number?", "is-string?", "is-boolean?", "is-list?", 
            "is-vector?", "is-map?", "is-nil?", "is-function?"
        ]
        
        for func_name in type_check_functions:
            try:
                self.web_safe_env.lookup(func_name)
            except EvaluationError:
                self.fail(f"Type check function '{func_name}' should be available in web-safe environment")

    def test_bdd_functions_included(self):
        """Test that BDD assertion functions are included (for now)."""
        bdd_functions = ["assert-equal?", "assert-true?", "assert-false?", "assert-nil?", "assert-not-nil?"]
        
        for func_name in bdd_functions:
            try:
                self.web_safe_env.lookup(func_name)
            except EvaluationError:
                self.fail(f"BDD function '{func_name}' should be available in web-safe environment")

    def test_environment_isolation(self):
        """Test that web-safe and regular environments are properly isolated."""
        # Define something in regular environment
        run_lispy_string("(define test-var 42)", self.regular_env)
        
        # Should exist in regular environment
        result = run_lispy_string("test-var", self.regular_env)
        self.assertEqual(result, 42)
        
        # Should NOT exist in web-safe environment
        with self.assertRaises(EvaluationError):
            run_lispy_string("test-var", self.web_safe_env)
        
        # Define something in web-safe environment
        run_lispy_string("(define web-safe-var 100)", self.web_safe_env)
        
        # Should exist in web-safe environment
        result = run_lispy_string("web-safe-var", self.web_safe_env)
        self.assertEqual(result, 100)
        
        # Should NOT exist in regular environment (they're separate instances)
        with self.assertRaises(EvaluationError):
            run_lispy_string("web-safe-var", self.regular_env)


if __name__ == '__main__':
    unittest.main() 
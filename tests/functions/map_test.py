import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector

class MapFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Define an 'inc' function for testing (expects 1 arg)
        run_lispy_string("(define inc (fn (x) (+ x 1)))", self.env)
        # Define an 'identity' function for testing (expects 1 arg)
        run_lispy_string("(define identity (fn (x) x))", self.env)
        # Define a function that expects 0 arguments
        run_lispy_string("(define zero-arg-fn (fn () 42))", self.env)
        # Define a function that expects 2 arguments
        run_lispy_string("(define two-arg-fn (fn (a b) (+ a b)))", self.env)


    def test_map_empty_vector(self):
        """Test (map [] inc) returns []."""
        lispy_code = "(map [] inc)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, Vector([]))

    def test_map_simple_vector(self):
        """Test (map [1 2 3] inc) returns [2 3 4]."""
        lispy_code = "(map [1 2 3] inc)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([2, 3, 4]))

    def test_map_original_vector_unchanged(self):
        """Test that map does not mutate the original vector."""
        run_lispy_string("(define my-vec [10 20 30])", self.env)
        lispy_code_map = "(map my-vec inc)"
        run_lispy_string(lispy_code_map, self.env)
        original_vec = run_lispy_string("my-vec", self.env)
        self.assertIsInstance(original_vec, Vector)
        self.assertEqual(original_vec, Vector([10, 20, 30]))

    def test_map_with_lambda(self):
        """Test map with an inline lambda function."""
        lispy_code = "(map [1 2 3 4] (fn (x) (* x x)))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 4, 9, 16]))

    def test_map_returns_different_types(self):
        """Test map with a function that returns different types."""
        # Define a function that returns a number if even, a string if odd
        run_lispy_string(
            "(define type-dispatcher (fn (x) (if (= (% x 2) 0) (* x 10) \"odd\")))",
            self.env
        )
        lispy_code = "(map [1 2 3 4] type-dispatcher)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["odd", 20, "odd", 40]))

    def test_map_incorrect_arg_count_too_few(self):
        """Test map with too few arguments."""
        lispy_code = "(map [])"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'map' expects 2 arguments, got 1.")

    def test_map_incorrect_arg_count_too_many(self):
        """Test map with too many arguments."""
        lispy_code = "(map [1 2] inc [3 4])"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'map' expects 2 arguments, got 3.")

    def test_map_first_arg_not_vector(self):
        """Test map when the first argument is not a vector."""
        lispy_code = "(map 1 inc)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "TypeError: First argument to 'map' must be a vector, got <class 'int'>.")

    def test_map_second_arg_not_procedure(self):
        """Test map when the second argument is not a procedure."""
        lispy_code = "(map [1 2 3] 1)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "TypeError: Second argument to 'map' must be a procedure, got <class 'int'>.")
    
    def test_map_first_arg_list_not_vector(self):
        """Test map when the first argument is a list instead of a vector."""
        lispy_code = "(map '(1 2 3) inc)" # Using a list instead of a vector
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "TypeError: First argument to 'map' must be a vector, got <class 'lispy.types.LispyList'>.")

    def test_map_proc_arity_zero(self):
        """Test map with a procedure that expects zero arguments."""
        lispy_code = "(map [1 2 3] zero-arg-fn)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        # The exact representation of the function might vary, so we check the core message.
        # Expected: "ArityError: Procedure <UserDefinedFunction params:()> passed to 'map' expects 1 argument, got 0."
        self.assertIn("expects 1 argument, got 0", str(cm.exception))
        self.assertIn("Procedure <UserDefinedFunction params:()> passed to 'map'", str(cm.exception))

    def test_map_proc_arity_two(self):
        """Test map with a procedure that expects two arguments."""
        lispy_code = "(map [1 2 3] two-arg-fn)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        # Expected: "ArityError: Procedure <UserDefinedFunction params:(a, b)> passed to 'map' expects 1 argument, got 2."
        self.assertIn("expects 1 argument, got 2", str(cm.exception))
        self.assertIn("Procedure <UserDefinedFunction params:(a, b)> passed to 'map'", str(cm.exception))

    def test_map_thread_first_composition(self):
        """Test map works beautifully in thread-first composition."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)
        run_lispy_string("(define double (fn [x] (* x 2)))", self.env)
        
        # Test thread-first composition: filter then map
        result = run_lispy_string("""
        (-> [-1 2 3 -4 5]
            (filter positive?)
            (map double))
        """, self.env)
        
        # Should filter to [2 3 5] then double to [4 6 10]
        self.assertEqual(result, Vector([4, 6, 10]))

if __name__ == '__main__':
    unittest.main() 
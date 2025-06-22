import unittest
from unittest.mock import patch
import io
import sys

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class DoseqFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_doseq_basic_vector(self):
        """Test basic doseq with vector."""
        # Test that doseq executes and returns nil
        result = run_lispy_string('(doseq [x [1 2 3]] x)', self.env)
        self.assertIsNone(result)  # doseq returns nil

    def test_doseq_basic_list(self):
        """Test basic doseq with list."""
        result = run_lispy_string("(doseq [x '(1 2 3)] x)", self.env)
        self.assertIsNone(result)

    def test_doseq_empty_collection(self):
        """Test doseq with empty collection."""
        result = run_lispy_string('(doseq [x []] x)', self.env)
        self.assertIsNone(result)  # Body should not execute

    def test_doseq_multiple_body_expressions(self):
        """Test doseq with multiple body expressions."""
        result = run_lispy_string('''(doseq [x [2 3 4]]
                                       (+ x 1)
                                       (* x 2))''', self.env)
        self.assertIsNone(result)

    def test_doseq_binding_scoping(self):
        """Test that binding variable is scoped to the doseq block."""
        run_lispy_string('(define x 100)', self.env)  # Outer x
        run_lispy_string('(doseq [x [1 2 3]] x)', self.env)  # Use x inside doseq
        
        # Outer x should remain unchanged
        outer_x = run_lispy_string('x', self.env)
        self.assertEqual(outer_x, 100)

    def test_doseq_access_outer_environment(self):
        """Test that doseq body can access outer environment."""
        run_lispy_string('(define multiplier 10)', self.env)
        result = run_lispy_string('(doseq [x [1 2 3]] (* x multiplier))', self.env)
        self.assertIsNone(result)

    def test_doseq_nested(self):
        """Test nested doseq forms."""
        result = run_lispy_string('''(doseq [x [1 2]]
                              (doseq [y [10 20]]
                                (+ x y)))''', self.env)
        self.assertIsNone(result)

    def test_doseq_with_range(self):
        """Test doseq with range function."""
        result = run_lispy_string('(doseq [i (range 3)] i)', self.env)
        self.assertIsNone(result)

    def test_doseq_with_complex_expressions(self):
        """Test doseq with complex binding and body expressions."""
        run_lispy_string('(define items [[1 2] [3 4]])', self.env)
        result = run_lispy_string('(doseq [item items] (first item))', self.env)
        self.assertIsNone(result)

    # Error Cases

    def test_doseq_no_arguments(self):
        """Test doseq with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'doseq' expects at least 2 arguments ([binding collection] body...), got 0."
        )

    def test_doseq_only_binding_vector(self):
        """Test doseq with only binding vector (no body)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x [1 2 3]])', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'doseq' expects at least 2 arguments ([binding collection] body...), got 1."
        )

    def test_doseq_binding_not_vector(self):
        """Test doseq with first argument not a vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq x (+ 1 2))', self.env)
        self.assertIn("SyntaxError: 'doseq' first argument must be a vector", str(cm.exception))

    def test_doseq_binding_vector_wrong_length_empty(self):
        """Test doseq with binding vector having wrong length (empty)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [] (+ 1 2))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'doseq' binding vector must have exactly 2 elements [binding collection], got 0."
        )

    def test_doseq_binding_vector_wrong_length_one(self):
        """Test doseq with binding vector having wrong length (one element)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x] (+ 1 2))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'doseq' binding vector must have exactly 2 elements [binding collection], got 1."
        )

    def test_doseq_binding_vector_wrong_length_three(self):
        """Test doseq with binding vector having wrong length (three elements)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x [1 2 3] y] (+ 1 2))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'doseq' binding vector must have exactly 2 elements [binding collection], got 3."
        )

    def test_doseq_binding_not_symbol(self):
        """Test doseq with binding not a symbol."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [1 [1 2 3]] (+ 1 2))', self.env)
        self.assertIn("SyntaxError: 'doseq' binding must be a symbol", str(cm.exception))

    def test_doseq_binding_string_not_symbol(self):
        """Test doseq with string binding (not a symbol)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq ["x" [1 2 3]] (+ 1 2))', self.env)
        self.assertIn("SyntaxError: 'doseq' binding must be a symbol", str(cm.exception))

    def test_doseq_binding_vector_not_symbol(self):
        """Test doseq with vector binding (not a symbol)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [[x y] [1 2 3]] (+ 1 2))', self.env)
        self.assertIn("SyntaxError: 'doseq' binding must be a symbol", str(cm.exception))

    def test_doseq_collection_not_vector_or_list_number(self):
        """Test doseq with collection that's not a vector or list (number)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x 123] (+ 1 2))', self.env)
        self.assertIn("TypeError: 'doseq' collection must be a vector or list", str(cm.exception))

    def test_doseq_collection_not_vector_or_list_string(self):
        """Test doseq with collection that's not a vector or list (string)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x "hello"] (+ 1 2))', self.env)
        self.assertIn("TypeError: 'doseq' collection must be a vector or list", str(cm.exception))

    def test_doseq_collection_not_vector_or_list_map(self):
        """Test doseq with collection that's not a vector or list (map)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x {:a 1}] (+ 1 2))', self.env)
        self.assertIn("TypeError: 'doseq' collection must be a vector or list", str(cm.exception))

    def test_doseq_collection_not_vector_or_list_nil(self):
        """Test doseq with collection that's not a vector or list (nil)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x nil] (+ 1 2))', self.env)
        self.assertIn("TypeError: 'doseq' collection must be a vector or list", str(cm.exception))

    def test_doseq_collection_expression_error(self):
        """Test doseq when collection expression evaluation fails."""
        with self.assertRaises(EvaluationError):
            run_lispy_string('(doseq [x (/ 1 0)] (+ 1 2))', self.env)

    def test_doseq_body_expression_error(self):
        """Test doseq when body expression evaluation fails."""
        with self.assertRaises(EvaluationError):
            run_lispy_string('(doseq [x [1 2 3]] (/ 1 0))', self.env)

    def test_doseq_binding_variable_in_collection_expression(self):
        """Test that binding variable is not available in collection expression."""
        # This should fail because x is not defined when evaluating the collection expression
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(doseq [x (cons x [1 2 3])] (+ 1 2))', self.env)
        self.assertIn("Unbound symbol", str(cm.exception))

    def test_doseq_with_function_calls_in_body(self):
        """Test doseq with function calls in body."""
        result = run_lispy_string('(doseq [x [1 2 3 4]] (* x x))', self.env)
        self.assertIsNone(result)

    def test_doseq_with_conditional_in_body(self):
        """Test doseq with conditional logic in body."""
        result = run_lispy_string('''(doseq [x [1 2 3 4 5 6]]
                              (if (= (% x 2) 0)
                                  x))''', self.env)
        self.assertIsNone(result)

    def test_doseq_scope_isolation(self):
        """Test that variables defined in doseq body don't leak to outer scope."""
        run_lispy_string('(doseq [x [1]] (define local_var x))', self.env)
        
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('local_var', self.env)
        self.assertIn("Unbound symbol", str(cm.exception))

    def test_doseq_with_list_collection_expression(self):
        """Test doseq where collection is created by list function."""
        result = run_lispy_string('(doseq [x (list 1 2 3)] (* x 2))', self.env)
        self.assertIsNone(result)

    def test_doseq_with_vector_collection_expression(self):
        """Test doseq where collection is created by vector function."""
        result = run_lispy_string('(doseq [x (vector 5 10 15)] (/ x 5))', self.env)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main() 
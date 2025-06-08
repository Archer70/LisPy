import unittest

from lispy.types import Vector, Symbol
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class GetFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # Vector access tests
    def test_get_vector_valid_index(self):
        """Test (get [10 20 30] 1) returns 20."""
        result = run_lispy_string("(get [10 20 30] 1)", self.env)
        self.assertEqual(result, 20)

    def test_get_vector_first_index(self):
        """Test (get [10 20 30] 0) returns 10."""
        result = run_lispy_string("(get [10 20 30] 0)", self.env)
        self.assertEqual(result, 10)

    def test_get_vector_last_index(self):
        """Test (get [10 20 30] 2) returns 30."""
        result = run_lispy_string("(get [10 20 30] 2)", self.env)
        self.assertEqual(result, 30)

    def test_get_vector_single_element(self):
        """Test (get [42] 0) returns 42."""
        result = run_lispy_string("(get [42] 0)", self.env)
        self.assertEqual(result, 42)

    def test_get_vector_out_of_bounds_no_default(self):
        """Test (get [10 20] 5) raises IndexError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get [10 20] 5)", self.env)
        self.assertIn("IndexError", str(cm.exception))
        self.assertIn("5 out of bounds for vector of size 2", str(cm.exception))

    def test_get_vector_negative_index_no_default(self):
        """Test (get [10 20] -1) raises IndexError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get [10 20] -1)", self.env)
        self.assertIn("IndexError", str(cm.exception))

    def test_get_vector_out_of_bounds_with_default(self):
        """Test (get [10 20] 5 \"default\") returns \"default\"."""
        result = run_lispy_string('(get [10 20] 5 "default")', self.env)
        self.assertEqual(result, "default")

    def test_get_vector_negative_index_with_default(self):
        """Test (get [10 20] -1 \"default\") returns \"default\"."""
        result = run_lispy_string('(get [10 20] -1 "default")', self.env)
        self.assertEqual(result, "default")

    def test_get_empty_vector_with_default(self):
        """Test (get [] 0 \"empty\") returns \"empty\"."""
        result = run_lispy_string('(get [] 0 "empty")', self.env)
        self.assertEqual(result, "empty")

    def test_get_vector_non_integer_index(self):
        """Test (get [10 20] \"0\") raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(get [10 20] "0")', self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("Vector index must be an integer", str(cm.exception))

    # Map access tests
    def test_get_map_existing_key(self):
        """Test (get {:a 1 :b 2} ':a) returns 1."""
        result = run_lispy_string("(get {:a 1 :b 2} ':a)", self.env)
        self.assertEqual(result, 1)

    def test_get_map_another_existing_key(self):
        """Test (get {:name \"Alice\" :age 30} ':name) returns \"Alice\"."""
        result = run_lispy_string('(get {:name "Alice" :age 30} \':name)', self.env)
        self.assertEqual(result, "Alice")

    def test_get_map_missing_key_no_default(self):
        """Test (get {:a 1 :b 2} ':c) returns nil."""
        result = run_lispy_string("(get {:a 1 :b 2} ':c)", self.env)
        self.assertIsNone(result)

    def test_get_map_missing_key_with_default(self):
        """Test (get {:a 1 :b 2} ':c \"not found\") returns \"not found\"."""
        result = run_lispy_string('(get {:a 1 :b 2} \':c "not found")', self.env)
        self.assertEqual(result, "not found")

    def test_get_empty_map_no_default(self):
        """Test (get {} ':missing) returns nil."""
        result = run_lispy_string("(get {} ':missing)", self.env)
        self.assertIsNone(result)

    def test_get_empty_map_with_default(self):
        """Test (get {} ':missing \"default\") returns \"default\"."""
        result = run_lispy_string('(get {} \':missing "default")', self.env)
        self.assertEqual(result, "default")

    def test_get_map_non_symbol_key(self):
        """Test (get {:a 1} \"a\") raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(get {:a 1} "a")', self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("Map key must be a symbol", str(cm.exception))

    def test_get_map_integer_key(self):
        """Test (get {:a 1} 0) raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get {:a 1} 0)", self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("Map key must be a symbol", str(cm.exception))

    # Mixed data type tests
    def test_get_vector_mixed_types(self):
        """Test get with vectors containing mixed data types."""
        result = run_lispy_string('(get [1 "hello" true nil] 1)', self.env)
        self.assertEqual(result, "hello")
        
        result = run_lispy_string('(get [1 "hello" true nil] 2)', self.env)
        self.assertEqual(result, True)
        
        result = run_lispy_string('(get [1 "hello" true nil] 3)', self.env)
        self.assertIsNone(result)

    def test_get_map_mixed_value_types(self):
        """Test get with maps containing mixed value types."""
        result = run_lispy_string('(get {:num 42 :str "hello" :bool true :nil nil} \':str)', self.env)
        self.assertEqual(result, "hello")
        
        result = run_lispy_string('(get {:num 42 :str "hello" :bool true :nil nil} \':bool)', self.env)
        self.assertEqual(result, True)
        
        result = run_lispy_string('(get {:num 42 :str "hello" :bool true :nil nil} \':nil)', self.env)
        self.assertIsNone(result)

    # Default value tests
    def test_get_default_value_types(self):
        """Test get with various default value types."""
        # String default
        result = run_lispy_string('(get [] 0 "default")', self.env)
        self.assertEqual(result, "default")
        
        # Number default
        result = run_lispy_string("(get [] 0 42)", self.env)
        self.assertEqual(result, 42)
        
        # Boolean default
        result = run_lispy_string("(get [] 0 true)", self.env)
        self.assertEqual(result, True)
        
        # Vector default
        result = run_lispy_string("(get [] 0 [1 2 3])", self.env)
        self.assertEqual(result, Vector([1, 2, 3]))
        
        # Map default
        result = run_lispy_string("(get [] 0 {:default true})", self.env)
        self.assertEqual(result, {Symbol(':default'): True})

    # Error handling tests
    def test_get_wrong_collection_type(self):
        """Test (get \"string\" 0) raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(get "string" 0)', self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("'get' first argument must be a vector or map", str(cm.exception))

    def test_get_wrong_collection_type_number(self):
        """Test (get 42 0) raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get 42 0)", self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("'get' first argument must be a vector or map", str(cm.exception))

    def test_get_wrong_collection_type_boolean(self):
        """Test (get true 0) raises TypeError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get true 0)", self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("'get' first argument must be a vector or map", str(cm.exception))

    def test_get_no_args(self):
        """Test (get) raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'get' expects 2 or 3 arguments, got 0.")

    def test_get_one_arg(self):
        """Test (get [1 2 3]) raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(get [1 2 3])", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'get' expects 2 or 3 arguments, got 1.")

    def test_get_too_many_args(self):
        """Test (get [1 2 3] 0 \"default\" \"extra\") raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(get [1 2 3] 0 "default" "extra")', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'get' expects 2 or 3 arguments, got 4.")

    # Nested structure tests
    def test_get_nested_vectors(self):
        """Test get with nested vectors."""
        result = run_lispy_string("(get [[1 2] [3 4] [5 6]] 1)", self.env)
        self.assertEqual(result, Vector([3, 4]))
        
        # Get element from nested vector
        result = run_lispy_string("(get (get [[1 2] [3 4] [5 6]] 1) 0)", self.env)
        self.assertEqual(result, 3)

    def test_get_nested_maps(self):
        """Test get with nested maps."""
        result = run_lispy_string("(get {:user {:name \"Alice\" :age 30}} ':user)", self.env)
        expected = {Symbol(':name'): "Alice", Symbol(':age'): 30}
        self.assertEqual(result, expected)
        
        # Get from nested map
        result = run_lispy_string("(get (get {:user {:name \"Alice\" :age 30}} ':user) ':name)", self.env)
        self.assertEqual(result, "Alice")

    def test_get_vector_containing_maps(self):
        """Test get with vector containing maps."""
        result = run_lispy_string("(get [{:a 1} {:b 2} {:c 3}] 1)", self.env)
        expected = {Symbol(':b'): 2}
        self.assertEqual(result, expected)

    def test_get_map_containing_vectors(self):
        """Test get with map containing vectors."""
        result = run_lispy_string("(get {:nums [1 2 3] :letters [\"a\" \"b\" \"c\"]} ':letters)", self.env)
        expected = Vector(["a", "b", "c"])
        self.assertEqual(result, expected)

    # Practical usage tests
    def test_get_with_variables(self):
        """Test get using variables for collections and keys."""
        run_lispy_string("(define my-vector [10 20 30])", self.env)
        run_lispy_string("(define my-index 1)", self.env)
        
        result = run_lispy_string("(get my-vector my-index)", self.env)
        self.assertEqual(result, 20)
        
        run_lispy_string("(define my-map {:name \"Bob\" :age 25})", self.env)
        result = run_lispy_string("(get my-map ':name)", self.env)
        self.assertEqual(result, "Bob")

    def test_get_chained_operations(self):
        """Test get in combination with other operations."""
        # Get + arithmetic
        result = run_lispy_string("(+ (get [1 2 3] 0) (get [1 2 3] 2))", self.env)
        self.assertEqual(result, 4)  # 1 + 3
        
        # Get + comparison (using equal? for general equality)
        result = run_lispy_string('(equal? (get {:status "active"} \':status) "active")', self.env)
        self.assertEqual(result, True)
        
        # Get + conditionals
        result = run_lispy_string('(if (get {:enabled true} \':enabled) "yes" "no")', self.env)
        self.assertEqual(result, "yes")

    def test_get_with_nil_values(self):
        """Test get when dealing with nil values."""
        # Vector containing nil
        result = run_lispy_string("(get [1 nil 3] 1)", self.env)
        self.assertIsNone(result)
        
        # Map with nil value
        result = run_lispy_string("(get {:key nil} ':key)", self.env)
        self.assertIsNone(result)
        
        # Distinguish between nil value and missing key
        result = run_lispy_string("(get {:key nil} ':key)", self.env)
        self.assertIsNone(result)  # nil value exists
        
        result = run_lispy_string("(get {:key nil} ':missing)", self.env)
        self.assertIsNone(result)  # missing key returns nil


if __name__ == '__main__':
    unittest.main() 
import unittest

from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class EqualQTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # Basic primitive equality tests
    def test_equal_numbers_same(self):
        """Test (equal? 5 5) returns true."""
        result = run_lispy_string("(equal? 5 5)", self.env)
        self.assertEqual(result, True)

    def test_equal_numbers_different(self):
        """Test (equal? 5 6) returns false."""
        result = run_lispy_string("(equal? 5 6)", self.env)
        self.assertEqual(result, False)

    def test_equal_numbers_int_float(self):
        """Test (equal? 5 5.0) returns true."""
        result = run_lispy_string("(equal? 5 5.0)", self.env)
        self.assertEqual(result, True)

    def test_equal_strings_same(self):
        """Test (equal? \"hello\" \"hello\") returns true."""
        result = run_lispy_string('(equal? "hello" "hello")', self.env)
        self.assertEqual(result, True)

    def test_equal_strings_different(self):
        """Test (equal? \"hello\" \"world\") returns false."""
        result = run_lispy_string('(equal? "hello" "world")', self.env)
        self.assertEqual(result, False)

    def test_equal_booleans_same_true(self):
        """Test (equal? true true) returns true."""
        result = run_lispy_string("(equal? true true)", self.env)
        self.assertEqual(result, True)

    def test_equal_booleans_same_false(self):
        """Test (equal? false false) returns true."""
        result = run_lispy_string("(equal? false false)", self.env)
        self.assertEqual(result, True)

    def test_equal_booleans_different(self):
        """Test (equal? true false) returns false."""
        result = run_lispy_string("(equal? true false)", self.env)
        self.assertEqual(result, False)

    def test_equal_nil_same(self):
        """Test (equal? nil nil) returns true."""
        result = run_lispy_string("(equal? nil nil)", self.env)
        self.assertEqual(result, True)

    def test_equal_nil_different(self):
        """Test (equal? nil 0) returns false."""
        result = run_lispy_string("(equal? nil 0)", self.env)
        self.assertEqual(result, False)

    # Cross-type equality tests (should be false)
    def test_equal_number_string(self):
        """Test (equal? 5 \"5\") returns false."""
        result = run_lispy_string('(equal? 5 "5")', self.env)
        self.assertEqual(result, False)

    def test_equal_number_boolean(self):
        """Test (equal? 1 true) returns false."""
        result = run_lispy_string("(equal? 1 true)", self.env)
        self.assertEqual(result, False)

    def test_equal_string_boolean(self):
        """Test (equal? \"true\" true) returns false."""
        result = run_lispy_string('(equal? "true" true)', self.env)
        self.assertEqual(result, False)

    def test_equal_empty_string_nil(self):
        """Test (equal? \"\" nil) returns false."""
        result = run_lispy_string('(equal? "" nil)', self.env)
        self.assertEqual(result, False)

    # Vector equality tests
    def test_equal_vectors_same(self):
        """Test (equal? [1 2 3] [1 2 3]) returns true."""
        result = run_lispy_string("(equal? [1 2 3] [1 2 3])", self.env)
        self.assertEqual(result, True)

    def test_equal_vectors_different_values(self):
        """Test (equal? [1 2 3] [1 2 4]) returns false."""
        result = run_lispy_string("(equal? [1 2 3] [1 2 4])", self.env)
        self.assertEqual(result, False)

    def test_equal_vectors_different_length(self):
        """Test (equal? [1 2 3] [1 2]) returns false."""
        result = run_lispy_string("(equal? [1 2 3] [1 2])", self.env)
        self.assertEqual(result, False)

    def test_equal_vectors_different_order(self):
        """Test (equal? [1 2 3] [3 2 1]) returns false."""
        result = run_lispy_string("(equal? [1 2 3] [3 2 1])", self.env)
        self.assertEqual(result, False)

    def test_equal_vectors_empty(self):
        """Test (equal? [] []) returns true."""
        result = run_lispy_string("(equal? [] [])", self.env)
        self.assertEqual(result, True)

    def test_equal_vectors_mixed_types(self):
        """Test (equal? [1 \"hello\" true] [1 \"hello\" true]) returns true."""
        result = run_lispy_string(
            '(equal? [1 "hello" true] [1 "hello" true])', self.env
        )
        self.assertEqual(result, True)

    def test_equal_vectors_with_nil(self):
        """Test (equal? [1 nil 3] [1 nil 3]) returns true."""
        result = run_lispy_string("(equal? [1 nil 3] [1 nil 3])", self.env)
        self.assertEqual(result, True)

    # Map equality tests
    def test_equal_maps_same(self):
        """Test (equal? {:a 1 :b 2} {:a 1 :b 2}) returns true."""
        result = run_lispy_string("(equal? {:a 1 :b 2} {:a 1 :b 2})", self.env)
        self.assertEqual(result, True)

    def test_equal_maps_different_order(self):
        """Test (equal? {:a 1 :b 2} {:b 2 :a 1}) returns true (order independent)."""
        result = run_lispy_string("(equal? {:a 1 :b 2} {:b 2 :a 1})", self.env)
        self.assertEqual(result, True)

    def test_equal_maps_different_values(self):
        """Test (equal? {:a 1 :b 2} {:a 1 :b 3}) returns false."""
        result = run_lispy_string("(equal? {:a 1 :b 2} {:a 1 :b 3})", self.env)
        self.assertEqual(result, False)

    def test_equal_maps_different_keys(self):
        """Test (equal? {:a 1 :b 2} {:a 1 :c 2}) returns false."""
        result = run_lispy_string("(equal? {:a 1 :b 2} {:a 1 :c 2})", self.env)
        self.assertEqual(result, False)

    def test_equal_maps_different_size(self):
        """Test (equal? {:a 1 :b 2} {:a 1}) returns false."""
        result = run_lispy_string("(equal? {:a 1 :b 2} {:a 1})", self.env)
        self.assertEqual(result, False)

    def test_equal_maps_empty(self):
        """Test (equal? {} {}) returns true."""
        result = run_lispy_string("(equal? {} {})", self.env)
        self.assertEqual(result, True)

    def test_equal_maps_with_nil_values(self):
        """Test (equal? {:a nil :b 2} {:a nil :b 2}) returns true."""
        result = run_lispy_string("(equal? {:a nil :b 2} {:a nil :b 2})", self.env)
        self.assertEqual(result, True)

    # List equality tests
    def test_equal_lists_same(self):
        """Test (equal? '(1 2 3) '(1 2 3)) returns true."""
        result = run_lispy_string("(equal? '(1 2 3) '(1 2 3))", self.env)
        self.assertEqual(result, True)

    def test_equal_lists_different(self):
        """Test (equal? '(1 2 3) '(1 2 4)) returns false."""
        result = run_lispy_string("(equal? '(1 2 3) '(1 2 4))", self.env)
        self.assertEqual(result, False)

    def test_equal_lists_empty(self):
        """Test (equal? '() '()) returns true."""
        result = run_lispy_string("(equal? '() '())", self.env)
        self.assertEqual(result, True)

    # Cross-collection type tests (should be false)
    def test_equal_vector_list_same_elements(self):
        """Test (equal? [1 2 3] '(1 2 3)) returns false (different types)."""
        result = run_lispy_string("(equal? [1 2 3] '(1 2 3))", self.env)
        self.assertEqual(result, False)

    def test_equal_vector_map(self):
        """Test (equal? [1 2] {:a 1 :b 2}) returns false."""
        result = run_lispy_string("(equal? [1 2] {:a 1 :b 2})", self.env)
        self.assertEqual(result, False)

    # Nested structure equality tests
    def test_equal_nested_vectors(self):
        """Test (equal? [[1 2] [3 4]] [[1 2] [3 4]]) returns true."""
        result = run_lispy_string("(equal? [[1 2] [3 4]] [[1 2] [3 4]])", self.env)
        self.assertEqual(result, True)

    def test_equal_nested_vectors_different(self):
        """Test (equal? [[1 2] [3 4]] [[1 2] [3 5]]) returns false."""
        result = run_lispy_string("(equal? [[1 2] [3 4]] [[1 2] [3 5]])", self.env)
        self.assertEqual(result, False)

    def test_equal_nested_maps(self):
        """Test (equal? {:user {:name \"Alice\"}} {:user {:name \"Alice\"}}) returns true."""
        result = run_lispy_string(
            '(equal? {:user {:name "Alice"}} {:user {:name "Alice"}})', self.env
        )
        self.assertEqual(result, True)

    def test_equal_nested_maps_different(self):
        """Test (equal? {:user {:name \"Alice\"}} {:user {:name \"Bob\"}}) returns false."""
        result = run_lispy_string(
            '(equal? {:user {:name "Alice"}} {:user {:name "Bob"}})', self.env
        )
        self.assertEqual(result, False)

    def test_equal_mixed_nested_structures(self):
        """Test (equal? {:data [1 2]} {:data [1 2]}) returns true."""
        result = run_lispy_string("(equal? {:data [1 2]} {:data [1 2]})", self.env)
        self.assertEqual(result, True)

    def test_equal_complex_nested_structure(self):
        """Test complex nested structure equality."""
        code = """(equal? 
                    {:users [{:name "Alice" :active true} {:name "Bob" :active false}] 
                     :config {:debug true :version 1.0}}
                    {:users [{:name "Alice" :active true} {:name "Bob" :active false}] 
                     :config {:debug true :version 1.0}})"""
        result = run_lispy_string(code, self.env)
        self.assertEqual(result, True)

    # Multi-argument tests
    def test_equal_multiple_args_all_same(self):
        """Test (equal? 5 5 5 5) returns true."""
        result = run_lispy_string("(equal? 5 5 5 5)", self.env)
        self.assertEqual(result, True)

    def test_equal_multiple_args_one_different(self):
        """Test (equal? 5 5 6 5) returns false."""
        result = run_lispy_string("(equal? 5 5 6 5)", self.env)
        self.assertEqual(result, False)

    def test_equal_multiple_vectors(self):
        """Test (equal? [1 2] [1 2] [1 2]) returns true."""
        result = run_lispy_string("(equal? [1 2] [1 2] [1 2])", self.env)
        self.assertEqual(result, True)

    def test_equal_multiple_mixed_types_all_different(self):
        """Test (equal? 5 \"5\" [5] {:a 5}) returns false."""
        result = run_lispy_string('(equal? 5 "5" [5] {:a 5})', self.env)
        self.assertEqual(result, False)

    # Error handling tests
    def test_equal_no_args(self):
        """Test (equal?) raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(equal?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'equal?' requires at least 2 arguments, got 0.",
        )

    def test_equal_one_arg(self):
        """Test (equal? 5) raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(equal? 5)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'equal?' requires at least 2 arguments, got 1.",
        )

    # Symbol equality tests
    def test_equal_symbols_same(self):
        """Test (equal? ':a ':a) returns true."""
        result = run_lispy_string("(equal? ':a ':a)", self.env)
        self.assertEqual(result, True)

    def test_equal_symbols_different(self):
        """Test (equal? ':a ':b) returns false."""
        result = run_lispy_string("(equal? ':a ':b)", self.env)
        self.assertEqual(result, False)

    # Practical usage tests
    def test_equal_with_get_function(self):
        """Test equal? works with get function for string comparison."""
        result = run_lispy_string(
            '(equal? (get {:status "active"} \':status) "active")', self.env
        )
        self.assertEqual(result, True)

    def test_equal_with_variables(self):
        """Test equal? works with variables."""
        run_lispy_string("(define my-vector [1 2 3])", self.env)
        run_lispy_string("(define other-vector [1 2 3])", self.env)
        result = run_lispy_string("(equal? my-vector other-vector)", self.env)
        self.assertEqual(result, True)

    def test_equal_chained_comparison(self):
        """Test equal? in conditional expressions."""
        result = run_lispy_string(
            '(if (equal? "hello" "hello") "same" "different")', self.env
        )
        self.assertEqual(result, "same")


if __name__ == "__main__":
    unittest.main()

import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError, ArityError
from lispy.types import LispyList, Vector

class ReduceFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Helper for string concatenation - needs a proper string-append eventually
        # For now, using a simplified Python-backed version for testing reduce
        self.env.store['py-concat'] = lambda args, env: args[0] + args[1]
        run_lispy_string("(define string-append (fn [s1 s2] (py-concat s1 s2)))", self.env)
        run_lispy_string("""
        (define concat-str (fn [acc item]
                             (string-append acc item)))
        """, self.env)
        run_lispy_string("""
        (define cons-onto (fn [acc item]
                            (cons item acc)))""", self.env)
        run_lispy_string("""
        (define sum-of-doubles (fn [acc item]
                                 (+ acc (* item 2))))
        """, self.env)
        run_lispy_string("(define zero-arg-reducer (fn [] 0))", self.env)
        run_lispy_string("(define one-arg-reducer (fn [x] x))", self.env)
        run_lispy_string("(define three-arg-reducer (fn [a b c] (+ a b c)))", self.env)

    def test_reduce_empty_vector_no_initial(self):
        """Test (reduce [] +) raises error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce [] +)", self.env)
        self.assertEqual(str(cm.exception), "ValueError: reduce() of empty sequence with no initial value.")

    def test_reduce_empty_list_no_initial(self):
        """Test (reduce '() +) raises error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce '() +)", self.env)
        self.assertEqual(str(cm.exception), "ValueError: reduce() of empty sequence with no initial value.")

    def test_reduce_empty_vector_with_initial(self):
        """Test (reduce [] + 0) returns 0."""
        result = run_lispy_string("(reduce [] + 0)", self.env)
        self.assertEqual(result, 0)

    def test_reduce_empty_list_with_initial(self):
        """Test (reduce '() + 0) returns 0."""
        result = run_lispy_string("(reduce '() + 0)", self.env)
        self.assertEqual(result, 0)

    def test_reduce_vector_sum_no_initial(self):
        """Test (reduce [1 2 3 4] +) returns 10."""
        result = run_lispy_string("(reduce [1 2 3 4] +)", self.env)
        self.assertEqual(result, 10)

    def test_reduce_list_sum_no_initial(self):
        """Test (reduce '(1 2 3 4) +) returns 10."""
        result = run_lispy_string("(reduce '(1 2 3 4) +)", self.env)
        self.assertEqual(result, 10)

    def test_reduce_vector_sum_with_initial(self):
        """Test (reduce [1 2 3 4] + 10) returns 20."""
        result = run_lispy_string("(reduce [1 2 3 4] + 10)", self.env)
        self.assertEqual(result, 20)

    def test_reduce_list_sum_with_initial(self):
        """Test (reduce '(1 2 3 4) + 10) returns 20."""
        result = run_lispy_string("(reduce '(1 2 3 4) + 10)", self.env)
        self.assertEqual(result, 20)

    def test_reduce_single_element_vector_no_initial(self):
        """Test (reduce [5] +) returns 5."""
        result = run_lispy_string("(reduce [5] +)", self.env)
        self.assertEqual(result, 5)

    def test_reduce_single_element_list_no_initial(self):
        """Test (reduce '(5) +) returns 5."""
        result = run_lispy_string("(reduce '(5) +)", self.env)
        self.assertEqual(result, 5)

    def test_reduce_single_element_vector_with_initial(self):
        """Test (reduce [5] + 10) returns 15."""
        result = run_lispy_string("(reduce [5] + 10)", self.env)
        self.assertEqual(result, 15)

    def test_reduce_single_element_list_with_initial(self):
        """Test (reduce '(5) + 10) returns 15."""
        result = run_lispy_string("(reduce '(5) + 10)", self.env)
        self.assertEqual(result, 15)

    def test_reduce_string_concat_vector_with_initial(self):
        """Test (reduce ["a" "b" "c"] concat-str "") returns "abc"."""
        result = run_lispy_string("(reduce [\"a\" \"b\" \"c\"] concat-str \"\")", self.env)
        self.assertEqual(result, "abc")

    def test_reduce_string_concat_list_no_initial(self):
        """Test (reduce '("a" "b" "c") concat-str) returns "abc"."""
        result = run_lispy_string("(reduce '(\"a\" \"b\" \"c\") concat-str)", self.env)
        self.assertEqual(result, "abc")

    def test_reduce_custom_fn_build_list(self):
        """Test (reduce [1 2 3] cons-onto '()) returns (3 2 1)."""
        result = run_lispy_string("(reduce [1 2 3] cons-onto '())", self.env)
        self.assertEqual(result, LispyList([3, 2, 1]))

    # --- Argument Validation Tests ---
    def test_reduce_too_few_args(self):
        """Test reduce with too few arguments (0 or 1)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'reduce' expects 2 or 3 arguments, got 0.")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce [])", self.env) # Was (reduce +)
        self.assertEqual(str(cm.exception), "SyntaxError: 'reduce' expects 2 or 3 arguments, got 1.")

    def test_reduce_too_many_args(self):
        """Test reduce with too many arguments (4)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce [1 2] + 0 'extra)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'reduce' expects 2 or 3 arguments, got 4.")

    def test_reduce_collection_not_list_or_vector(self):
        """Test reduce when collection is not a list or vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce \"abc\" + 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: First argument to 'reduce' must be a list or vector, got <class 'str'>.")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce 123 + 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: First argument to 'reduce' must be a list or vector, got <class 'int'>.")

    def test_reduce_procedure_not_callable(self):
        """Test reduce when the procedure argument is not callable."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce [1 2] 123 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: Second argument to 'reduce' must be a procedure, got <class 'int'>.")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(reduce [1 2] \'(not-a-fn) 0)", self.env)
        self.assertEqual(str(cm.exception), "TypeError: Second argument to 'reduce' must be a procedure, got <class 'lispy.types.LispyList'>.")

    def test_reduce_proc_arity_incorrect_zero_args(self):
        """Test reduce when the reducing procedure expects 0 arguments."""
        with self.assertRaises(ArityError) as cm:
            run_lispy_string("(reduce [1 2] zero-arg-reducer 0)", self.env)
        self.assertEqual(str(cm.exception), "Procedure <UserDefinedFunction params:()> passed to 'reduce' expects 2 arguments, got 0.")

    def test_reduce_proc_arity_incorrect_one_arg(self):
        """Test reduce when the reducing procedure expects 1 argument."""
        with self.assertRaises(ArityError) as cm:
            run_lispy_string("(reduce [1 2] one-arg-reducer 0)", self.env)
        self.assertEqual(str(cm.exception), "Procedure <UserDefinedFunction params:(x)> passed to 'reduce' expects 2 arguments, got 1.")

    def test_reduce_proc_arity_incorrect_three_args(self):
        """Test reduce when the reducing procedure expects 3 arguments."""
        with self.assertRaises(ArityError) as cm:
            run_lispy_string("(reduce [1 2] three-arg-reducer 0)", self.env)
        self.assertEqual(str(cm.exception), "Procedure <UserDefinedFunction params:(a, b, c)> passed to 'reduce' expects 2 arguments, got 3.")

    def test_reduce_with_thread_first(self):
        """Test reduce used with the -> (thread-first) macro."""
        result1 = run_lispy_string("(-> [1 2 3 4] (reduce +))", self.env)
        self.assertEqual(result1, 10)
        result2 = run_lispy_string("(-> [1 2 3 4] (reduce + 0))", self.env)
        self.assertEqual(result2, 10)
        result3 = run_lispy_string("(-> [1 2 3] (reduce sum-of-doubles 0))", self.env)
        self.assertEqual(result3, 12)

if __name__ == '__main__':
    unittest.main() 
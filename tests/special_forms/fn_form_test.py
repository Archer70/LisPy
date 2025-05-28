# lispy_project/tests/special_forms/fn_form_test.py
import unittest

from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string
from lispy.closure import Function # For type checking and direct instantiation in tests


class FnFormTest(unittest.TestCase): # Renamed class

    def setUp(self):
        self.env = create_global_env()

    # --- Tests for 'fn' special form and function calls --- # Updated comment
    def test_fn_creation(self): # Renamed test
        # (fn (x) (+ x 1))
        result = run_lispy_string("(fn [x] (+ x 1))", self.env)
        self.assertIsInstance(result, Function)
        self.assertEqual(len(result.params), 1)
        self.assertEqual(result.params[0].name, "x")
        self.assertEqual(len(result.body), 1)
        self.assertIs(result.defining_env, self.env) # Should capture the current env

    def test_fn_call_simple(self): # Renamed test
        # ((fn (x) (+ x 1)) 10) -> 11
        result = run_lispy_string("((fn [x] (+ x 1)) 10)", self.env)
        self.assertEqual(result, 11)

    def test_fn_call_multiple_params(self): # Renamed test
        # ((fn (x y) (+ x y)) 3 4) -> 7
        result = run_lispy_string("((fn [x y] (+ x y)) 3 4)", self.env)
        self.assertEqual(result, 7)

    def test_fn_call_no_params(self): # Renamed test
        # ((fn () 42)) -> 42
        result = run_lispy_string("((fn [] 42))", self.env)
        self.assertEqual(result, 42)

    def test_fn_call_multiple_body_expressions(self): # Renamed test
        # ((fn (x) (define y x) (+ y 10)) 5) -> 15
        # The define y x will happen in the fn's call_env
        result = run_lispy_string("((fn [x] (define y x) (+ y 10)) 5)", self.env)
        self.assertEqual(result, 15)

    def test_fn_closure_captures_defining_env(self): # Renamed test
        # (define make-adder (fn (n) (fn (x) (+ x n))))
        # (define add5 (make-adder 5))
        # (add5 3) -> 8
        run_lispy_string("(define n_outer 100)", self.env) # Should not be used by add5 if closure is correct

        run_lispy_string("(define make-adder (fn [n] (fn [x] (+ x n))))", self.env)
        add5_function = run_lispy_string("(make-adder 5)", self.env)
        self.assertIsInstance(add5_function, Function)
        run_lispy_string("(define add5 (make-adder 5))", self.env)

        result = run_lispy_string("(add5 3)", self.env)
        self.assertEqual(result, 8)

        run_lispy_string("(define add7 (make-adder 7))", self.env)
        result2 = run_lispy_string("(add7 10)", self.env)
        self.assertEqual(result2, 17)

    def test_fn_define_and_call(self): # Renamed test
        # (define my-add (fn (a b) (+ a b)))
        # (my-add 10 20) -> 30
        run_lispy_string("(define my-add (fn [a b] (+ a b)))", self.env)
        result = run_lispy_string("(my-add 10 20)", self.env)
        self.assertEqual(result, 30)

    def test_fn_recursion_via_define(self): # Renamed test
        run_lispy_string("(define fact (fn [n] (if (<= n 1) 1 (* n (fact (- n 1))))))", self.env)
        result = run_lispy_string("(fact 5)", self.env)
        self.assertEqual(result, 120)

    def test_fn_arity_error_too_few_args(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("((fn [x y] (+ x y)) 1)", self.env)
        self.assertTrue("ArityError" in str(cm.exception))
        self.assertTrue("expects 2 arguments, got 1" in str(cm.exception))

    def test_fn_arity_error_too_many_args(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("((fn [x] x) 1 2)", self.env)
        self.assertTrue("ArityError" in str(cm.exception))
        self.assertTrue("expects 1 argument" in str(cm.exception))
        self.assertTrue("got 2" in str(cm.exception))

    def test_fn_syntax_error_no_params_or_body(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(fn)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'fn' requires a parameter list and at least one body expression. Usage: (fn (params...) body1 ...)")

    def test_fn_syntax_error_no_body(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(fn [])", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'fn' requires a parameter list and at least one body expression. Usage: (fn (params...) body1 ...)")

    def test_fn_syntax_error_params_not_list(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(fn x x)", self.env)
        self.assertTrue("SyntaxError: Parameter list for 'fn' must be a list" in str(cm.exception))

    def test_fn_syntax_error_param_not_symbol(self): # Renamed test
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(fn [123] x)", self.env)
        self.assertTrue("SyntaxError: All parameters in 'fn' parameter list must be symbols" in str(cm.exception))
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(fn [x "a-string"] x)', self.env)
        self.assertTrue("SyntaxError: All parameters in 'fn' parameter list must be symbols" in str(cm.exception))

if __name__ == '__main__':
    unittest.main() 
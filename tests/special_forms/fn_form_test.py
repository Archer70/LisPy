# lispy_project/tests/special_forms/fn_form_test.py
import unittest

from lispy.evaluator import evaluate
from lispy.functions import global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol
from lispy.environment import Environment
from lispy.closure import Function # For type checking and direct instantiation in tests

class FnFormTest(unittest.TestCase): # Renamed class

    def setUp(self):
        self.env = Environment(outer=global_env)
        self.empty_env = Environment() # For tests that might need a truly empty env

    # --- Tests for 'fn' special form and function calls --- # Updated comment
    def test_fn_creation(self): # Renamed test
        # (fn (x) (+ x 1))
        params = [Symbol("x")]
        body = [[Symbol("+"), Symbol("x"), 1]] # Body is a list of expressions
        expr = [Symbol("fn"), params, *body] # Changed Symbol("lambda") to Symbol("fn")
        
        result = evaluate(expr, self.env)
        self.assertIsInstance(result, Function)
        self.assertEqual(result.params, params)
        self.assertEqual(result.body, body)
        self.assertIs(result.defining_env, self.env) # Should capture the current env

    def test_fn_call_simple(self): # Renamed test
        # ((fn (x) (+ x 1)) 10) -> 11
        fn_expr = [Symbol("fn"), [Symbol("x")], [Symbol("+"), Symbol("x"), 1]] # Changed Symbol("lambda") to Symbol("fn")
        call_expr = [fn_expr, 10]
        self.assertEqual(evaluate(call_expr, self.env), 11)

    def test_fn_call_multiple_params(self): # Renamed test
        # ((fn (x y) (+ x y)) 3 4) -> 7
        fn_expr = [Symbol("fn"), [Symbol("x"), Symbol("y")], [Symbol("+"), Symbol("x"), Symbol("y")]] # Changed Symbol("lambda") to Symbol("fn")
        call_expr = [fn_expr, 3, 4]
        self.assertEqual(evaluate(call_expr, self.env), 7)

    def test_fn_call_no_params(self): # Renamed test
        # ((fn () 42)) -> 42
        fn_expr = [Symbol("fn"), [], 42] # Changed Symbol("lambda") to Symbol("fn")
        call_expr = [fn_expr]
        self.assertEqual(evaluate(call_expr, self.env), 42)

    def test_fn_call_multiple_body_expressions(self): # Renamed test
        # ((fn (x) (define y x) (+ y 10)) 5) -> 15
        # The define y x will happen in the fn's call_env
        fn_expr = [
            Symbol("fn"), # Changed Symbol("lambda") to Symbol("fn")
            [Symbol("x")], 
            [Symbol("define"), Symbol("y"), Symbol("x")], # First body expr
            [Symbol("+"), Symbol("y"), 10]                # Second body expr (result)
        ]
        call_expr = [fn_expr, 5]
        self.assertEqual(evaluate(call_expr, self.env), 15)

    def test_fn_closure_captures_defining_env(self): # Renamed test
        # (define make-adder (fn (n) (fn (x) (+ x n))))
        # (define add5 (make-adder 5))
        # (add5 3) -> 8
        self.env.define("n_outer", 100) # Should not be used by add5 if closure is correct

        make_adder_params = [Symbol("n")]
        # Body of make-adder is a single expression: (fn (x) (+ x n))
        make_adder_body_expr = [Symbol("fn"), [Symbol("x")], [Symbol("+"), Symbol("x"), Symbol("n")]] # Changed Symbol("lambda") to Symbol("fn")
        
        define_make_adder_expr = [
            Symbol("define"), Symbol("make-adder"),
            [Symbol("fn"), make_adder_params, make_adder_body_expr] # Changed Symbol("lambda") to Symbol("fn")
        ]
        evaluate(define_make_adder_expr, self.env)

        add5_function = evaluate([Symbol("make-adder"), 5], self.env)
        self.assertIsInstance(add5_function, Function)
        self.env.define("add5", add5_function)

        result = evaluate([Symbol("add5"), 3], self.env)
        self.assertEqual(result, 8)

        add7_function = evaluate([Symbol("make-adder"), 7], self.env)
        self.env.define("add7", add7_function)
        result2 = evaluate([Symbol("add7"), 10], self.env)
        self.assertEqual(result2, 17)

    def test_fn_define_and_call(self): # Renamed test
        # (define my-add (fn (a b) (+ a b)))
        # (my-add 10 20) -> 30
        define_expr = [
            Symbol("define"), 
            Symbol("my-add"), 
            [Symbol("fn"), [Symbol("a"), Symbol("b")], [Symbol("+"), Symbol("a"), Symbol("b")]] # Changed Symbol("lambda") to Symbol("fn")
        ]
        evaluate(define_expr, self.env)
        
        call_expr = [Symbol("my-add"), 10, 20]
        self.assertEqual(evaluate(call_expr, self.env), 30)

    def test_fn_recursion_via_define(self): # Renamed test
        fact_fn_expr = [
            Symbol("fn"), [Symbol("n")], # Changed Symbol("lambda") to Symbol("fn")
            [Symbol("if"), [Symbol("<="), Symbol("n"), 1],
                1,
                [Symbol("*"), Symbol("n"), [Symbol("fact"), [Symbol("-"), Symbol("n"), 1]]]
            ]
        ]
        define_fact_expr = [Symbol("define"), Symbol("fact"), fact_fn_expr]
        evaluate(define_fact_expr, self.env)
        
        result = evaluate([Symbol("fact"), 5], self.env)
        self.assertEqual(result, 120)

    def test_fn_arity_error_too_few_args(self): # Renamed test
        fn_expr = [Symbol("fn"), [Symbol("x"), Symbol("y")], [Symbol("+"), Symbol("x"), Symbol("y")]]
        call_expr = [fn_expr, 1]
        with self.assertRaisesRegex(EvaluationError, r"ArityError:.* Function '\S+' expects 2 arguments, got 1\."):
            evaluate(call_expr, self.env)

    def test_fn_arity_error_too_many_args(self): # Renamed test
        fn_expr = [Symbol("fn"), [Symbol("x")], [Symbol("x")]]
        call_expr = [fn_expr, 1, 2]
        with self.assertRaisesRegex(EvaluationError, r"ArityError:.* Function '\S+' expects 1 arguments?, got 2\."):
            evaluate(call_expr, self.env)

    def test_fn_syntax_error_no_params_or_body(self): # Renamed test
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'fn' requires a parameter list and at least one body expression"):
            evaluate([Symbol("fn")], self.env) # Changed Symbol("lambda") to Symbol("fn")

    def test_fn_syntax_error_no_body(self): # Renamed test
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'fn' requires a parameter list and at least one body expression"):
            evaluate([Symbol("fn"), []], self.env) # Changed Symbol("lambda") to Symbol("fn")

    def test_fn_syntax_error_params_not_list(self): # Renamed test
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: Parameter list for 'fn' must be a list, got Symbol"):
            evaluate([Symbol("fn"), Symbol("x"), [Symbol("x")]], self.env) # Changed Symbol("lambda") to Symbol("fn")

    def test_fn_syntax_error_param_not_symbol(self): # Renamed test
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: All parameters in 'fn' parameter list must be symbols, got int: '123'"):
            evaluate([Symbol("fn"), [123], [Symbol("x")]], self.env) # Changed Symbol("lambda") to Symbol("fn")
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: All parameters in 'fn' parameter list must be symbols, got str: 'a-string'"):
            evaluate([Symbol("fn"), [Symbol("x"), "a-string"], [Symbol("x")]], self.env) # Changed Symbol("lambda") to Symbol("fn")

if __name__ == '__main__':
    unittest.main() 
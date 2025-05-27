# lispy_project/tests/special_forms/let_form_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from lispy.functions import create_global_env

class LetFormTest(unittest.TestCase):
    def setUp(self):
        self.global_env = create_global_env()

    def test_let_basic(self):
        code = "(let [x 1 y 2] (+ x y))"
        self.assertEqual(run_lispy_string(code, self.global_env), 3)

    def test_let_empty_bindings(self):
        code = "(let [] (+ 1 2))"
        self.assertEqual(run_lispy_string(code, self.global_env), 3)

    def test_let_sequential_body(self):
        code = "(let [x 1] (define y 2) (+ x y))" # define in let should modify let's env
        self.assertEqual(run_lispy_string(code, self.global_env), 3)

    def test_let_initializer_scope_let_star_behavior(self):
        """Test let* behavior: initializers can see previous bindings in the same let."""
        env = create_global_env()
        run_lispy_string("(define x 10)", env) # Outer x
        
        # y is initialized with the let-bound x (1), not the outer x (10)
        code = "(let [x 1 y x] y)"
        self.assertEqual(run_lispy_string(code, env), 1)
        
        # z is initialized with the let-bound y (which used let-bound x)
        code_sequential = "(let [x 1 y (+ x 1) z (+ y 1)] z)" # x=1, y=2, z=3
        self.assertEqual(run_lispy_string(code_sequential, env), 3)

    def test_let_initializer_still_sees_outer_scope_if_not_shadowed(self):
        env = create_global_env()
        run_lispy_string("(define outer_val 100)", env)
        code = "(let [x outer_val y (+ x 1)] y)" # x=100, y=101
        self.assertEqual(run_lispy_string(code, env), 101)

    def test_let_shadowing(self):
        env = create_global_env()
        run_lispy_string("(define x 100)", env)
        code = "(let [x 1] x)"
        self.assertEqual(run_lispy_string(code, env), 1)
        self.assertEqual(run_lispy_string("x", env), 100) # Outer x remains unchanged

    def test_let_nested(self):
        code = "(let [x 1] (let [y 2] (+ x y)))"
        self.assertEqual(run_lispy_string(code, self.global_env), 3)

    def test_let_nested_shadowing_let_star(self):
        # Inner let's y uses inner let's x (2)
        code = "(let [x 1] (let [x 2 y x] y))"
        self.assertEqual(run_lispy_string(code, self.global_env), 2)
        
        # Verify inner x value
        code_inner_x = "(let [x 1] (let [x 2 y x] x))"
        self.assertEqual(run_lispy_string(code_inner_x, self.global_env), 2)
        
        # Verify outer let's x is still accessible if not shadowed by inner let's init
        # (This is standard lexical scoping, let* only affects current binding block)
        code_outer_still_accessible = "(let [x 1 z x] (let [y (+ z 10)] y))" # x=1, z=1, y=11
        self.assertEqual(run_lispy_string(code_outer_still_accessible, self.global_env), 11)

    def test_let_access_outer_scope(self):
        env = create_global_env()
        run_lispy_string("(define z 30)", env)
        code = "(let [x 1] (+ x z))"
        self.assertEqual(run_lispy_string(code, env), 31)

    def test_let_syntax_error_main_form_too_short(self):
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'let' requires a bindings vector and at least one body expression."):
            run_lispy_string("(let [x 1])", self.global_env) # No body
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'let' requires a bindings vector and at least one body expression."):
            run_lispy_string("(let)", self.global_env) # No bindings, no body

    def test_let_syntax_error_bindings_not_vector(self):
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Bindings for 'let' must be a vector/list, got Symbol"):
            run_lispy_string("(let x (+ 1 2))", self.global_env)

    def test_let_syntax_error_odd_bindings_count(self):
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Bindings in 'let' must be in symbol-value pairs. Found an odd number of elements"):
            run_lispy_string("(let [x] (+ 1 2))", self.global_env)
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Bindings in 'let' must be in symbol-value pairs. Found an odd number of elements"):
            run_lispy_string("(let [x 1 y] (+ 1 2))", self.global_env)

    def test_let_syntax_error_binding_var_not_symbol(self):
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Variable in 'let' binding must be a symbol, got int: '1' at index 0"):
            run_lispy_string("(let [1 10] 1)", self.global_env)
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Variable in 'let' binding must be a symbol, got Vector: '\[Symbol\(\'a\'\) Symbol\(\'b\'\)\]' at index 0"):
            run_lispy_string("(let [[a b] 10] 1)", self.global_env) # Fixed typo: removed extra ] after 10
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: Variable in 'let' binding must be a symbol, got str: 'x' at index 0"):
            run_lispy_string('(let ["x" 1] 1)', self.global_env) # "x" is a string, not a symbol

    def test_let_define_interaction(self):
        """Test that define inside let modifies the let's environment."""
        code = "(let [x 1] (define y (+ x 1)) y)"
        self.assertEqual(run_lispy_string(code, self.global_env), 2)
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: y"):
            run_lispy_string("y", self.global_env)

    def test_let_lambda_interaction(self):
        """Test fn defined and used within a let."""
        code = "(let [x 10] ( (fn (y) (+ x y)) 5 ))"
        self.assertEqual(run_lispy_string(code, self.global_env), 15)

    def test_let_lambda_capture_let_vars(self):
        """Test that a fn captures variables from the let environment it's defined in."""
        code = "(let [x 10] (let [f (fn (y) (+ x y))] (f 5) ))"
        self.assertEqual(run_lispy_string(code, self.global_env), 15)

    def test_let_redefine_does_not_affect_outer(self):
        env = create_global_env()
        run_lispy_string("(define x 100)", env)
        run_lispy_string("(let [x 1] x)", env)
        self.assertEqual(run_lispy_string("x", env), 100)

if __name__ == '__main__':
    unittest.main() 
import unittest
from unittest.mock import Mock, MagicMock

from lispy.tail_call import TailCall, is_tail_position, is_function_call, is_recursive_call
from lispy.closure import Function
from lispy.types import Symbol
from lispy.environment import Environment
from lispy.exceptions import EvaluationError


class TailCallTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        
    def test_tail_call_creation(self):
        """Test TailCall object creation."""
        # Create a mock function
        mock_function = Mock(spec=Function)
        mock_function.params = ['x', 'y']
        mock_function.body = []
        
        args = [1, 2]
        tail_call = TailCall(mock_function, args)
        
        self.assertEqual(tail_call.function, mock_function)
        self.assertEqual(tail_call.args, args)
    
    def test_tail_call_repr(self):
        """Test TailCall string representation."""
        mock_function = Mock(spec=Function)
        mock_function.__repr__ = Mock(return_value="MockFunction")
        
        args = [1, 2, 3]
        tail_call = TailCall(mock_function, args)
        
        repr_str = repr(tail_call)
        self.assertIn("TailCall", repr_str)
        self.assertIn("[1, 2, 3]", repr_str)

    def test_tail_call_empty_args(self):
        """Test TailCall with empty arguments list."""
        mock_function = Mock(spec=Function)
        
        tail_call = TailCall(mock_function, [])
        
        self.assertEqual(tail_call.function, mock_function)
        self.assertEqual(tail_call.args, [])


class IsTailPositionTest(unittest.TestCase):
    def test_tail_position_single_expression(self):
        """Test tail position detection with single expression body."""
        # In a body with only 1 expression, index 0 is tail position
        self.assertTrue(is_tail_position(0, 1))
    
    def test_tail_position_multiple_expressions(self):
        """Test tail position detection with multiple expressions."""
        # In a body with 3 expressions, only index 2 is tail position
        self.assertFalse(is_tail_position(0, 3))
        self.assertFalse(is_tail_position(1, 3))
        self.assertTrue(is_tail_position(2, 3))
    
    def test_tail_position_empty_body(self):
        """Test tail position with empty body."""
        # Edge case: empty body
        self.assertFalse(is_tail_position(0, 0))
    
    def test_tail_position_large_body(self):
        """Test tail position with larger function body."""
        body_length = 10
        # Only the last expression is in tail position
        for i in range(body_length - 1):
            self.assertFalse(is_tail_position(i, body_length))
        self.assertTrue(is_tail_position(body_length - 1, body_length))
    
    def test_tail_position_edge_cases(self):
        """Test tail position edge cases."""
        # Negative index (invalid but test behavior)
        self.assertFalse(is_tail_position(-1, 3))
        
        # Index equal to body length (invalid but test behavior)
        self.assertFalse(is_tail_position(3, 3))
        
        # Index greater than body length (invalid but test behavior)
        self.assertFalse(is_tail_position(5, 3))


class IsFunctionCallTest(unittest.TestCase):
    def test_function_call_valid_list(self):
        """Test function call detection with valid function call forms."""
        # Non-empty list is a function call
        self.assertTrue(is_function_call([Symbol('+'), 1, 2]))
        self.assertTrue(is_function_call(['func']))
        self.assertTrue(is_function_call([Symbol('car'), [1, 2, 3]]))
    
    def test_function_call_empty_list(self):
        """Test function call detection with empty list."""
        # Empty list is not a function call
        self.assertFalse(is_function_call([]))
    
    def test_function_call_non_list_types(self):
        """Test function call detection with non-list types."""
        # Non-list types are not function calls
        self.assertFalse(is_function_call(42))
        self.assertFalse(is_function_call("string"))
        self.assertFalse(is_function_call(Symbol('symbol')))
        self.assertFalse(is_function_call(None))
        self.assertFalse(is_function_call(True))
        self.assertFalse(is_function_call({'key': 'value'}))
    
    def test_function_call_different_list_types(self):
        """Test function call detection with different list-like types."""
        # Regular Python list
        self.assertTrue(is_function_call([Symbol('+'), 1]))
        
        # Tuple (should not be considered a function call)
        self.assertFalse(is_function_call((Symbol('+'), 1)))
    
    def test_function_call_nested_structures(self):
        """Test function call detection with nested structures."""
        # Nested function calls
        nested_call = [Symbol('+'), [Symbol('*'), 2, 3], 4]
        self.assertTrue(is_function_call(nested_call))
        
        # Inner list is also a function call
        inner_call = nested_call[1]  # [Symbol('*'), 2, 3]
        self.assertTrue(is_function_call(inner_call))


class IsRecursiveCallTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        
    def test_recursive_call_same_function(self):
        """Test recursive call detection when calling the same function."""
        # Create a mock function
        mock_function = Mock(spec=Function)
        
        # Set up environment to return the same function when looking up 'factorial'
        self.env.define('factorial', mock_function)
        
        # Test expression: (factorial n)
        expr = [Symbol('factorial'), Symbol('n')]
        
        self.assertTrue(is_recursive_call(expr, mock_function, self.env))
    
    def test_recursive_call_different_function(self):
        """Test recursive call detection when calling a different function."""
        # Create two different mock functions
        current_function = Mock(spec=Function)
        other_function = Mock(spec=Function)
        
        # Set up environment to return different function
        self.env.define('other-func', other_function)
        
        # Test expression: (other-func n)
        expr = [Symbol('other-func'), Symbol('n')]
        
        self.assertFalse(is_recursive_call(expr, current_function, self.env))
    
    def test_recursive_call_non_function_call(self):
        """Test recursive call detection with non-function-call expressions."""
        mock_function = Mock(spec=Function)
        
        # Test with various non-function-call expressions
        self.assertFalse(is_recursive_call(42, mock_function, self.env))
        self.assertFalse(is_recursive_call("string", mock_function, self.env))
        self.assertFalse(is_recursive_call(Symbol('x'), mock_function, self.env))
        self.assertFalse(is_recursive_call([], mock_function, self.env))  # Empty list
    
    def test_recursive_call_lookup_error(self):
        """Test recursive call detection when symbol lookup fails."""
        mock_function = Mock(spec=Function)
        
        # Test expression with undefined symbol
        expr = [Symbol('undefined-function'), 1, 2]
        
        # Should return False when lookup fails
        self.assertFalse(is_recursive_call(expr, mock_function, self.env))
    
    def test_recursive_call_non_symbol_operator(self):
        """Test recursive call detection with non-symbol operator."""
        mock_function = Mock(spec=Function)
        
        # Test expression where operator is not a symbol
        expr = [42, 1, 2]  # Number as operator
        
        self.assertFalse(is_recursive_call(expr, mock_function, self.env))
        
        # Test with string as operator
        expr = ["string", 1, 2]
        
        self.assertFalse(is_recursive_call(expr, mock_function, self.env))
    
    def test_recursive_call_attribute_error(self):
        """Test recursive call detection when AttributeError occurs."""
        mock_function = Mock(spec=Function)
        
        # Create a symbol that doesn't have 'name' attribute somehow
        bad_symbol = Mock()
        bad_symbol.name = Mock(side_effect=AttributeError("No name"))
        
        expr = [bad_symbol, 1, 2]
        
        # Should return False when AttributeError occurs
        self.assertFalse(is_recursive_call(expr, mock_function, self.env))
    
    def test_recursive_call_with_parameters(self):
        """Test recursive call detection with various parameters."""
        mock_function = Mock(spec=Function)
        self.env.define('test-func', mock_function)
        
        # Test with multiple parameters
        expr = [Symbol('test-func'), Symbol('a'), Symbol('b'), 42, "string"]
        
        self.assertTrue(is_recursive_call(expr, mock_function, self.env))
    
    def test_recursive_call_symbol_identity(self):
        """Test that recursive call detection works with symbol identity."""
        function_a = Mock(spec=Function)
        function_b = Mock(spec=Function)
        
        # Both functions bound to same name (function_b shadows function_a)
        self.env.define('same-name', function_a)
        self.env.define('same-name', function_b)  # Overwrites previous binding
        
        expr = [Symbol('same-name'), 1]
        
        # Should be recursive for function_b but not function_a
        self.assertTrue(is_recursive_call(expr, function_b, self.env))
        self.assertFalse(is_recursive_call(expr, function_a, self.env))

    def test_recursive_call_nested_environments(self):
        """Test recursive call detection with nested environments."""
        outer_function = Mock(spec=Function)
        inner_function = Mock(spec=Function)
        
        # Set up outer environment
        outer_env = Environment()
        outer_env.define('func', outer_function)
        
        # Set up inner environment that shadows the outer function
        inner_env = Environment(outer=outer_env)
        inner_env.define('func', inner_function)
        
        expr = [Symbol('func'), 1]
        
        # Should find inner_function in inner environment
        self.assertTrue(is_recursive_call(expr, inner_function, inner_env))
        self.assertFalse(is_recursive_call(expr, outer_function, inner_env))


class IntegrationTest(unittest.TestCase):
    """Integration tests combining multiple tail call functions."""
    
    def test_tail_call_workflow(self):
        """Test a typical tail call optimization workflow."""
        # Create a mock function
        mock_function = Mock(spec=Function)
        mock_function.params = ['n', 'acc']
        
        # Set up environment
        env = Environment()
        env.define('factorial-helper', mock_function)
        
        # Simulate function body with multiple expressions
        body = [
            [Symbol('if'), [Symbol('='), Symbol('n'), 0], Symbol('acc')],
            [Symbol('factorial-helper'), [Symbol('-'), Symbol('n'), 1], [Symbol('*'), Symbol('n'), Symbol('acc')]]
        ]
        
        # Test tail position detection
        self.assertFalse(is_tail_position(0, len(body)))  # First expression not in tail position
        self.assertTrue(is_tail_position(1, len(body)))   # Last expression in tail position
        
        # Test if the tail expression is a function call
        tail_expr = body[1]
        self.assertTrue(is_function_call(tail_expr))
        
        # Test if it's a recursive call
        self.assertTrue(is_recursive_call(tail_expr, mock_function, env))
        
        # Create TailCall object for optimization
        args = [10, 1]  # Example arguments
        tail_call = TailCall(mock_function, args)
        
        self.assertEqual(tail_call.function, mock_function)
        self.assertEqual(tail_call.args, args)
    
    def test_non_tail_recursive_call(self):
        """Test detection of non-tail recursive calls."""
        mock_function = Mock(spec=Function)
        env = Environment()
        env.define('factorial', mock_function)
        
        # Non-tail recursive call: (* n (factorial (- n 1)))
        # The recursive call is not in tail position
        expr = [Symbol('*'), Symbol('n'), [Symbol('factorial'), [Symbol('-'), Symbol('n'), 1]]]
        
        # The whole expression is not a function call (it's multiplication)
        self.assertTrue(is_function_call(expr))
        self.assertFalse(is_recursive_call(expr, mock_function, env))
        
        # But the inner expression is a recursive call
        inner_expr = expr[2]  # [Symbol('factorial'), [Symbol('-'), Symbol('n'), 1]]
        self.assertTrue(is_function_call(inner_expr))
        self.assertTrue(is_recursive_call(inner_expr, mock_function, env))
        
        # However, it's not in tail position within a function body
        function_body = [expr]  # Single expression body
        self.assertTrue(is_tail_position(0, len(function_body)))  # The * expression is in tail position
        # But the recursive call within it is not the tail call
    
    def test_complex_conditional_tail_calls(self):
        """Test tail call detection in complex conditional expressions."""
        mock_function = Mock(spec=Function)
        env = Environment()
        env.define('complex-func', mock_function)
        
        # Function body with nested conditionals
        body = [
            [Symbol('define'), Symbol('temp'), Symbol('x')],  # Not tail position
            [Symbol('if'), Symbol('condition'),
                [Symbol('complex-func'), Symbol('a')],         # Tail call in then branch
                [Symbol('complex-func'), Symbol('b')]          # Tail call in else branch
            ]  # Tail position
        ]
        
        # The if expression is in tail position
        self.assertTrue(is_tail_position(1, len(body)))
        
        if_expr = body[1]
        then_branch = if_expr[2]
        else_branch = if_expr[3]
        
        # Both branches contain function calls
        self.assertTrue(is_function_call(then_branch))
        self.assertTrue(is_function_call(else_branch))
        
        # Both are recursive calls
        self.assertTrue(is_recursive_call(then_branch, mock_function, env))
        self.assertTrue(is_recursive_call(else_branch, mock_function, env))


if __name__ == "__main__":
    unittest.main() 
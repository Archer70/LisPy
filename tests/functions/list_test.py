# tests/functions/list_test.py
import unittest

from lispy.functions import global_env, create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError # Though list itself may not raise, its args might
from lispy.types import Symbol

class ListFunctionTest(unittest.TestCase):

    def setUp(self):
        self.env = create_global_env() # Use a fresh env to ensure 'list' is defined

    def test_list_empty(self):
        self.assertEqual(run_lispy_string("(list)", self.env), [])

    def test_list_with_numbers(self):
        self.assertEqual(run_lispy_string("(list 1 2 3)", self.env), [1, 2, 3])

    def test_list_with_strings(self):
        self.assertEqual(run_lispy_string('(list "a" "b" "c")', self.env), ["a", "b", "c"])

    def test_list_with_mixed_types(self):
        expected_list = [1, "hello", True, None, Symbol('sym')]
        # Define sym for the run_lispy_string context if needed, or quote it
        # For (list 1 "hello" true nil 'sym), 'sym needs to be quoted or defined
        # Or, if Symbol('sym') is the direct result of some evaluation, that's fine.
        # Let's test with literals primarily, as list just constructs from evaluated args.
        self.assertEqual(run_lispy_string("(list 1 \"hello\" true nil 'sym)", self.env), expected_list)

    def test_list_with_nested_lists(self):
        # (list (list 1 2) (list 3 4)) -> [[1,2], [3,4]]
        self.assertEqual(run_lispy_string("(list (list 1 2) (list 3 4))", self.env), [[1, 2], [3, 4]])

    def test_list_with_nested_calls(self):
        self.assertEqual(run_lispy_string("(list (+ 1 2) (* 2 3))", self.env), [3, 6])

    def test_list_with_nil_and_booleans(self):
        self.assertEqual(run_lispy_string("(list nil true false)", self.env), [None, True, False])

if __name__ == '__main__':
    unittest.main() 
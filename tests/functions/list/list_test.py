# tests/functions/list_test.py
import unittest

from lispy.functions import create_global_env
from lispy.types import LispyList, Symbol
from lispy.utils import run_lispy_string


class ListFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()  # Use a fresh env to ensure 'list' is defined

    def test_list_empty(self):
        result = run_lispy_string("(list)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([]))

    def test_list_with_numbers(self):
        result = run_lispy_string("(list 1 2 3)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([1, 2, 3]))

    def test_list_with_strings(self):
        result = run_lispy_string('(list "a" "b" "c")', self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList(["a", "b", "c"]))

    def test_list_with_mixed_types(self):
        expected_list = LispyList([1, "hello", True, None, Symbol("sym")])
        # Define sym for the run_lispy_string context if needed, or quote it
        # For (list 1 "hello" true nil 'sym), 'sym needs to be quoted or defined
        # Or, if Symbol('sym') is the direct result of some evaluation, that's fine.
        # Let's test with literals primarily, as list just constructs from evaluated args.
        result = run_lispy_string('(list 1 "hello" true nil \'sym)', self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, expected_list)

    def test_list_with_nested_lists(self):
        # (list (list 1 2) (list 3 4)) -> [[1,2], [3,4]]
        result = run_lispy_string("(list (list 1 2) (list 3 4))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([LispyList([1, 2]), LispyList([3, 4])]))

    def test_list_with_nested_calls(self):
        result = run_lispy_string("(list (+ 1 2) (* 2 3))", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([3, 6]))

    def test_list_with_nil_and_booleans(self):
        result = run_lispy_string("(list nil true false)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([None, True, False]))


if __name__ == "__main__":
    unittest.main()

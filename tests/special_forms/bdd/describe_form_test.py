import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class TestDescribeForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_describe_basic_structure(self):
        # For now, let's assume `describe` evaluates its body and returns the last result.
        # The main effect is registering the description and its scenarios.
        # (print "hello") returns None in LisPy.
        result = run_lispy_string('(describe "A feature" (print "hello"))', self.env)
        self.assertIsNone(result)

    def test_describe_no_body(self):
        result = run_lispy_string('(describe "Another feature")', self.env)
        self.assertIsNone(result)

    def test_describe_arity_error_no_args(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(describe)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'describe' expects at least a description string, got 0 arguments."
        )

    def test_describe_arity_error_no_description_string(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(describe (print "uh oh"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'describe' expects a description string as its first argument."
        )

if __name__ == '__main__':
    unittest.main() 
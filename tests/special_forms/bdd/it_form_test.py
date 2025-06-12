# tests/special_forms/bdd/it_form_test.py
import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry


class TestItForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results()

    def helper_run_in_feature_context(self, code_string):
        registry.start_feature("Test Feature for 'it'")
        try:
            result = run_lispy_string(code_string, self.env)
        finally:
            registry.end_feature()
        return result

    def test_it_basic_structure_with_body(self):
        # (it "should perform an action" (print "action-performed"))
        # `print` returns None, so `it` should return None.
        result = self.helper_run_in_feature_context(
            '(it "should perform an action" nil)'
        )
        self.assertIsNone(result)

    def test_it_no_body(self):
        # (it "should have no body")
        result = self.helper_run_in_feature_context('(it "should have no body")')
        self.assertIsNone(result)

    def test_it_arity_error_no_args(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_feature_context("(it)")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'it' expects at least a description string, got 0 arguments.",
        )

    def test_it_arity_error_no_description_string(self):
        # (it (print "oops"))
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_feature_context('(it (print "oops"))')
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'it' expects a description string as its first argument.",
        )

    def test_it_description_not_a_string(self):
        # (it 123 (print "oops"))
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_feature_context('(it 123 (print "oops"))')
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'it' expects a description string as its first argument.",
        )

    def test_it_outside_describe_block(self):
        # This test specifically checks behavior WITHOUT feature context
        # registry.clear_bdd_results() is already called in setUp
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(it "should fail" (print "test"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'it' form can only be used inside a 'describe' block.",
        )


if __name__ == "__main__":
    unittest.main()

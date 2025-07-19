"""LisPy BDD Assertion Functions"""

from .assert_equal_q_fn import assert_equal_q, assert_equal_q_doc
from .assert_true_q_fn import assert_true_q, assert_true_q_doc
from .assert_false_q_fn import assert_false_q, assert_false_q_doc
from .assert_nil_q_fn import assert_nil_q, assert_nil_q_doc
from .assert_not_nil_q_fn import bdd_assert_not_nil_q, documentation_assert_not_nil_q

# This dictionary will be merged into the global environment
bdd_assertion_functions = {
    "assert-equal?": assert_equal_q,
    "assert-true?": assert_true_q,
    "assert-false?": assert_false_q,
    "assert-nil?": assert_nil_q,
    "assert-not-nil?": bdd_assert_not_nil_q,
}

__all__ = ["bdd_assertion_functions"]

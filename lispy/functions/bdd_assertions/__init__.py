"""LisPy BDD Assertion Functions"""

from .assert_equal_q_fn import bdd_assert_equal_q
from .assert_true_q_fn import bdd_assert_true_q
from .assert_false_q_fn import bdd_assert_false_q
from .assert_nil_q_fn import bdd_assert_nil_q
from .assert_not_nil_q_fn import bdd_assert_not_nil_q

# This dictionary will be merged into the global environment
bdd_assertion_functions = {
    "assert-equal?": bdd_assert_equal_q,
    "assert-true?": bdd_assert_true_q,
    "assert-false?": bdd_assert_false_q,
    "assert-nil?": bdd_assert_nil_q,
    "assert-not-nil?": bdd_assert_not_nil_q,
}

__all__ = ["bdd_assertion_functions"] 
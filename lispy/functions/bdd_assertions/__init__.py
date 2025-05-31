"""LisPy BDD Assertion Functions"""

from .assert_equal_q_fn import bdd_assert_equal_q

# This dictionary will be merged into the global environment
bdd_assertion_functions = {
    "assert-equal?": bdd_assert_equal_q,
}

__all__ = ["bdd_assertion_functions"] 
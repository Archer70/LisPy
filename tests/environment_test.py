import unittest

from lispy.environment import Environment
from lispy.exceptions import EvaluationError  # For checking expected errors


class EnvironmentTest(unittest.TestCase):
    def test_define_and_lookup_simple(self):
        env = Environment()
        env.define("x", 100)
        self.assertEqual(env.lookup("x"), 100)
        env.define("message", "hello")
        self.assertEqual(env.lookup("message"), "hello")

    def test_lookup_unbound_symbol_simple(self):
        env = Environment()
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: y"):
            env.lookup("y")

    def test_lookup_from_outer_environment(self):
        outer_env = Environment()
        outer_env.define("a", 10)
        inner_env = Environment(outer=outer_env)
        self.assertEqual(inner_env.lookup("a"), 10)

    def test_shadowing_in_inner_environment(self):
        outer_env = Environment()
        outer_env.define("x", "outer_x")
        inner_env = Environment(outer=outer_env)
        inner_env.define("x", "inner_x")  # Shadows outer_env's x

        self.assertEqual(inner_env.lookup("x"), "inner_x")
        # To verify outer_env is not affected, we'd ideally look it up there directly.
        # For now, this structure assumes lookup in outer_env itself still works.
        self.assertEqual(outer_env.lookup("x"), "outer_x")

    def test_lookup_unbound_through_outer(self):
        outer_env = Environment()
        outer_env.define("only_in_outer", "value")
        inner_env = Environment(outer=outer_env)
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: not_found"):
            inner_env.lookup("not_found")

    def test_define_does_not_affect_outer(self):
        outer_env = Environment()
        outer_env.define("y", 30)

        inner_env = Environment(outer=outer_env)
        inner_env.define("z", 40)  # New symbol in inner
        inner_env.define("y", 50)  # Shadowing y in inner

        self.assertEqual(inner_env.lookup("z"), 40)
        self.assertEqual(inner_env.lookup("y"), 50)

        # Check outer environment remains unchanged
        self.assertEqual(outer_env.lookup("y"), 30)
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: z"):
            outer_env.lookup("z")  # z should not be in outer


if __name__ == "__main__":
    unittest.main()

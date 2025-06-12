import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import Symbol


class MergeFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_merge_empty_args(self):
        """Test (merge) returns {}."""
        result = run_lispy_string("(merge)", self.env)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_merge_single_map(self):
        """Test (merge {:a 1 :b 2}) returns {:a 1 :b 2}."""
        result = run_lispy_string("(merge (hash-map ':a 1 ':b 2))", self.env)
        self.assertIsInstance(result, dict)
        expected = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected)

    def test_merge_two_maps_no_overlap(self):
        """Test merging two maps with no overlapping keys."""
        result = run_lispy_string("(merge (hash-map ':a 1) (hash-map ':b 2))", self.env)
        self.assertIsInstance(result, dict)
        expected = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected)

    def test_merge_two_maps_with_overlap(self):
        """Test merging two maps where later map overrides earlier keys."""
        result = run_lispy_string(
            "(merge (hash-map ':a 1 ':b 2) (hash-map ':a 3 ':c 4))", self.env
        )
        self.assertIsInstance(result, dict)
        expected = {Symbol(":a"): 3, Symbol(":b"): 2, Symbol(":c"): 4}
        self.assertEqual(result, expected)

    def test_merge_multiple_maps(self):
        """Test merging three maps with various overlaps."""
        lispy_code = "(merge (hash-map ':a 1 ':b 2) (hash-map ':b 3 ':c 4) (hash-map ':c 5 ':d 6))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected = {
            Symbol(":a"): 1,
            Symbol(":b"): 3,  # Overridden by second map
            Symbol(":c"): 5,  # Overridden by third map
            Symbol(":d"): 6,
        }
        self.assertEqual(result, expected)

    def test_merge_empty_maps(self):
        """Test merging empty maps."""
        result = run_lispy_string("(merge (hash-map) (hash-map) (hash-map))", self.env)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_merge_with_empty_map(self):
        """Test merging maps where some are empty."""
        result = run_lispy_string(
            "(merge (hash-map ':a 1) (hash-map) (hash-map ':b 2))", self.env
        )
        self.assertIsInstance(result, dict)
        expected = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected)

    def test_merge_mixed_value_types(self):
        """Test merge with different value types."""
        lispy_code = "(merge (hash-map ':name \"LisPy\" ':version 1) (hash-map ':active true ':version 2.0))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected = {
            Symbol(":name"): "LisPy",
            Symbol(":version"): 2.0,  # Overridden
            Symbol(":active"): True,
        }
        self.assertEqual(result, expected)

    def test_merge_preserves_original_maps(self):
        """Test that merge does not mutate the original maps."""
        run_lispy_string("(define map1 (hash-map ':a 1 ':b 2))", self.env)
        run_lispy_string("(define map2 (hash-map ':a 3 ':c 4))", self.env)
        run_lispy_string("(merge map1 map2)", self.env)

        # Check that original maps are unchanged
        original_map1 = run_lispy_string("map1", self.env)
        original_map2 = run_lispy_string("map2", self.env)

        expected_map1 = {Symbol(":a"): 1, Symbol(":b"): 2}
        expected_map2 = {Symbol(":a"): 3, Symbol(":c"): 4}

        self.assertEqual(original_map1, expected_map1)
        self.assertEqual(original_map2, expected_map2)

    def test_merge_large_number_of_maps(self):
        """Test merge with many maps."""
        # Create multiple maps with overlapping keys
        lispy_code = """(merge 
                          (hash-map ':shared 1 ':a 1) 
                          (hash-map ':shared 2 ':b 2) 
                          (hash-map ':shared 3 ':c 3) 
                          (hash-map ':shared 4 ':d 4))"""
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected = {
            Symbol(":shared"): 4,  # Last value wins
            Symbol(":a"): 1,
            Symbol(":b"): 2,
            Symbol(":c"): 3,
            Symbol(":d"): 4,
        }
        self.assertEqual(result, expected)

    # --- Error Handling Tests ---
    def test_merge_invalid_argument_type(self):
        """Test merge with non-hash-map arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(merge [1 2 3])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'merge' arguments must be hash maps, got <class 'lispy.types.Vector'> at position 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(merge (hash-map \':a 1) "not-a-map")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'merge' arguments must be hash maps, got <class 'str'> at position 1.",
        )

    def test_merge_mixed_valid_invalid_args(self):
        """Test merge with mix of valid and invalid arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(merge (hash-map ':a 1) (hash-map ':b 2) 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'merge' arguments must be hash maps, got <class 'int'> at position 2.",
        )

    def test_merge_with_thread_first(self):
        """Test merge used with the -> (thread-first) special form."""
        result = run_lispy_string(
            "(-> (hash-map ':a 1) (merge (hash-map ':b 2) (hash-map ':c 3)))", self.env
        )
        self.assertIsInstance(result, dict)
        expected = {Symbol(":a"): 1, Symbol(":b"): 2, Symbol(":c"): 3}
        self.assertEqual(result, expected)

    def test_merge_override_with_thread_first(self):
        """Test merge with key override via thread-first."""
        result = run_lispy_string(
            "(-> (hash-map ':key 'original) (merge (hash-map ':key 'override)))",
            self.env,
        )
        self.assertIsInstance(result, dict)
        expected = {Symbol(":key"): Symbol("override")}
        self.assertEqual(result, expected)

    def test_merge_chaining_with_thread_first(self):
        """Test chaining merge with other operations via thread-first."""
        # This would require additional functions to work with hash maps in a chain
        # For now, just test that merge works in a thread-first context
        result = run_lispy_string(
            "(-> (hash-map ':base 1) (merge (hash-map ':extra 2)))", self.env
        )
        self.assertIsInstance(result, dict)
        expected = {Symbol(":base"): 1, Symbol(":extra"): 2}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

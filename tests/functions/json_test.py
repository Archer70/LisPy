import unittest
from lispy.functions import create_global_env
from lispy.types import Symbol, Vector, LispyList
from lispy.exceptions import LisPyError
from lispy.utils import run_lispy_string


class TestJSONFunctions(unittest.TestCase):
    """Test JSON encoding and decoding functions."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_json_encode_primitives(self):
        """Test encoding primitive data types."""
        # None/nil
        result = run_lispy_string('(json-encode nil)', self.env)
        self.assertEqual(result, "null")
        
        # Numbers
        result = run_lispy_string('(json-encode 42)', self.env)
        self.assertEqual(result, "42")
        
        result = run_lispy_string('(json-encode 3.14)', self.env)
        self.assertEqual(result, "3.14")
        
        # Booleans
        result = run_lispy_string('(json-encode true)', self.env)
        self.assertEqual(result, "true")
        
        result = run_lispy_string('(json-encode false)', self.env)
        self.assertEqual(result, "false")
        
        # Strings
        result = run_lispy_string('(json-encode "hello")', self.env)
        self.assertEqual(result, '"hello"')

    def test_json_encode_symbols(self):
        """Test encoding symbols to strings."""
        # Regular symbol
        result = run_lispy_string('(json-encode (quote test))', self.env)
        self.assertEqual(result, '"test"')
        
        # Keyword symbol (with colon)
        result = run_lispy_string('(json-encode (quote :status))', self.env)
        self.assertEqual(result, '"status"')

    def test_json_encode_collections(self):
        """Test encoding collections (lists, vectors)."""
        # Vector
        result = run_lispy_string('(json-encode [1 2 3])', self.env)
        self.assertEqual(result, "[1, 2, 3]")
        
        # List
        result = run_lispy_string('(json-encode (list 1 2 3))', self.env)
        self.assertEqual(result, "[1, 2, 3]")

    def test_json_encode_maps(self):
        """Test encoding maps/dictionaries."""
        # Simple map (using hash-map with symbol keys that represent strings)
        result = run_lispy_string('(json-encode (hash-map (quote name) "Alice" (quote age) 30))', self.env)
        self.assertIn('"name": "Alice"', result)
        self.assertIn('"age": 30', result)
        
        # Map with symbol keys
        result = run_lispy_string('(json-encode {:name "Alice" :age 30})', self.env)
        self.assertIn('"name": "Alice"', result)
        self.assertIn('"age": 30', result)

    def test_json_encode_nested_structures(self):
        """Test encoding complex nested structures."""
        lispy_code = '''(json-encode {:users [{:name "Alice" :age 30}
                                             {:name "Bob" :age 25}]
                                     :active true})'''
        result = run_lispy_string(lispy_code, self.env)
        
        # Should contain all the data
        self.assertIn('"users"', result)
        self.assertIn('"Alice"', result)
        self.assertIn('"Bob"', result)
        self.assertIn('"active": true', result)

    def test_json_encode_arity_error(self):
        """Test arity error for json-encode."""
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-encode)', self.env)
        self.assertIn("expects exactly 1 argument", str(context.exception))
        
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-encode 1 2)', self.env)
        self.assertIn("expects exactly 1 argument", str(context.exception))

    def test_json_decode_primitives(self):
        """Test decoding primitive JSON values."""
        # null
        result = run_lispy_string('(json-decode "null")', self.env)
        self.assertIsNone(result)
        
        # Numbers
        result = run_lispy_string('(json-decode "42")', self.env)
        self.assertEqual(result, 42)
        
        result = run_lispy_string('(json-decode "3.14")', self.env)
        self.assertEqual(result, 3.14)
        
        # Booleans
        result = run_lispy_string('(json-decode "true")', self.env)
        self.assertEqual(result, True)
        
        result = run_lispy_string('(json-decode "false")', self.env)
        self.assertEqual(result, False)
        
        # Strings
        result = run_lispy_string('(json-decode "\\"hello\\"")', self.env)
        self.assertEqual(result, "hello")

    def test_json_decode_arrays(self):
        """Test decoding JSON arrays to vectors."""
        result = run_lispy_string('(json-decode "[1, 2, 3]")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(list(result), [1, 2, 3])
        
        # Empty array
        result = run_lispy_string('(json-decode "[]")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(list(result), [])

    def test_json_decode_objects(self):
        """Test decoding JSON objects to maps with keyword keys."""
        result = run_lispy_string('(json-decode "{\\"name\\": \\"Alice\\", \\"age\\": 30}")', self.env)
        
        self.assertIsInstance(result, dict)
        self.assertIn(Symbol(":name"), result)
        self.assertIn(Symbol(":age"), result)
        self.assertEqual(result[Symbol(":name")], "Alice")
        self.assertEqual(result[Symbol(":age")], 30)

    def test_json_decode_nested_structures(self):
        """Test decoding complex nested JSON."""
        json_str = '"{\\"users\\": [{\\"name\\": \\"Alice\\", \\"age\\": 30}], \\"active\\": true}"'
        result = run_lispy_string(f'(json-decode {json_str})', self.env)
        
        self.assertIsInstance(result, dict)
        self.assertIn(Symbol(":users"), result)
        self.assertIn(Symbol(":active"), result)
        
        users = result[Symbol(":users")]
        self.assertIsInstance(users, Vector)
        self.assertEqual(len(users), 1)
        
        user = users[0]
        self.assertIsInstance(user, dict)
        self.assertEqual(user[Symbol(":name")], "Alice")
        self.assertEqual(user[Symbol(":age")], 30)

    def test_json_decode_invalid_json(self):
        """Test error handling for invalid JSON."""
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-decode "invalid json")', self.env)
        self.assertIn("Invalid JSON", str(context.exception))
        
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-decode "{broken: json}")', self.env)
        self.assertIn("Invalid JSON", str(context.exception))

    def test_json_decode_arity_error(self):
        """Test arity error for json-decode."""
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-decode)', self.env)
        self.assertIn("expects exactly 1 argument", str(context.exception))
        
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-decode "test" "extra")', self.env)
        self.assertIn("expects exactly 1 argument", str(context.exception))

    def test_json_decode_non_string_input(self):
        """Test error for non-string input to json-decode."""
        with self.assertRaises(LisPyError) as context:
            run_lispy_string('(json-decode 42)', self.env)
        self.assertIn("expects a string", str(context.exception))

    def test_json_roundtrip(self):
        """Test encoding then decoding returns equivalent data."""
        # First encode some data
        encoded_result = run_lispy_string('''(json-encode {:name "Alice"
                                                          :age 30
                                                          :hobbies ["reading" "coding"]
                                                          :active true
                                                          :metadata nil})''', self.env)
        self.assertIsInstance(encoded_result, str)
        
        # Then decode it back
        decoded_result = run_lispy_string(f'(json-decode "{encoded_result.replace('"', '\\"')}")', self.env)
        
        # Should have the same structure (though vectors might not be identical objects)
        self.assertEqual(decoded_result[Symbol(":name")], "Alice")
        self.assertEqual(decoded_result[Symbol(":age")], 30)
        self.assertEqual(list(decoded_result[Symbol(":hobbies")]), ["reading", "coding"])
        self.assertEqual(decoded_result[Symbol(":active")], True)
        self.assertIsNone(decoded_result[Symbol(":metadata")])

    def test_json_functions_in_global_env(self):
        """Test that JSON functions are available in global environment."""
        self.assertIn("json-encode", self.env.store)
        self.assertIn("json-decode", self.env.store)
        
        # Test they work through the environment
        result = run_lispy_string('(json-encode {:test 123})', self.env)
        self.assertIn('"test"', result)
        self.assertIn('123', result)
        
        result = run_lispy_string('(json-decode "{\\"test\\": 123}")', self.env)
        self.assertEqual(result[Symbol(":test")], 123)

    def test_json_empty_collections(self):
        """Test encoding/decoding empty collections."""
        # Empty vector
        result = run_lispy_string('(json-encode [])', self.env)
        self.assertEqual(result, "[]")
        
        # Empty dict
        result = run_lispy_string('(json-encode {})', self.env)
        self.assertEqual(result, "{}")
        
        # Decode empty structures
        result = run_lispy_string('(json-decode "[]")', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(len(result), 0)
        
        result = run_lispy_string('(json-decode "{}")', self.env)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main() 
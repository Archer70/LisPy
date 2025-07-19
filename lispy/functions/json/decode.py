"""
JSON decoding function for LisPy.

Converts JSON strings to LisPy data structures.
"""

import json
from typing import List, Any
from lispy.exceptions import LisPyError, EvaluationError
from lispy.types import Symbol, Vector
from lispy.environment import Environment
from ..decorators import lispy_function, lispy_documentation


class JSONDecodeError(LisPyError):
    """Exception raised for JSON decoding errors."""
    pass


@lispy_function("json-decode")
def json_decode(args: List[Any], env: Environment) -> Any:
    """
    Decode a JSON string to LisPy data.
    
    Args:
        args: List containing one argument - the JSON string to decode
        env: Environment (unused)
        
    Returns:
        Decoded LisPy data structure
        
    Raises:
        EvaluationError: If JSON string is invalid or cannot be decoded
    """
    if len(args) != 1:
        raise EvaluationError(f"ArgumentError: 'json-decode' expects exactly 1 argument, got {len(args)}")
    
    json_string = args[0]
    
    if not isinstance(json_string, str):
        raise EvaluationError(f"TypeError: 'json-decode' expects a string, got {type(json_string).__name__}")
    
    try:
        # Parse JSON string
        parsed_data = json.loads(json_string)
        
        # Convert to LisPy data structures
        return _convert_from_json(parsed_data)
        
    except json.JSONDecodeError as e:
        raise EvaluationError(f"ParseError: Invalid JSON: {str(e)}")
    except Exception as e:
        raise EvaluationError(f"DecodeError: JSON decode error: {str(e)}")


def _convert_from_json(value):
    """
    Convert JSON-parsed Python values to LisPy data structures.
    
    Args:
        value: Value from json.loads()
        
    Returns:
        LisPy-compatible value with appropriate types
    """
    if isinstance(value, dict):
        # Convert objects to LisPy maps with Symbol keys
        result = {}
        for k, v in value.items():
            # Convert string keys to keyword symbols
            if isinstance(k, str):
                key_symbol = Symbol(f":{k}")
            else:
                key_symbol = Symbol(f":{str(k)}")
            
            result[key_symbol] = _convert_from_json(v)
        return result
        
    elif isinstance(value, list):
        # Convert arrays to LisPy vectors
        converted_items = [_convert_from_json(item) for item in value]
        return Vector(converted_items)
        
    else:
        # Primitives (str, int, float, bool, None) are already compatible
        return value


@lispy_documentation("json-decode")
def json_decode_doc():
    return """
json-decode: Convert JSON string to LisPy data

Usage:
  (json-decode json-string)

Arguments:
  json-string - String containing valid JSON

Returns:
  LisPy data structure corresponding to the JSON

JSON to LisPy Conversions:
  - null          → nil
  - numbers       → numbers (42, 3.14)
  - booleans      → booleans (true, false)
  - strings       → strings ("hello")
  - arrays        → vectors ([1 2 3])
  - objects       → maps with keyword keys ({:name "Alice"})

Examples:
  ; Primitives
  (json-decode "null")       ; → nil
  (json-decode "42")         ; → 42
  (json-decode "true")       ; → true
  (json-decode "\\"hello\\"")   ; → "hello"
  
  ; Collections
  (json-decode "[1,2,3]")                    ; → [1 2 3]
  (json-decode "{\\"name\\":\\"Alice\\"}")       ; → {:name "Alice"}
  
  ; Nested structures
  (json-decode "{\\"users\\":[{\\"name\\":\\"Alice\\",\\"age\\":30}]}")
  ; → {:users [{:name "Alice" :age 30}]}
  
  ; Working with HTTP responses
  (define response (await (http-get "https://api.example.com/users")))
  (define users (json-decode (get response :body)))

Notes:
  - Object keys become keyword symbols (prefixed with :)
  - Arrays become vectors (not lists)
  - Nested structures are recursively converted
  - Invalid JSON raises ParseError
  - Whitespace in JSON is ignored (standard JSON parsing)

Error Handling:
  (try
    (json-decode "invalid json")
    (catch ParseError e
      (println "Parse error:" e)))

See also: json-encode for the reverse operation
""" 
"""
JSON encoding function for LisPy.

Converts LisPy data structures to JSON strings.
"""

import json
from lispy.exceptions import LisPyError
from lispy.types import Symbol, Vector, LispyList


class JSONEncodeError(LisPyError):
    """Exception raised for JSON encoding errors."""
    pass


def builtin_json_encode(args, env):
    """
    Encode LisPy data as a JSON string.
    
    Args:
        args: List containing one argument - the data to encode
        env: Environment (unused)
        
    Returns:
        str: JSON string representation of the data
        
    Raises:
        JSONEncodeError: If data cannot be encoded as JSON
    """
    if len(args) != 1:
        raise JSONEncodeError(f"json-encode expects exactly 1 argument, got {len(args)}")
    
    data = args[0]
    
    try:
        # Convert LisPy data to JSON-compatible format
        json_compatible = _convert_for_json(data)
        
        # Encode as JSON string
        return json.dumps(json_compatible)
        
    except (TypeError, ValueError) as e:
        raise JSONEncodeError(f"Cannot encode as JSON: {str(e)}")


def _convert_for_json(value):
    """
    Convert LisPy values to JSON-compatible Python values.
    
    Args:
        value: Value to convert
        
    Returns:
        JSON-compatible value (dict, list, str, int, float, bool, None)
    """
    if isinstance(value, Symbol):
        # Convert symbols to strings (removing leading colon if present)
        symbol_name = value.name
        return symbol_name[1:] if symbol_name.startswith(':') else symbol_name
        
    elif isinstance(value, (list, Vector, LispyList)):
        # Recursively convert list/vector elements
        return [_convert_for_json(item) for item in value]
        
    elif isinstance(value, dict):
        # Recursively convert dictionary values and normalize keys
        result = {}
        for k, v in value.items():
            # Convert keys to strings
            if isinstance(k, Symbol):
                str_key = k.name
                if str_key.startswith(':'):
                    str_key = str_key[1:]
            else:
                str_key = str(k)
            
            result[str_key] = _convert_for_json(v)
        return result
        
    elif value is None:
        # None becomes JSON null
        return None
        
    elif isinstance(value, (int, float, bool, str)):
        # Primitives are already JSON-compatible
        return value
        
    else:
        # For other types, convert to string representation
        # This includes functions, promises, etc.
        return str(value)


# Documentation
documentation_json_encode = """
json-encode: Convert LisPy data to JSON string

Usage:
  (json-encode data)

Arguments:
  data - LisPy data to encode as JSON

Returns:
  String containing JSON representation of the data

Supported Data Types:
  - nil           → null
  - Numbers       → numbers (42, 3.14)
  - Booleans      → booleans (true, false)
  - Strings       → strings ("hello")
  - Symbols       → strings (removes leading colon from keywords)
  - Vectors/Lists → arrays ([1, 2, 3])
  - Maps          → objects ({"key": "value"})
  - Nested data   → recursively converted

Examples:
  ; Primitives
  (json-encode nil)        ; → "null"
  (json-encode 42)         ; → "42"
  (json-encode true)       ; → "true"
  (json-encode "hello")    ; → "\\"hello\\""
  
  ; Collections
  (json-encode [1 2 3])            ; → "[1,2,3]"
  (json-encode {:name "Alice"})     ; → "{\\"name\\":\\"Alice\\"}"
  
  ; Nested structures
  (json-encode {:users [{:name "Alice" :age 30}
                        {:name "Bob" :age 25}]})
  
  ; Keywords become strings (colon removed)
  (json-encode {:status :success})  ; → "{\\"status\\":\\"success\\"}"

Notes:
  - Symbols/keywords have leading colons removed
  - Functions and other non-JSON types become string representations
  - Circular references will cause infinite recursion
  - Output is compact (no pretty-printing)

See also: json-decode for the reverse operation
""" 
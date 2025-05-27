from lispy.types import Symbol
from lispy.exceptions import EvaluationError

def builtin_dissoc(args):
    """Removes keys from a map.
    (dissoc map key & keys)
    Behaves like Clojure's dissoc.
    """
    if not args:
        raise EvaluationError("SyntaxError: 'dissoc' expects at least 1 argument (map), got 0.")

    target_map, *keys = args

    if target_map is None:
        return None

    if not isinstance(target_map, dict):
        raise EvaluationError(f"TypeError: First argument to 'dissoc' must be a map or nil, got {type(target_map)}.")

    if not keys:
        return target_map.copy()

    new_map = target_map.copy()
    for key_to_remove in keys:
        if not isinstance(key_to_remove, Symbol):
            raise EvaluationError(f"TypeError: Keys to 'dissoc' must be symbols, got {type(key_to_remove)}.")
        if key_to_remove in new_map:
            del new_map[key_to_remove]
    return new_map 
from lispy.exceptions import EvaluationError


def merge_fn(args, env):
    """Merge multiple hash maps into a single hash map.

    Usage: (merge map1 map2 ...)

    Args:
        map1, map2, ...: Hash maps to merge

    Returns:
        A new hash map containing all key-value pairs from the input maps.
        Later arguments override earlier ones for duplicate keys.

    Examples:
        (merge {:a 1} {:b 2}) => {:a 1 :b 2}
        (merge {:a 1} {:a 2 :b 3}) => {:a 2 :b 3}  ; Later :a overrides
        (merge) => {}  ; Empty merge returns empty map
    """
    if len(args) == 0:
        # Empty merge returns empty hash map
        return {}

    # Validate all arguments are hash maps
    for i, arg in enumerate(args):
        if not isinstance(arg, dict):
            raise EvaluationError(
                f"TypeError: 'merge' arguments must be hash maps, got {type(arg)} at position {i}."
            )

    # Merge all maps, with later ones overriding earlier ones
    result_map = {}
    for hash_map in args:
        result_map.update(hash_map)

    return result_map

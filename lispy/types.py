# LisPy Custom Types


class Symbol:
    """Represents a Lisp symbol."""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Symbol('{self.name}')"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        return False

    def __hash__(self):
        # Symbols are hashable so they can be used as dict keys (e.g. in environments)
        return hash(self.name)


class Vector(list):
    """Represents a Lisp vector, which is self-evaluating.
    Inherits from list for convenience but can be distinctly identified.
    """

    def __repr__(self):
        # Provide a Lisp-like representation for vectors
        return f"[{' '.join(map(repr, self))}]"

    # No need to override __eq__ or __hash__ if list's behavior is fine
    # and vectors are mutable like lists. If they need to be hashable for some reason
    # (e.g., to be keys in LisPy maps, though not typical for vectors),
    # then __hash__ and __eq__ would need careful consideration, likely making them immutable.
    # For now, assume they are mutable sequences like Python lists.


class LispyList(list):
    """Represents a Lisp list.
    Inherits from list for convenience and distinct identification.
    """

    def __repr__(self):
        # Provide a Lisp-like representation for lists
        return f"({' '.join(map(repr, self))})"

    # Similar to Vector, assuming mutable sequence behavior from Python lists.
    # If lists needed to be hashable, immutability would be a consideration.

# LisPy Environment

# from .evaluator import EvaluationError # Old import
from .exceptions import EvaluationError  # EvaluationError now from .exceptions


class Environment:
    """Manages symbol bindings for the LisPy interpreter."""

    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer  # For lexical scoping later

    def define(self, name_str: str, value):
        """Define a symbol in the current environment."""
        # `name_str` should be the string name of the symbol
        self.store[name_str] = value

    def lookup(self, name_str: str):
        """Look up a symbol in this environment or outer ones."""
        # `name_str` should be the string name of the symbol
        if name_str in self.store:
            return self.store[name_str]
        elif self.outer is not None:
            return self.outer.lookup(name_str)
        else:
            raise EvaluationError(f"Unbound symbol: {name_str}")

    # We might add methods like `set` later if we want to modify existing
    # bindings, which has different semantics from `define` in some Lisps.

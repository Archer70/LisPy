import os
from typing import Dict, Set, List, Optional
from .environment import Environment
from .exceptions import EvaluationError
from .lexer import tokenize
from .parser import parse


class Module:
    """Represents a loaded LisPy module."""

    def __init__(self, name: str, file_path: str):
        self.name = name
        self.file_path = file_path
        # Module's private environment - inherit from global environment for built-ins
        from .functions import create_global_env

        self.env = create_global_env()  # Start with built-in functions
        self.exports: Set[str] = set()  # Exported symbol names
        self.loaded = False

    def add_export(self, symbol_name: str):
        """Add a symbol to the module's exports."""
        self.exports.add(symbol_name)

    def get_exported_value(self, symbol_name: str):
        """Get the value of an exported symbol."""
        if symbol_name not in self.exports:
            raise EvaluationError(
                f"Symbol '{symbol_name}' is not exported by module '{self.name}'"
            )
        return self.env.lookup(symbol_name)

    def get_all_exports(self) -> Dict[str, any]:
        """Get all exported symbols and their values."""
        result = {}
        for symbol_name in self.exports:
            try:
                result[symbol_name] = self.env.lookup(symbol_name)
            except EvaluationError:
                # Symbol was exported but not defined - skip it
                pass
        return result


class ModuleLoader:
    """Handles loading and caching of LisPy modules."""

    def __init__(self):
        self.cache: Dict[str, Module] = {}  # module_name -> Module
        self.loading: Set[str] = set()  # Track modules currently being loaded
        self.load_paths: List[str] = ["."]  # Default load path

    def add_load_path(self, path: str):
        """Add a directory to the module load path."""
        if path not in self.load_paths:
            self.load_paths.append(path)

    def find_module_file(self, module_name: str) -> Optional[str]:
        """Find the file path for a given module name."""
        # Convert module name to file path (e.g., "math/utils" -> "math/utils.lpy")
        relative_path = module_name.replace("/", os.sep) + ".lpy"

        for load_path in self.load_paths:
            full_path = os.path.join(load_path, relative_path)
            if os.path.isfile(full_path):
                return os.path.abspath(full_path)
        return None

    def load_module(self, module_name: str, evaluator_func) -> Module:
        """
        Load a module by name. Returns cached module if already loaded.
        evaluator_func should be the evaluate function from evaluator.py
        """
        # Check cache first
        if module_name in self.cache:
            return self.cache[module_name]

        # Check for circular dependency
        if module_name in self.loading:
            raise EvaluationError(
                f"Circular dependency detected: module '{module_name}' is already being loaded"
            )

        # Find the module file
        file_path = self.find_module_file(module_name)
        if file_path is None:
            raise EvaluationError(
                f"Module '{module_name}' not found in load paths: {self.load_paths}"
            )

        # Mark as loading to detect circular dependencies
        self.loading.add(module_name)

        try:
            # Create module instance
            module = Module(module_name, file_path)

            # Read and parse the module file
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            # Tokenize and parse
            tokens = tokenize(source_code)

            # Parse all expressions in the file
            expressions = self._parse_all_expressions(tokens)

            # Set the current module context for export forms
            set_current_module(module, module.env)

            # Evaluate all expressions in the module's environment
            for expr in expressions:
                evaluator_func(expr, module.env)

            # Mark as loaded
            module.loaded = True

            # Cache the module
            self.cache[module_name] = module

            return module

        finally:
            # Remove from loading set
            self.loading.discard(module_name)

    def _parse_all_expressions(self, tokens):
        """Parse all expressions from a list of tokens."""
        expressions = []
        position = 0

        while position < len(tokens):
            # Find the end of the current expression
            expr_tokens, new_position = self._extract_next_expression_tokens(
                tokens, position
            )
            if expr_tokens:
                expr = parse(expr_tokens)
                expressions.append(expr)
            position = new_position

        return expressions

    def _extract_next_expression_tokens(self, tokens, start_pos):
        """Extract tokens for the next complete expression."""
        if start_pos >= len(tokens):
            return [], start_pos

        # Handle different token types
        token_type, token_value = tokens[start_pos]

        if token_type in ["NUMBER", "STRING", "BOOLEAN", "NIL", "SYMBOL"]:
            # Atomic expression - just one token
            return [tokens[start_pos]], start_pos + 1
        elif token_type == "QUOTE":
            # Quote expression - quote token + next expression
            quote_tokens = [tokens[start_pos]]
            next_expr_tokens, new_pos = self._extract_next_expression_tokens(
                tokens, start_pos + 1
            )
            return quote_tokens + next_expr_tokens, new_pos
        elif token_type in ["LPAREN", "LBRACKET", "LBRACE"]:
            # Compound expression - find matching closing delimiter
            return self._extract_compound_expression(tokens, start_pos)
        else:
            raise EvaluationError(f"Unexpected token type: {token_type}")

    def _extract_compound_expression(self, tokens, start_pos):
        """Extract a compound expression (list, vector, or map)."""
        if start_pos >= len(tokens):
            return [], start_pos

        opening_token = tokens[start_pos][0]
        closing_token = {
            "LPAREN": "RPAREN",
            "LBRACKET": "RBRACKET",
            "LBRACE": "RBRACE",
        }[opening_token]

        result_tokens = [tokens[start_pos]]  # Include opening token
        pos = start_pos + 1
        depth = 1

        while pos < len(tokens) and depth > 0:
            token_type, token_value = tokens[pos]
            result_tokens.append(tokens[pos])

            if token_type == opening_token:
                depth += 1
            elif token_type == closing_token:
                depth -= 1

            pos += 1

        if depth > 0:
            raise EvaluationError(f"Unclosed {opening_token} in module")

        return result_tokens, pos

    def get_module(self, module_name: str) -> Optional[Module]:
        """Get a cached module by name."""
        return self.cache.get(module_name)

    def is_loaded(self, module_name: str) -> bool:
        """Check if a module is already loaded."""
        return module_name in self.cache and self.cache[module_name].loaded


# Global module loader instance
_module_loader = ModuleLoader()


def get_module_loader() -> ModuleLoader:
    """Get the global module loader instance."""
    return _module_loader


def set_current_module(module: Module, env: Environment):
    """Set the current module context in an environment."""
    # Store module reference in environment for export special form
    env._current_module = module


def get_current_module(env: Environment) -> Optional[Module]:
    """Get the current module from an environment."""
    return getattr(env, "_current_module", None)

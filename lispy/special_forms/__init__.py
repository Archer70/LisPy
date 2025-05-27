# lispy_project/lispy/special_forms/__init__.py
from typing import Dict, Callable, List, Any
from ..environment import Environment # For type hint in handler signature

# Import handler functions
from .define_form import handle_define_form
from .fn_form import handle_fn_form # Changed from lambda_form to fn_form
from .if_form import handle_if_form
from .let_form import handle_let_form
from .quote_form import handle_quote_form
from .thread_first import handle_thread_first # Added thread_first
from .export_form import export_form
from .import_form import import_form

# A registry for special form handlers
# Maps the symbol (as a string) to the handler function
special_form_handlers = {
    "define": handle_define_form,
    "fn": handle_fn_form, # Changed from handle_lambda_form
    "if": handle_if_form,
    "let": handle_let_form,
    "quote": handle_quote_form,
    "->": handle_thread_first, # Added thread_first
    "export": export_form,
    "import": import_form,
}

__all__ = ["special_form_handlers"] # Keep __all__ simple for now
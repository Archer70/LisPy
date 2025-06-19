# lispy_project/lispy/special_forms/__init__.py
from typing import Dict, Callable, List, Any
from ..environment import Environment  # For type hint in handler signature

# Import handler functions (alphabetized)
from .and_form import handle_and_form, documentation_and
from .async_form import handle_async_form, documentation_async
from .await_form import handle_await_form, documentation_await
from .bdd.action_form import action_form_handler
from .bdd.assert_raises_q_form import assert_raises_q_form_handler
from .bdd.describe_form import describe_form_handler
from .bdd.given_form import given_form_handler
from .bdd.it_form import it_form_handler
from .bdd.then_form import then_form_handler
from .cond_form import handle_cond, documentation_cond
from .define_form import handle_define_form, documentation_define
from .defn_async_form import handle_defn_async_form, documentation_defn_async
from .doseq_form import handle_doseq_form, documentation_doseq
from .export_form import export_form, documentation_export
from .fn_form import handle_fn_form, documentation_fn
from .if_form import handle_if_form, documentation_if
from .import_form import import_form, documentation_import
from .let_form import handle_let_form, documentation_let
from .loop_form import handle_loop_form, documentation_loop
from .or_form import handle_or_form, documentation_or
from .quote_form import handle_quote_form, documentation_quote
from .recur_form import handle_recur, documentation_recur
from .thread_first import handle_thread_first, documentation_thread_first
from .thread_last import handle_thread_last, documentation_thread_last
from .throw_form import handle_throw_form, documentation_throw
from .try_form import handle_try_form, documentation_try
from .when_form import handle_when_form, documentation_when

# A registry for special form handlers (alphabetized by key)
# Maps the symbol (as a string) to the handler function
special_form_handlers: Dict[str, Callable[[List[Any], Environment, Callable], Any]] = {
    "->": handle_thread_first,
    "->>": handle_thread_last,
    "action": action_form_handler,
    "and": handle_and_form,
    "assert-raises?": assert_raises_q_form_handler,
    "async": handle_async_form,
    "await": handle_await_form,
    "cond": handle_cond,
    "define": handle_define_form,
    "defn-async": handle_defn_async_form,
    "describe": describe_form_handler,
    "doseq": handle_doseq_form,
    "export": export_form,
    "fn": handle_fn_form,
    "given": given_form_handler,
    "if": handle_if_form,
    "import": import_form,
    "it": it_form_handler,
    "let": handle_let_form,
    "loop": handle_loop_form,
    "or": handle_or_form,
    "quote": handle_quote_form,
    "recur": handle_recur,
    "then": then_form_handler,
    "throw": handle_throw_form,
    "try": handle_try_form,
    "when": handle_when_form,
}

__all__ = [
    "special_form_handlers",
    "documentation_and",
    "documentation_async",
    "documentation_await",
    "documentation_cond",
    "documentation_define",
    "documentation_defn_async",
    "documentation_doseq",
    "documentation_export",
    "documentation_fn",
    "documentation_if",
    "documentation_import",
    "documentation_let",
    "documentation_loop",
    "documentation_or",
    "documentation_quote",
    "documentation_recur",
    "documentation_thread_first",
    "documentation_thread_last",
    "documentation_throw",
    "documentation_try",
    "documentation_when"
]

from ..exceptions import EvaluationError
from ..types import Symbol
from ..module_system import get_module_loader


def import_form(expression, env, evaluate):
    """
    Handle the import special form.
    Supports multiple syntax forms:
    - (import "module-name")                    # Import all exports
    - (import "module-name" :as "prefix")       # Import with prefix
    - (import "module-name" :only (sym1 sym2))  # Selective import
    """
    if len(expression) < 2:
        raise EvaluationError("SyntaxError: 'import' requires a module name")

    # Extract module name
    module_name_expr = expression[1]
    if not isinstance(module_name_expr, str):
        raise EvaluationError("SyntaxError: 'import' module name must be a string")

    module_name = module_name_expr

    # Parse import options
    import_style = "all"  # Default: import all exports
    prefix = None
    only_symbols = None

    # Parse optional arguments
    i = 2
    while i < len(expression):
        arg = expression[i]

        if isinstance(arg, Symbol) and arg.name == ":as":
            if i + 1 >= len(expression):
                raise EvaluationError("SyntaxError: 'import :as' requires a prefix")
            prefix_expr = expression[i + 1]
            if not isinstance(prefix_expr, str):
                raise EvaluationError(
                    "SyntaxError: 'import :as' prefix must be a string"
                )
            prefix = prefix_expr
            import_style = "prefixed"
            i += 2
        elif isinstance(arg, Symbol) and arg.name == ":only":
            if i + 1 >= len(expression):
                raise EvaluationError(
                    "SyntaxError: 'import :only' requires a symbol list"
                )
            only_expr = expression[i + 1]
            if not isinstance(only_expr, list):
                raise EvaluationError(
                    "SyntaxError: 'import :only' requires a list of symbols"
                )

            # Validate that all items in the list are symbols
            only_symbols = []
            for sym_expr in only_expr:
                if not isinstance(sym_expr, Symbol):
                    raise EvaluationError(
                        "SyntaxError: 'import :only' list must contain only symbols"
                    )
                only_symbols.append(sym_expr.name)

            import_style = "selective"
            i += 2
        else:
            raise EvaluationError(f"SyntaxError: Unknown import option: {arg}")

    # Load the module
    module_loader = get_module_loader()
    try:
        module = module_loader.load_module(module_name, evaluate)
    except Exception as e:
        raise EvaluationError(f"Failed to load module '{module_name}': {str(e)}")

    # Import symbols based on the style
    if import_style == "all":
        _import_all_exports(module, env)
    elif import_style == "prefixed":
        _import_with_prefix(module, env, prefix)
    elif import_style == "selective":
        _import_selective(module, env, only_symbols)

    # Return nil (import is a side-effect operation)
    return None


def _import_all_exports(module, env):
    """Import all exported symbols from a module."""
    exports = module.get_all_exports()
    for symbol_name, value in exports.items():
        env.define(symbol_name, value)


def _import_with_prefix(module, env, prefix):
    """Import all exported symbols with a prefix."""
    exports = module.get_all_exports()
    for symbol_name, value in exports.items():
        prefixed_name = f"{prefix}/{symbol_name}"
        env.define(prefixed_name, value)


def _import_selective(module, env, symbol_names):
    """Import only the specified symbols from a module."""
    for symbol_name in symbol_names:
        try:
            value = module.get_exported_value(symbol_name)
            env.define(symbol_name, value)
        except EvaluationError as e:
            raise EvaluationError(
                f"Cannot import '{symbol_name}' from module '{module.name}': {str(e)}"
            )

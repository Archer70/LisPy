# LisPy Custom Exceptions


class LisPyError(Exception):
    """Base class for all LisPy-specific errors."""

    pass


class ParseError(LisPyError):
    """Custom exception for parsing errors."""

    pass


class EvaluationError(LisPyError):
    """Custom exception for evaluation errors."""

    pass


class ArityError(EvaluationError):
    """Custom exception for function arity errors."""

    pass


class LexerError(LisPyError):
    """Custom exception for lexer/tokenization errors."""

    pass


class PromiseError(LisPyError):
    """Custom exception for promise-related errors."""

    pass


class UserThrownError(LisPyError):
    """Exception thrown by user code via (throw ...)."""

    def __init__(self, value):
        self.value = value
        super().__init__(str(value))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"UserThrownError({repr(self.value)})"


class AssertionFailure(LisPyError):
    """Custom exception for BDD assertion failures."""

    pass

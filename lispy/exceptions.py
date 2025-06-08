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


class AssertionFailure(LisPyError):
    """Custom exception for BDD assertion failures."""

    pass

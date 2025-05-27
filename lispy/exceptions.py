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

class LexerError(LisPyError):
    """Custom exception for lexer/tokenization errors."""
    pass 
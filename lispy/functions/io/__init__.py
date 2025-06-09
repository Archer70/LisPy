"""LisPy I/O Functions"""

from .print import builtin_print, documentation_print
from .println import builtin_println, documentation_println
from .read_line import builtin_read_line, documentation_read_line
from .slurp import builtin_slurp, documentation_slurp
from .spit import builtin_spit, documentation_spit

__all__ = [
    # Functions
    "builtin_print",
    "builtin_println",
    "builtin_read_line",
    "builtin_slurp",
    "builtin_spit",
    # Documentation
    "documentation_print",
    "documentation_println",
    "documentation_read_line",
    "documentation_slurp",
    "documentation_spit",
] 
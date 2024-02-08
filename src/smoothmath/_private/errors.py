from __future__ import annotations


class DomainError(Exception):
    """Raised when evaluating or localizing at a Point where an Expression is not defined."""
    pass

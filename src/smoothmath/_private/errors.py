from __future__ import annotations


class DomainError(Exception):
    """
    Raised when evaluating or differentiating at a point where an expression is not defined.
    """

    pass


class CoordinateMissing(Exception):
    """
    Raised when a :class:`~smoothmath.Point` does not have a required coordinate.
    """

    pass

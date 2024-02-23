from __future__ import annotations


class DomainError(Exception):
    """
    Raised when evaluating or differentiating at a point where an
    :class:`~smoothmath.Expression` is undefined.
    """

    pass


class CoordinateMissing(Exception):
    """
    Raised when a :class:`~smoothmath.Point` does not have a required coordinate.
    """

    pass

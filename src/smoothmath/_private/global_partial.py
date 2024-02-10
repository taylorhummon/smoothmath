from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath import RealNumber, Expression, Point


class GlobalPartial:
    """
    The partial derivative of an expression.
    """

    @classmethod
    def build(
        cls: type,
        original_expression: Expression,
        synthetic_partial: Expression
    ):
        return cls(original_expression, synthetic_partial._normalize())

    def __init__(
        self: GlobalPartial,
        original_expression: Expression,
        synthetic_partial: Expression
    ) -> None:
        #: The expression which this is the partial derivative of.
        self.original_expression: Expression
        self.original_expression = original_expression
        self._synthetic_partial: Expression
        self._synthetic_partial = synthetic_partial

    def at(
        self: GlobalPartial,
        point: Point
    ) -> RealNumber:
        """
        Localize the partial derivative at a point.

        :param point: where to localize
        """
        # We evaluate the original expression to check for DomainErrors.
        # e.g. (ln(x))' = 1 / x
        # Notice that the RHS appears defined for negative x, but ln(x) isn't defined there!
        self.original_expression.evaluate(point)
        return self._synthetic_partial.evaluate(point)

    def __eq__(
        self: GlobalPartial,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self.original_expression == other.original_expression) and
            (self._synthetic_partial == other._synthetic_partial)
        )

    def __hash__(
        self: GlobalPartial
    ) -> int:
        return hash((self.original_expression, self._synthetic_partial))

    def __str__(
        self: GlobalPartial
    ) -> str:
        return str(self._synthetic_partial)

    def __repr__(
        self: GlobalPartial
    ) -> str:
        return f"(original: {self.original_expression}; partial: {self._synthetic_partial})"

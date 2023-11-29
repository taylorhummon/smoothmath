from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.expression import Expression


class GlobalPartial:
    def __init__(
        self: GlobalPartial,
        original_expression: Expression,
        synthetic_partial: Expression
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._synthetic_partial: Expression
        self._synthetic_partial = synthetic_partial

    def at(
        self: GlobalPartial,
        point: Point
    ) -> real_number:
        # We evaluate the original expression to check for DomainErrors.
        # e.g. (ln(x))' = 1 / x
        # Notice that the RHS appears defined for negative x, but ln(x) isn't defined there!
        self.original_expression.evaluate(point)
        return self._synthetic_partial.evaluate(point)

    def __eq__(
        self: GlobalPartial,
        other: GlobalPartial
    ) -> bool:
        # We'll assume correctness of the synthetic partial, so it suffices to compare
        # the original expressions.
        return self.original_expression == other.original_expression

    def __str__(
        self: GlobalPartial
    ) -> str:
        return str(self._synthetic_partial)

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
        global_partial: Expression
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._global_partial: Expression # !!! decide on different name
        self._global_partial = global_partial

    def partial_at(
        self: GlobalPartial,
        point: Point
    ) -> real_number:
        # We evaluate the original expression to check for DomainErrors.
        # e.g. (ln(x))' = 1 / x
        # Notice that the RHS appears defined for negative x, but ln(x) isn't defined there!
        self.original_expression.evaluate(point)
        return self._global_partial.evaluate(point)

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
import smoothmath.expressions as ex


# differential rule: d(a + b) = da + db

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._value = a_value + b_value
        return self._value

    def _partial_at(
        self: Plus,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._partial_at(point, with_respect_to)
        b_partial = self._b._partial_at(point, with_respect_to)
        return a_partial + b_partial

    def _compute_local_partials(
        self: Plus,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        self._a._compute_local_partials(computed_local_partials, point, accumulated)
        self._b._compute_local_partials(computed_local_partials, point, accumulated)

    def _global_partial(
        self: Plus,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        b_partial = self._b._global_partial(with_respect_to)
        return ex.Plus(a_partial, b_partial)

    def _compute_global_partials(
        self: Plus,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        self._a._compute_global_partials(computed_global_partials, accumulated)
        self._b._compute_global_partials(computed_global_partials, accumulated)

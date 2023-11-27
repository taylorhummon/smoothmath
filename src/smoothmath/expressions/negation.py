from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.expression import Expression

from smoothmath.expression import UnaryExpression
import smoothmath.expressions as ex


# differential rule: d(-a) = -da

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = - a_value
        return self._value

    def _local_partial(
        self: Negation,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._local_partial(point, with_respect_to)
        return - a_partial

    def _global_partial(
        self: Negation,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        return ex.Negation(a_partial)

    def _compute_local_partials(
        self: Negation,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        self._a._compute_local_partials(computed_local_partials, point, - accumulated)

    def _compute_global_partials(
        self: Negation,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        self._a._compute_global_partials(computed_global_partials, ex.Negation(accumulated))

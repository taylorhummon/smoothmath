from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
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

    def _partial_at(
        self: Negation,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._partial_at(point, with_respect_to)
        return - a_partial

    def _compute_all_partials_at(
        self: Negation,
        all_partials: AllPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        self._a._compute_all_partials_at(all_partials, point, - accumulated)

    def _synthetic_partial(
        self: Negation,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Negation(a_partial)

    def _compute_all_synthetic_partials(
        self: Negation,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        self._a._compute_all_synthetic_partials(synthetic, ex.Negation(accumulated))

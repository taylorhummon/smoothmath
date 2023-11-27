from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.expression import Expression

import math
from smoothmath.expression import UnaryExpression
import smoothmath.expressions as ex


# differential rule: d(cos(a)) = - sin(a) * da

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = math.cos(a_value)
        return self._value

    def _local_partial(
        self: Cosine,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return - math.sin(a_value) * a_partial

    def _global_partial(
        self: Cosine,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        return ex.Multiply(
            ex.Negation(ex.Sine(self._a)),
            a_partial
        )

    def _compute_local_partials(
        self: Cosine,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        next_accumulated = - accumulated * math.sin(a_value)
        self._a._compute_local_partials(computed_local_partials, point, next_accumulated)

    def _compute_global_partials(
        self: Cosine,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        next_accumulated = ex.Multiply(accumulated, ex.Negation(ex.Sine(self._a)))
        self._a._compute_global_partials(computed_global_partials, next_accumulated)

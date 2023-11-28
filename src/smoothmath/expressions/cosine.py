from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.local_differential import LocalDifferential
    from smoothmath.global_differential import GlobalDifferential
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

    def _synthetic_partial(
        self: Cosine,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Negation(ex.Sine(self._a)),
            a_partial
        )

    def _compute_local_differential(
        self: Cosine,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        next_accumulated = - accumulated * math.sin(a_value)
        self._a._compute_local_differential(local_differential, point, next_accumulated)

    def _compute_global_differential(
        self: Cosine,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None:
        next_accumulated = ex.Multiply(accumulated, ex.Negation(ex.Sine(self._a)))
        self._a._compute_global_differential(global_differential, next_accumulated)

from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(cos(a)) = - sin(a) * da

class Cosine(base.UnaryExpression):
    def __init__(
        self: Cosine,
        expression: sm.Expression
    ) -> None:
        super().__init__(expression)

    def _evaluate(
        self: Cosine,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = math.cos(a_value)
        return self._value

    def _local_partial(
        self: Cosine,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return - math.sin(a_value) * a_partial

    def _synthetic_partial(
        self: Cosine,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Negation(ex.Sine(self._a)),
            a_partial
        )

    def _compute_local_differential(
        self: Cosine,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(builder.point)
        next_accumulated = - accumulated * math.sin(a_value)
        self._a._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Cosine,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = ex.Multiply(accumulated, ex.Negation(ex.Sine(self._a)))
        self._a._compute_global_differential(builder, next_accumulated)

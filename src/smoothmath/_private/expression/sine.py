from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.expression.base import UnaryExpression
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(sin(a)) = cos(a) * da

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: sm.Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = math.sin(a_value)
        return self._value

    def _local_partial(
        self: Sine,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return math.cos(a_value) * a_partial

    def _synthetic_partial(
        self: Sine,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Cosine(self._a),
            a_partial
        )

    def _compute_local_differential(
        self: Sine,
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        next_accumulated = accumulated * math.cos(a_value)
        self._a._compute_local_differential(builder, point, next_accumulated)

    def _compute_global_differential(
        self: Sine,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = ex.Multiply(accumulated, ex.Cosine(self._a))
        self._a._compute_global_differential(builder, next_accumulated)

from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(a ** 2) = 2 * a * da

class Square(base.UnaryExpression):
    def __init__(
        self: Square,
        a: sm.Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Square,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = a_value ** 2
        return self._value

    def _local_partial(
        self: Square,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return 2 * a_value * a_partial

    def _synthetic_partial(
        self: Square,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Square,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(builder.point)
        next_accumulated = accumulated * 2 * a_value
        self._a._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Square,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(builder, next_accumulated)

    def _synthetic_partial_helper(
        self: Square,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            multiplier,
            ex.Multiply(ex.Constant(2), self._a)
        )

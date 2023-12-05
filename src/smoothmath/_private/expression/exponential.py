from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.expression.base import UnaryExpression
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(C ** a) = ln(C) * (C ** a) * da

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: sm.Expression,
        base: sm.real_number = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base: sm.real_number
        self._base = base

    def _rebuild(
        self: Exponential,
        a: sm.Expression
    ) -> Exponential:
        return Exponential(a, self._base)

    def _evaluate(
        self: Exponential,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = self._base ** a_value
        return self._value

    def _local_partial(
        self: Exponential,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        result_value = self._base ** a_value
        return math.log(self._base) * result_value * a_partial

    def _synthetic_partial(
        self: Exponential,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Exponential,
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None:
        self_value = self._evaluate(point)
        next_accumulated = accumulated * math.log(self._base) * self_value
        self._a._compute_local_differential(builder, point, next_accumulated)

    def _compute_global_differential(
        self: Exponential,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(builder, next_accumulated)

    def _synthetic_partial_helper(
        self: Exponential,
        multiplier: sm.Expression
    ) -> sm.Expression:
        if self._base == math.e:
            return ex.Multiply(multiplier, ex.Exponential(self._a, base = self._base))
        else:
            return ex.Multiply(
                multiplier,
                ex.Multiply(
                    ex.Logarithm(ex.Constant(self._base), base = math.e),
                    ex.Exponential(self._a, base = self._base)
                )
            )

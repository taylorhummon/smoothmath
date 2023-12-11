from __future__ import annotations
from typing import TYPE_CHECKING, Any
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import get_class_name
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(C ** a) = log_e(C) * (C ** a) * da

class Exponential(base.ParameterizedUnaryExpression):
    def __init__(
        self: Exponential,
        base: sm.real_number,
        expression: sm.Expression
    ) -> None:
        super().__init__(expression)
        if base <= 0:
            raise Exception(f"Exponentials must have a positive base, found: {base}")
        self._base: sm.real_number
        self._base = base

    def _rebuild(
        self: Exponential,
        expression: sm.Expression
    ) -> Exponential:
        return ex.Exponential(self._base, expression)

    def _parameter(
        self: Exponential
    ) -> sm.real_number:
        return self._base

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
        self_value = self._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return math.log(self._base) * self_value * a_partial

    def _synthetic_partial(
        self: Exponential,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Exponential,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self_value = self._evaluate(builder.point)
        next_accumulated = accumulated * math.log(self._base) * self_value
        self._a._compute_local_differential(builder, next_accumulated)

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
        if self._base == 1:
            return ex.Constant(0)
        elif self._base == math.e:
            return ex.Multiply(multiplier, ex.Exponential(self._base, self._a))
        else:
            return ex.Multiply(
                multiplier,
                ex.Multiply(
                    ex.Logarithm(math.e, ex.Constant(self._base)),
                    ex.Exponential(self._base, self._a)
                )
            )

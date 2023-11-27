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


# differential rule: d(C ** a) = ln(C) * (C ** a) * da

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: real_number = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base: real_number
        self._base = base

    def _evaluate(
        self: Exponential,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = self._base ** a_value
        return self._value

    def _local_partial(
        self: Exponential,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        result_value = self._base ** a_value
        return math.log(self._base) * result_value * a_partial

    def _global_partial(
        self: Exponential,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        return self._global_partial_helper(a_partial)

    def _compute_local_partials(
        self: Exponential,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None:
        self_value = self._evaluate(point)
        next_accumulated = accumulated * math.log(self._base) * self_value
        self._a._compute_local_partials(local_differential, point, next_accumulated)

    def _compute_global_partials(
        self: Exponential,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._global_partial_helper(accumulated)
        self._a._compute_global_partials(global_differential, next_accumulated)

    def _global_partial_helper(
        self: Exponential,
        multiplier: Expression
    ) -> Expression:
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

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.synthetic import Synthetic
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

    def _partial_at(
        self: Exponential,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        a_partial = self._a._partial_at(point, with_respect_to)
        result_value = self._base ** a_value
        return math.log(self._base) * result_value * a_partial

    def _compute_local_partials(
        self: Exponential,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        self_value = self._evaluate(point)
        next_accumulated = accumulated * math.log(self._base) * self_value
        self._a._compute_local_partials(computed_local_partials, point, next_accumulated)

    def _synthetic_partial(
        self: Exponential,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_all_synthetic_partials(
        self: Exponential,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_all_synthetic_partials(synthetic, next_accumulated)

    def _synthetic_partial_helper(
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

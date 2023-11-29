from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.local_differential import LocalDifferentialBuilder
    from smoothmath.global_differential import GlobalDifferentialBuilder
    from smoothmath.expression import Expression

import math
from smoothmath.expression import UnaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(log_C(a)) = (1 / (log_e(C) * a)) * da

class Logarithm(UnaryExpression):
    def __init__(
        self: Logarithm,
        a: Expression,
        base: real_number = math.e
    ) -> None:
        super().__init__(a)
        if base <= 0:
            raise Exception("Logarithms must have a positive base")
        elif base == 1:
            raise Exception("Logarithms cannot have base = 1")
        self._base: real_number
        self._base = base

    def _verify_domain_constraints(
        self: Logarithm,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("Logarithm(x) blows up around x = 0")
        elif a_value < 0:
            raise DomainError("Logarithm(x) is undefined for x < 0")

    def _evaluate(
        self: Logarithm,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self._value = math.log(a_value, self._base)
        return self._value

    def _local_partial(
        self: Logarithm,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._local_partial(point, with_respect_to)
        return a_partial / (math.log(self._base) * a_value)

    def _synthetic_partial(
        self: Logarithm,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Logarithm,
        builder: LocalDifferentialBuilder,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        next_accumulated = accumulated / (math.log(self._base) * a_value)
        self._a._compute_local_differential(builder, point, next_accumulated)

    def _compute_global_differential(
        self: Logarithm,
        builder: GlobalDifferentialBuilder,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(builder, next_accumulated)

    def _synthetic_partial_helper(
        self: Logarithm,
        multiplier: Expression
    ) -> Expression:
        if self._base == math.e:
            return ex.Divide(multiplier, self._a)
        else:
            return ex.Divide(
                multiplier,
                ex.Multiply(
                    ex.Logarithm(ex.Constant(self._base), base = math.e),
                    self._a,
                )
            )

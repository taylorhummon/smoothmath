from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Logarithm(base.ParameterizedUnaryExpression):
    def __init__(
        self: Logarithm,
        inner: sm.Expression,
        base: sm.real_number
    ) -> None:
        super().__init__(inner, base)
        if base <= 0:
            raise Exception("Logarithm must have a positive base")
        elif base == 1:
            raise Exception("Logarithm cannot have base = 1")

    @property
    def base(
        self: Logarithm
    ) -> sm.real_number:
        return self._parameter

    def _verify_domain_constraints(
        self: Logarithm,
        inner_value: sm.real_number
    ) -> None:
        if inner_value == 0:
            raise sm.DomainError("Logarithm(x) blows up around x = 0")
        elif inner_value < 0:
            raise sm.DomainError("Logarithm(x) is undefined for x < 0")

    def _value_formula(
        self: Logarithm,
        inner_value: sm.real_number
    ):
        return math.log(inner_value, self.base)

    def _local_partial(
        self: Logarithm,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: Logarithm,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: Logarithm,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        inner_value = self._inner._evaluate(builder.point)
        self._verify_domain_constraints(inner_value)
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Logarithm,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: Logarithm,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        if self.base == math.e:
            return multiplier / inner_value
        else:
            return multiplier / (math.log(self.base, math.e) * inner_value)

    def _synthetic_partial_formula(
        self: Logarithm,
        multiplier: sm.Expression
    ) -> sm.Expression:
        if self.base == math.e:
            return ex.Divide(multiplier, self._inner)
        else:
            return ex.Divide(
                multiplier,
                ex.Multiply(ex.Logarithm(ex.Constant(self.base), base = math.e), self._inner)
            )

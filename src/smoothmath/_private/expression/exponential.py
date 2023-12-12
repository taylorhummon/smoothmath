from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Exponential(base.ParameterizedUnaryExpression):
    def __init__(
        self: Exponential,
        base: sm.real_number,
        inner: sm.Expression
    ) -> None:
        super().__init__(inner)
        if base <= 0:
            raise Exception(f"Exponentials must have a positive base, found: {base}")
        self._base: sm.real_number
        self._base = base

    def _parameter(
        self: Exponential
    ) -> sm.real_number:
        return self._base

    def _verify_domain_constraints(
        self: Exponential,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Exponential,
        inner_value: sm.real_number
    ):
        return self._base ** inner_value

    def _local_partial(
        self: Exponential,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: Exponential,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: Exponential,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Exponential,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: Exponential,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        if self._base == 1:
            return 0
        self_value = self._evaluate(point)
        if self._base == math.e:
            return self_value * multiplier
        else:
            return math.log(self._base) * self_value * multiplier

    def _synthetic_partial_formula(
        self: Exponential,
        multiplier: sm.Expression
    ) -> sm.Expression:
        if self._base == 1:
            return ex.Constant(0)
        elif self._base == math.e:
            return ex.Multiply(ex.Exponential(self._base, self._inner), multiplier)
        else:
            return ex.Multiply(
                ex.Multiply(
                    ex.Logarithm(math.e, ex.Constant(self._base)),
                    ex.Exponential(self._base, self._inner)
                ),
                multiplier
            )

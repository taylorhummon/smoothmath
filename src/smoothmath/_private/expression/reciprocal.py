from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.expression.nth_power import nth_power
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Reciprocal(base.UnaryExpression):
    def __init__(
        self: Reciprocal,
        inner: sm.Expression
    ) -> None:
        super().__init__(inner)

    def _verify_domain_constraints(
        self: Reciprocal,
        point: sm.Point
    ) -> None:
        inner_value = self._inner._evaluate(point)
        if inner_value == 0:
            raise sm.DomainError("Reciprocal(x) blows up around x = 0")

    def _evaluate(
        self: Reciprocal,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        self._verify_domain_constraints(point)
        inner_value = self._inner._evaluate(point)
        self._value = 1 / inner_value
        return self._value

    def _local_partial(
        self: Reciprocal,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        self._verify_domain_constraints(point)
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: Reciprocal,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: Reciprocal,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._verify_domain_constraints(builder.point)
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Reciprocal,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: Reciprocal,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        return - nth_power(-2, inner_value) * multiplier

    def _synthetic_partial_formula(
        self: Reciprocal,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Negation(ex.NthPower(-2, self._inner)), multiplier)

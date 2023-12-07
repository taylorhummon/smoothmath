from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(1 / a) = - (1 / a ** 2) * da

class Reciprocal(base.UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: sm.Expression
    ) -> None:
        super().__init__(a)

    def _verify_domain_constraints(
        self: Reciprocal,
        a_value: sm.real_number
    ) -> None:
        if a_value == 0:
            raise sm.DomainError("Reciprocal(x) blows up around x = 0")

    def _evaluate(
        self: Reciprocal,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self._value = 1 / a_value
        return self._value

    def _local_partial(
        self: Reciprocal,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._local_partial(point, with_respect_to)
        result_value = self._evaluate(point)
        return - (result_value ** 2) * a_partial

    def _synthetic_partial(
        self: Reciprocal,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Reciprocal,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(builder.point)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(builder.point)
        next_accumulated = - accumulated * (self_value ** 2)
        self._a._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Reciprocal,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(builder, next_accumulated)

    def _synthetic_partial_helper(
        self: Reciprocal,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            ex.Negation(ex.Reciprocal(ex.Power(self._a, ex.Constant(2)))),
            multiplier
        )

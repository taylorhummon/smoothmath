from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(sqrt(a)) = (1 / (2 sqrt(a))) * da

class SquareRoot(base.UnaryExpression):
    def __init__(
        self: SquareRoot,
        expression: sm.Expression
    ) -> None:
        super().__init__(expression)

    def _verify_domain_constraints(
        self: SquareRoot,
        a_value: sm.real_number
    ) -> None:
        if a_value == 0:
            raise sm.DomainError("SquareRoot(x) is not smooth around x = 0")
        elif a_value < 0:
            raise sm.DomainError("SquareRoot(x) is undefined for x < 0")

    def _evaluate(
        self: SquareRoot,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self._value = math.sqrt(a_value)
        return self._value

    def _local_partial(
        self: SquareRoot,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        self_value = self._evaluate(point)
        a_partial = self._a._local_partial(point, with_respect_to)
        return a_partial / (2 * self_value)

    def _synthetic_partial(
        self: SquareRoot,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: SquareRoot,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(builder.point)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(builder.point)
        next_accumulated = accumulated / (2 * self_value)
        self._a._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: SquareRoot,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(builder, next_accumulated)

    def _synthetic_partial_helper(
        self: SquareRoot,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Divide(
            multiplier,
            ex.Multiply(ex.Constant(2), ex.SquareRoot(self._a))
        )

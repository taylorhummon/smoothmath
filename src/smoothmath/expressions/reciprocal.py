from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.local_differential import LocalDifferential
    from smoothmath.global_differential import GlobalDifferential
    from smoothmath.expression import Expression

from smoothmath.expression import UnaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(1 / a) = - (1 / a ** 2) * da

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _verify_domain_constraints(
        self: Reciprocal,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("Reciprocal(x) blows up around x = 0")

    def _evaluate(
        self: Reciprocal,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self._value = 1 / a_value
        return self._value

    def _local_partial(
        self: Reciprocal,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._local_partial(point, with_respect_to)
        result_value = self._evaluate(point)
        return - (result_value ** 2) * a_partial

    def _synthetic_partial(
        self: Reciprocal,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: Reciprocal,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(point)
        next_accumulated = - accumulated * (self_value ** 2)
        self._a._compute_local_differential(local_differential, point, next_accumulated)

    def _compute_global_differential(
        self: Reciprocal,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_global_differential(global_differential, next_accumulated)

    def _synthetic_partial_helper(
        self: Reciprocal,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(
            ex.Negation(ex.Reciprocal(ex.Power(self._a, ex.Constant(2)))),
            multiplier
        )

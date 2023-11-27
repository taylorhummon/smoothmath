from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
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

    def _partial_at(
        self: Reciprocal,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._partial_at(point, with_respect_to)
        result_value = self._evaluate(point)
        return - (result_value ** 2) * a_partial

    def _compute_all_partials_at(
        self: Reciprocal,
        all_partials: AllPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(point)
        next_accumulated = - accumulated * (self_value ** 2)
        self._a._compute_all_partials_at(all_partials, point, next_accumulated)

    def _synthetic_partial(
        self: Reciprocal,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_all_synthetic_partials(
        self: Reciprocal,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_all_synthetic_partials(synthetic, next_accumulated)

    def _synthetic_partial_helper(
        self: Reciprocal,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(
            ex.Negation(ex.Reciprocal(ex.Power(self._a, ex.Constant(2)))),
            multiplier
        )

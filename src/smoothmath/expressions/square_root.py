from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.expression import Expression

import math
from smoothmath.expression import UnaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(sqrt(a)) = (1 / (2 sqrt(a))) * da

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _verify_domain_constraints(
        self: SquareRoot,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("SquareRoot(x) is not smooth around x = 0")
        elif a_value < 0:
            raise DomainError("SquareRoot(x) is undefined for x < 0")

    def _evaluate(
        self: SquareRoot,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self._value = math.sqrt(a_value)
        return self._value

    def _partial_at(
        self: SquareRoot,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._partial_at(point, with_respect_to)
        return a_partial / (2 * math.sqrt(a_value))

    def _global_partial(
        self: SquareRoot,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        return self._global_partial_helper(a_partial)

    def _compute_local_partials(
        self: SquareRoot,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(point)
        next_accumulated = accumulated / (2 * self_value)
        self._a._compute_local_partials(computed_local_partials, point, next_accumulated)

    def _compute_global_partials(
        self: SquareRoot,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._global_partial_helper(accumulated)
        self._a._compute_global_partials(computed_global_partials, next_accumulated)

    def _global_partial_helper(
        self: SquareRoot,
        multiplier: Expression
    ) -> Expression:
        return ex.Divide(
            multiplier,
            ex.Multiply(ex.Constant(2), ex.SquareRoot(self._a))
        )

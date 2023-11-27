from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(a * b) = b * da + a * db

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        point: Point
    ) -> real_number:
        pair_or_none = self._get_a_and_b_values_or_none(point)
        if pair_or_none == None:
            self._value = 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._value = a_value * b_value
        return self._value

    def _local_partial(
        self: Multiply,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        pair_or_none = self._get_a_and_b_values_or_none(point)
        if pair_or_none == None:
            return 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            a_partial = self._a._local_partial(point, with_respect_to)
            b_partial = self._b._local_partial(point, with_respect_to)
            return b_value * a_partial + a_value * b_partial

    def _global_partial(
        self: Multiply,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        b_partial = self._b._global_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._b, a_partial),
            ex.Multiply(self._a, b_partial)
        )

    def _compute_local_partials(
        self: Multiply,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        pair_or_none = self._get_a_and_b_values_or_none(point)
        if pair_or_none == None:
            return
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._a._compute_local_partials(computed_local_partials, point, accumulated * b_value)
            self._b._compute_local_partials(computed_local_partials, point, accumulated * a_value)

    def _compute_global_partials(
        self: Multiply,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        self._a._compute_global_partials(computed_global_partials, ex.Multiply(accumulated, self._b))
        self._b._compute_global_partials(computed_global_partials, ex.Multiply(accumulated, self._a))

    # the following method is used to allow shirt-circuiting of either a * 0 or 0 * b
    def _get_a_and_b_values_or_none(
        self: Multiply,
        point: Point
    ) -> tuple[real_number, real_number] | None:
        try:
            a_value = self._a._evaluate(point)
        except DomainError as error:
            try:
                b_value_inner = self._b._evaluate(point)
            except DomainError:
                raise error
            if b_value_inner == 0:
                return None
            raise
        try:
            b_value = self._b._evaluate(point)
        except DomainError as error:
            try:
                a_value_inner = self._a._evaluate(point)
            except DomainError:
                raise error
            if a_value_inner == 0:
                return None
            raise
        return (a_value, b_value)

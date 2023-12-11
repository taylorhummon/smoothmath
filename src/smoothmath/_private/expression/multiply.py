from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(a * b) = b * da + a * db

class Multiply(base.BinaryExpression):
    def __init__(
        self: Multiply,
        expression_a: sm.Expression,
        expression_b: sm.Expression
    ) -> None:
        super().__init__(expression_a, expression_b)

    def _evaluate(
        self: Multiply,
        point: sm.Point
    ) -> sm.real_number:
        pair_or_none = self._get_a_and_b_values_or_none(point)
        if pair_or_none == None:
            self._value = 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._value = a_value * b_value
        return self._value

    def _local_partial(
        self: Multiply,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        pair_or_none = self._get_a_and_b_values_or_none(point)
        if pair_or_none == None:
            return 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            a_partial = self._a._local_partial(point, with_respect_to)
            b_partial = self._b._local_partial(point, with_respect_to)
            return b_value * a_partial + a_value * b_partial

    def _synthetic_partial(
        self: Multiply,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._b, a_partial),
            ex.Multiply(self._a, b_partial)
        )

    def _compute_local_differential(
        self: Multiply,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        pair_or_none = self._get_a_and_b_values_or_none(builder.point)
        if pair_or_none == None:
            return
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._a._compute_local_differential(builder, accumulated * b_value)
            self._b._compute_local_differential(builder, accumulated * a_value)

    def _compute_global_differential(
        self: Multiply,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._a._compute_global_differential(builder, ex.Multiply(accumulated, self._b))
        self._b._compute_global_differential(builder, ex.Multiply(accumulated, self._a))

    # the following method is used to allow shirt-circuiting of either a * 0 or 0 * b
    def _get_a_and_b_values_or_none(
        self: Multiply,
        point: sm.Point
    ) -> tuple[sm.real_number, sm.real_number] | None:
        try:
            a_value = self._a._evaluate(point)
        except sm.DomainError as error:
            try:
                _b_value = self._b._evaluate(point)
            except sm.DomainError:
                raise error
            if _b_value == 0:
                return None
            raise
        try:
            b_value = self._b._evaluate(point)
        except sm.DomainError as error:
            try:
                _a_value = self._a._evaluate(point)
            except sm.DomainError:
                raise error
            if _a_value == 0:
                return None
            raise
        return (a_value, b_value)

from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Multiply(base.BinaryExpression):
    def _verify_domain_constraints(
        self: Multiply,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Multiply,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        return left_value * right_value

    def _evaluate(
        self: Multiply,
        point: sm.Point
    ) -> sm.real_number:
        pair_or_none = self._get_inner_values_or_none(point)
        if pair_or_none == None:
            self._value = 0
        else: # pair_or_none is the pair (left_value, right_value)
            left_value, right_value = pair_or_none
            self._value = left_value * right_value
        return self._value

    def _local_partial(
        self: Multiply,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        pair_or_none = self._get_inner_values_or_none(point)
        if pair_or_none == None:
            return 0
        else: # pair_or_none is the pair (left_value, right_value)
            left_value, right_value = pair_or_none
            left_partial = self._left._local_partial(point, with_respect_to)
            right_partial = self._right._local_partial(point, with_respect_to)
            return right_value * left_partial + left_value * right_partial

    def _synthetic_partial(
        self: Multiply,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._right, left_partial),
            ex.Multiply(self._left, right_partial)
        )

    def _compute_local_differential(
        self: Multiply,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        pair_or_none = self._get_inner_values_or_none(builder.point)
        if pair_or_none == None:
            return
        else: # pair_or_none is the pair (left_value, right_value)
            left_value, right_value = pair_or_none
            self._left._compute_local_differential(builder, right_value * accumulated)
            self._right._compute_local_differential(builder, left_value * accumulated)

    def _compute_global_differential(
        self: Multiply,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, ex.Multiply(self._right, accumulated))
        self._right._compute_global_differential(builder, ex.Multiply(self._left, accumulated))

    # the following method is used to allow shirt-circuiting of either left * 0 or 0 * right
    def _get_inner_values_or_none(
        self: Multiply,
        point: sm.Point
    ) -> tuple[sm.real_number, sm.real_number] | None:
        try:
            left_value = self._left._evaluate(point)
        except sm.DomainError as error:
            try:
                _right_value = self._right._evaluate(point)
            except sm.DomainError:
                raise error
            if _right_value == 0:
                return None
            raise
        try:
            right_value = self._right._evaluate(point)
        except sm.DomainError as error:
            try:
                _left_value = self._left._evaluate(point)
            except sm.DomainError:
                raise error
            if _left_value == 0:
                return None
            raise
        return (left_value, right_value)
